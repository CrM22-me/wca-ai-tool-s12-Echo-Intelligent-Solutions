# ==================================================
# ECHO INTELLIGENT SOLUTIONS
# AI STUDY BUDDY - MAIN AI ENGINE
# ==================================================

import os
import json
import time

from dotenv import load_dotenv
from google import genai
from google.genai import types

from prompts import SYSTEM_PROMPT, SUMMARY_PROMPT

from memory import (
    initialize_memory,
    add_user_message,
    add_ai_message
)

from json_validator import validate_with_retry

from progress_tracker import (
    initialize_progress,
    record_answer,
    display_progress,
    get_revision_questions
)

from summary import (
    prepare_summary_request,
    parse_summary_response,
    display_summary
)

from session_manager import save_session


# ==================================================
# 1. LOAD API CONFIGURATION
# ==================================================

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

MODEL_NAME = "gemini-3.8-flash"


# ==================================================
# 2. CREATE GEMINI CLIENT
# ==================================================

def create_ai_client():

    if not API_KEY:
        raise ValueError(
            "GEMINI_API_KEY was not found. "
            "Please check your .env file."
        )

    return genai.Client(api_key=API_KEY)


# ==================================================
# 3. SEND CONVERSATION TO GEMINI
# ==================================================

def call_gemini(
    messages,
    retry=False,
    system_prompt=None
):

    client = create_ai_client()

    conversation = []

    # Convert conversation memory into Gemini format
    for message in messages:

        role = message.get("role")
        content = message.get("content", "")

        if role == "user":

            conversation.append({
                "role": "user",
                "parts": [{"text": content}]
            })

        elif role == "assistant":

            conversation.append({
                "role": "model",
                "parts": [{"text": content}]
            })

    # Request corrected JSON if validation fails
    if retry:

        conversation.append({
            "role": "user",
            "parts": [{
                "text": (
                    "Your previous response did not meet "
                    "the required JSON format. "
                    "Correct it and return valid JSON only. "
                    "Include every required field."
                )
            }]
        })

    # Retry temporary server errors
    for attempt in range(3):

        try:

            response = client.models.generate_content(

                model=MODEL_NAME,

                contents=conversation,

                config=types.GenerateContentConfig(

                    system_instruction=(
                        system_prompt or SYSTEM_PROMPT
                    ),

                    response_mime_type="application/json"
                )
            )

            if not response.text:

                raise ValueError(
                    "Gemini returned an empty response."
                )

            return response.text

        except Exception as error:

            error_message = str(error)

            if "503" in error_message and attempt < 2:

                wait_time = 3 * (attempt + 1)

                print(
                    "\nGemini is temporarily busy. "
                    f"Retrying in {wait_time} seconds..."
                )

                time.sleep(wait_time)

            else:

                raise


# ==================================================
# 4. DISPLAY AI RESPONSE
# ==================================================

def display_ai_response(data):

    print("\n==================================")
    print("          STUDY BUDDY")
    print("==================================")

    if data.get("feedback"):

        print("\nFeedback:")
        print(data["feedback"])

    if data.get("question"):

        print("\nNext Question:")
        print(data["question"])

    print("==================================")


# ==================================================
# 5. VALIDATE AI RESPONSE
# ==================================================

def get_valid_ai_response(messages):

    response = call_gemini(messages)

    data = validate_with_retry(

        response,

        lambda: call_gemini(
            messages,
            retry=True
        )
    )

    return data


# ==================================================
# 6. FINAL AI SUMMARY
# ==================================================

def generate_final_summary(
    student_name,
    study_topic,
    messages,
    progress
):

    print("\n==================================")
    print("       GENERATING FINAL SUMMARY")
    print("==================================")

    summary_messages = prepare_summary_request(

        student_name,
        study_topic,
        messages,
        progress
    )

    summary = None

    try:

        # First summarization request
        response = call_gemini(

            summary_messages,

            system_prompt=SUMMARY_PROMPT
        )

        summary = parse_summary_response(response)

        # Retry if summary validation fails
        if summary is None:

            print("\nRequesting corrected AI summary...")

            response = call_gemini(

                summary_messages,

                retry=True,

                system_prompt=SUMMARY_PROMPT
            )

            summary = parse_summary_response(response)

        if summary is None:

            raise ValueError(
                "Gemini could not produce a valid summary."
            )

    except Exception as error:

        print(
            f"\nAI summarization error: {error}"
        )

        # Preserve the actual session data
        summary = {

            "student_name": student_name,
            "subject": study_topic,
            "topic": study_topic,

            "strengths": [],

            "topics_to_revise": [
                item.get("question", "")
                for item in progress["questions_to_revise"]
            ],

            "recommendations": [
                "Continue practising the study topic."
            ],

            "overall_feedback": (
                "AI summarization was unsuccessful. "
                "Your actual performance records are preserved."
            )
        }

    # Python progress records are authoritative
    total = progress["total_questions"]
    correct = progress["correct_answers"]

    summary["student_name"] = student_name
    summary["subject"] = summary.get("subject") or study_topic
    summary["topic"] = study_topic

    summary["total_questions"] = total
    summary["correct_answers"] = correct

    summary["incorrect_answers"] = (
        progress["incorrect_answers"]
    )

    summary["performance_percentage"] = (

        round((correct / total) * 100, 2)

        if total > 0 else 0
    )

    summary["progress_details"] = progress

    # Display final report
    display_summary(summary)

    return summary


# ==================================================
# 7. SAVE COMPLETED STUDY SESSION
# ==================================================

def save_completed_session(
    student_name,
    study_topic,
    messages,
    summary
):

    print("\nSaving your study session...")

    filepath = save_session(

        student_name,
        study_topic,
        messages,
        summary
    )

    if filepath:

        print("\nYour study session was saved successfully.")

    else:

        print("\nUnable to save your study session.")

    return filepath


# ==================================================
# 8. RUN REVISION QUESTIONS
# ==================================================

def run_revision(messages, progress):

    revision_questions = get_revision_questions(progress)

    if not revision_questions:

        print("\nNo incorrect answers to revise.")

        return

    print("\n==================================")
    print("             REVISION")
    print("==================================")

    for item in revision_questions:

        question = item.get("question", "")

        if not question:
            continue

        print("\nPrevious Question:")
        print(question)

        answer = input(
            "\nTry answering again: "
        ).strip()

        if not answer:

            print("No revision answer submitted.")

            continue

        revision_message = (

            "Revision attempt. "

            f"Previous question: {question}\n"

            f"My revised answer: {answer}\n"

            "Please assess my revised answer."
        )

        add_user_message(
            messages,
            revision_message
        )

        try:

            data = get_valid_ai_response(messages)

            if data is None:

                print(
                    "Revision response could not be validated."
                )

                messages.pop()

                continue

            add_ai_message(
                messages,
                json.dumps(data)
            )

            print("\nRevision Feedback:")

            print(
                data.get(
                    "feedback",
                    "No feedback provided."
                )
            )

            # Update revision tracking if the answer is correct
            if data.get("is_correct"):

                progress["questions_to_revise"] = [

                    question_item

                    for question_item in progress["questions_to_revise"]

                    if question_item.get("question") != question
                ]

        except Exception as error:

            print(
                f"\nRevision error: {error}"
            )

            if messages and messages[-1].get("role") == "user":

                messages.pop()


# ==================================================
# 9. RUN THE STUDY SESSION
# ==================================================

def run_study_session(student_name, study_topic):

    try:

        print("\n==================================")
        print("       STARTING STUDY SESSION")
        print("==================================")

        print(f"Student: {student_name}")
        print(f"Topic: {study_topic}")

        # Initialize conversation memory
        messages = initialize_memory(

            student_name,
            study_topic
        )

        # Initialize progress tracking
        progress = initialize_progress()

        current_question = None

        print("\nConnecting to Gemini AI...")

        # Generate first AI question
        data = get_valid_ai_response(messages)

        if data is None:

            print(
                "Unable to generate a valid first question."
            )

            return None

        # Save first AI response in memory
        add_ai_message(
            messages,
            json.dumps(data)
        )

        current_question = data.get(
            "question",
            ""
        )

        display_ai_response(data)

        # ==================================
        # MAIN CONVERSATION LOOP
        # ==================================

        while True:

            user_input = input(

                "\nYour answer "
                "(or type 'end' to finish): "

            ).strip()

            if not user_input:

                print("Please enter an answer.")

                continue

            if user_input.lower() in [

                "end",
                "exit",
                "finish"

            ]:

                print("\nEnding your study session...")

                break

            # Store student's answer
            add_user_message(
                messages,
                user_input
            )

            try:

                # Send full conversation history to Gemini
                data = get_valid_ai_response(messages)

                if data is None:

                    print(
                        "\nThe AI response could not be validated."
                    )

                    messages.pop()

                    continue

                # Record answer performance
                is_correct = data["is_correct"]

                score = 1 if is_correct else 0

                record_answer(

                    progress,

                    current_question,

                    user_input,

                    is_correct,

                    score
                )

                # Store AI response
                add_ai_message(

                    messages,

                    json.dumps(data)
                )

                # Display feedback and next question
                display_ai_response(data)

                # Display progress
                display_progress(progress)

                # Update current question
                current_question = data.get(
                    "question",
                    ""
                )

            except Exception as error:

                print(
                    f"\nAI connection error: {error}"
                )

                if messages and messages[-1].get("role") == "user":

                    messages.pop()

                print(
                    "You can try submitting your answer again."
                )

        # ==================================
        # REVISION SECTION
        # ==================================

        run_revision(
            messages,
            progress
        )

        # ==================================
        # FINAL SESSION RESULTS
        # ==================================

        print("\n==================================")
        print("       SESSION COMPLETED")
        print("==================================")

        display_progress(progress)

        # Generate final AI summary
        summary = generate_final_summary(

            student_name,

            study_topic,

            messages,

            progress
        )

        # Automatically save conversation and summary
        save_completed_session(

            student_name,

            study_topic,

            messages,

            summary
        )

        print("\nThank you for studying with Echo Study Buddy!")

        return messages, progress

    except Exception as error:

        print(
            f"\nStudy session error: {error}"
        )

        return None


# ==================================================
# 10. MODULE ENTRY POINT
# ==================================================

if __name__ == "__main__":

    print("Echo Intelligent Solutions")
    print("Study Buddy AI Engine")

    print(
        "\nRun the application through main.py."
    )