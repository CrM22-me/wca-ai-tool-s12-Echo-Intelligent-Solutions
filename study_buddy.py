import os
import json
import time

from dotenv import load_dotenv
from google import genai
from google.genai import types

from prompts import SYSTEM_PROMPT
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


# ==========================================
# 1. LOAD API CONFIGURATION
# ==========================================

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

# Use the same model name that worked in your API test.
MODEL_NAME = "gemini-3.8-flash"


# ==========================================
# 2. CREATE GEMINI CLIENT
# ==========================================

def create_ai_client():

    if not API_KEY:
        raise ValueError(
            "GEMINI_API_KEY was not found. "
            "Check your .env file."
        )

    return genai.Client(api_key=API_KEY)


# ==========================================
# 3. SEND CONVERSATION TO GEMINI
# ==========================================

def call_gemini(messages, retry=False, system_prompt=None):

    client = create_ai_client()

    conversation = []

    # Convert our conversation history into Gemini format.
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

    # Request a corrected JSON response if validation failed.
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

    # Retry temporary server overload errors.
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
                    "The AI returned an empty response."
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


# ==========================================
# 4. DISPLAY AI RESPONSE
# ==========================================

def display_ai_response(data):

    print("\n----------------------------------")
    print("STUDY BUDDY")
    print("----------------------------------")

    if data.get("feedback"):

        print("\nFeedback:")
        print(data["feedback"])

    if data.get("question"):

        print("\nNext Question:")
        print(data["question"])

    print("----------------------------------")


# ==========================================
# 5. HANDLE AI RESPONSE VALIDATION
# ==========================================

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


# ==========================================
# 6. RUN THE STUDY SESSION
# ==========================================

def run_study_session(student_name, study_topic):

    try:

        print("\n==================================")
        print("       STARTING STUDY SESSION")
        print("==================================")

        print(f"Student: {student_name}")
        print(f"Topic: {study_topic}")

        # Initialize conversation memory.
        messages = initialize_memory(
            student_name,
            study_topic
        )

        # Initialize student progress.
        progress = initialize_progress()

        # Track the question currently awaiting an answer.
        current_question = None

        # ----------------------------------
        # GET THE FIRST AI QUESTION
        # ----------------------------------

        data = get_valid_ai_response(messages)

        if data is None:
            print("\nUnable to start the study session.")
            return None

        add_ai_message(
            messages,
            json.dumps(data)
        )

        current_question = data.get("question", "")

        display_ai_response(data)

        # ----------------------------------
        # MAIN CONVERSATION LOOP
        # ----------------------------------

        while True:

            user_input = input(
                "\nYour answer "
                "(or type 'end' to finish): "
            ).strip()

            # Do not accept empty answers.
            if not user_input:

                print(
                    "Please enter an answer before continuing."
                )

                continue

            # Allow the student to end the session.
            if user_input.lower() in [
                "end",
                "exit",
                "finish"
            ]:

                print("\nEnding your study session...")
                break

            # Save the student's answer in conversation memory.
            add_user_message(
                messages,
                user_input
            )

            try:

                # Send the full conversation history.
                data = get_valid_ai_response(messages)

                if data is None:

                    print(
                        "\nThe AI response could not be validated. "
                        "Please try answering again."
                    )

                    # Remove the failed answer from memory.
                    messages.pop()

                    continue

                # ----------------------------------
                # RECORD THE ANSWER AND PROGRESS
                # ----------------------------------

                is_correct = data["is_correct"]

                score = 1 if is_correct else 0

                record_answer(

                    progress,

                    current_question,

                    user_input,

                    is_correct,

                    score
                )

                # Save the AI response in conversation memory.
                add_ai_message(
                    messages,
                    json.dumps(data)
                )

                # Display feedback and the next question.
                display_ai_response(data)

                # Display updated student progress.
                display_progress(progress)

                # Update the question awaiting an answer.
                current_question = data.get(
                    "question",
                    ""
                )

            except Exception as error:

                print(
                    "\nAn error occurred while processing "
                    f"your answer: {error}"
                )

                # Remove the answer if it was not successfully processed.
                if messages and messages[-1].get("role") == "user":
                    messages.pop()

                print(
                    "You can try submitting your answer again."
                )

        # ----------------------------------
        # REVISIT INCORRECT ANSWERS
        # ----------------------------------

        revision_questions = get_revision_questions(progress)

        if revision_questions:

            print("\n==================================")
            print("       REVISION TIME")
            print("==================================")

            print(
                "You have some questions to revisit."
            )

            for item in revision_questions:

                question = (
                    item.get("question", "")
                    if isinstance(item, dict)
                    else str(item)
                )

                if not question:
                    continue

                print("\nPrevious Question:")
                print(question)

                revision_answer = input(
                    "\nTry answering it again: "
                ).strip()

                if not revision_answer:
                    print("No revision answer submitted.")
                    continue

                add_user_message(
                    messages,
                    (
                        "Revision attempt. "
                        f"Previous question: {question}\n"
                        f"My revised answer: {revision_answer}\n"
                        "Please assess this revised answer."
                    )
                )

                revision_data = get_valid_ai_response(messages)

                if revision_data is None:
                    print(
                        "The revision response could not "
                        "be validated."
                    )
                    messages.pop()
                    continue

                add_ai_message(
                    messages,
                    json.dumps(revision_data)
                )

                print("\nRevision Feedback:")
                print(revision_data["feedback"])

        # ----------------------------------
        # FINAL SESSION RESULTS
        # ----------------------------------

        print("\n==================================")
        print("       SESSION COMPLETED")
        print("==================================")

        display_progress(progress)

        return messages, progress

    except Exception as error:

        print(
            "\nStudy session error: "
            f"{error}"
        )

        return None