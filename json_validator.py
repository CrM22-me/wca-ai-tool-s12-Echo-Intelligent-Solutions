# ==========================================
# ECHO INTELLIGENT SOLUTIONS
# AI STUDY BUDDY - JSON VALIDATOR
# ==========================================

import json


# Required fields in every AI study response
REQUIRED_FIELDS = [
    "status",
    "question",
    "feedback",
    "is_correct",
    "score",
    "topics_to_revise"
]


def validate_ai_response(response):
    """
    Checks whether the AI response contains valid JSON
    and all required fields.
    """

    try:
        # Convert the AI response into a Python dictionary
        data = json.loads(response)

        # Check whether all required fields are present
        for field in REQUIRED_FIELDS:
            if field not in data:
                raise ValueError(f"Missing field: {field}")

        # Check whether required text fields are not empty
        if not isinstance(data["status"], str) or not data["status"].strip():
            raise ValueError("Status cannot be empty.")

        if not isinstance(data["question"], str) or not data["question"].strip():
            raise ValueError("Question cannot be empty.")

        if not isinstance(data["feedback"], str):
            raise ValueError("Feedback must be text.")

        # Check the correctness field
        if not isinstance(data["is_correct"], bool):
            raise ValueError("is_correct must be true or false.")

        # Check the score field
        if not isinstance(data["score"], int) or isinstance(data["score"], bool):
            raise ValueError("Score must be an integer.")

        if data["score"] < 0:
            raise ValueError("Score cannot be negative.")

        # Check revision topics
        if not isinstance(data["topics_to_revise"], list):
            raise ValueError("topics_to_revise must be a list.")

        return True, data

    except json.JSONDecodeError:
        return False, "AI response is not valid JSON."

    except ValueError as error:
        return False, str(error)


def validate_with_retry(response, retry_function):
    """
    Validates an AI response.
    If validation fails, it attempts one retry.
    """

    is_valid, result = validate_ai_response(response)

    if is_valid:
        return result

    print("\nInvalid AI response detected.")
    print("Attempting to generate a corrected response...")

    try:
        # Make one additional attempt
        new_response = retry_function()
        
        is_valid, result = validate_ai_response(new_response)

        if is_valid:
            print("AI response successfully corrected.")
            return result

        print("The second response also failed validation.")

    except Exception as error:
        print(f"Retry failed: {error}")

    return None