# ==========================================
# ECHO INTELLIGENT SOLUTIONS
# AI STUDY BUDDY - CONVERSATION MEMORY
# ==========================================

def initialize_memory(student_name, study_topic):
    """
    Creates a new conversation history for a student.
    """

    messages = [
        {
            "role": "system",
            "content": (
                "You are an AI Study Buddy. "
                "Help the student learn through interactive questions. "
                "Remember all previous interactions."
            )
        },
        {
            "role": "user",
            "content": (
                f"My name is {student_name}. "
                f"I want to study {study_topic}. "
                "Please begin my study session by asking "
                "one relevant question."
            )
        }
    ]

    return messages


def add_user_message(messages, user_input):
    """
    Adds the student's response to conversation history.
    """

    messages.append({
        "role": "user",
        "content": user_input
    })

    return messages


def add_ai_message(messages, ai_response):
    """
    Adds the AI's response to conversation history.
    """

    messages.append({
        "role": "assistant",
        "content": ai_response
    })

    return messages


def get_conversation_history(messages):
    """
    Returns the complete conversation history.
    This history will be sent to the AI with every API call.
    """

    return messages


def clear_memory():
    """
    Creates an empty conversation history.
    """

    return []