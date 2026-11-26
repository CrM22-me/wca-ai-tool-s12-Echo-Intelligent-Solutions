# ==========================================
# ECHO INTELLIGENT SOLUTIONS
# AI STUDY BUDDY - MAIN AI ENGINE
# ==========================================

import os
import json

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
    display_progress
)


# Load API key from the .env file
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

MODEL_NAME = "gemini-3.8-flash"


def create_ai_client():
    """
    Creates a connection to the Gemini AI model.
    """

    if not API_KEY:
        raise ValueError("Gemini API key not found.")

    return genai.Client(api_key=API_KEY)


def call_gemini(messages, retry=False, system_prompt=None):
    """
    Sends the complete conversation history to Gemini.
    """

    client = create_ai_client()

    conversation = []

    for message in messages:

        if message["role"] == "user":
            conversation.append({
                "role": "user",
                "parts": [{"text": message["content"]}]
            })

        elif message["role"] == "assistant":
            conversation.append({
                "role": "model",
                "parts": [{"text": message["content"]}]
            })

    if retry:
        conversation.append({
            "role": "user",
            "parts": [{
                "text": (
                    "Your previous response was invalid. "
                    "Return corrected valid JSON with all "
                    "required fields. Return JSON only."
                )
            }]
        })

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=conversation,
        config=types.GenerateContentConfig(
            system_instruction=system_prompt or SYSTEM_PROMPT,
            response_mime_type="application/json"
        )
    )

    if not response.text:
        raise ValueError("Gemini returned an empty response.")

    return response.text


def display_ai_response(data):
    """
    Displays AI feedback and the next question.
    """

    print("\n--------------------------------")
    print("       AI STUDY BUDDY")
    print("--------------------------------")

    if data["feedback"]:
        print("\nFeedback:", data["feedback"])

    if data["question"]:
        print("\nQuestion:", data["question"])

    print("--------------------------------")


def run_study_session(student_name, study_topic):
    """
    Runs the interactive study session.
    Maintains conversation memory and tracks progress.
    """

    try:
        # Initialize conversation memory
        messages = initialize_memory(
            student_name,
            study_topic
        )

        # Initialize student progress
        progress = initialize_progress()

        print("\nConnecting to Gemini AI...")

        # Generate the first question
        response = call_gemini(messages)

        data = validate_with_retry(
            response,
            lambda: call_gemini(messages, retry=True)
        )

        if data is None:
            print("Unable to generate a valid question.")
            return None

        # Save the first AI response
        add_ai_message(messages, json.dumps(data))

        # Remember the current question
        current_question = data["question"]

        display_ai_response(data)

        # Continue the study conversation
        while True:

            user_input = input(
                "\nYour answer (or type 'end' to finish): "
            ).strip()

            if not user_input:
                print("Please enter an answer.")
                continue

            if user_input.lower() in ["end", "exit", "finish"]:
                print("\nEnding your study session...")
                break

            # Store the student's answer
            add_user_message(messages, user_input)

            try:
                # Send the complete conversation history
                response = call_gemini(messages)

                # Validate the AI response
                data = validate_with_retry(
                    response,
                    lambda: call_gemini(messages, retry=True)
                )

                if data is None:
                    print("Unable to process the response.")

                    # Remove unanswered turn from memory
                    messages.pop()
                    continue

                # Record the answer to the previous question
                is_correct = data["is_correct"]

                # Award one mark for correct answers
                score = 1 if is_correct else 0

                record_answer(
                    progress,
                    current_question,
                    user_input,
                    is_correct,
                    score
                )

                # Store the validated AI response
                add_ai_message(
                    messages,
                    json.dumps(data)
                )

                # Display feedback and next question
                display_ai_response(data)

                # Display updated student performance
                display_progress(progress)

                # Update the current question
                current_question = data["question"]

            except Exception as error:
                print(f"\nAI connection error: {error}")

                # Remove the unanswered turn
                messages.pop()

        print("\nStudy conversation completed.")

        # Return conversation and progress data
        return messages, progress

    except Exception as error:
        print(f"\nUnable to start study session: {error}")
        return None