# ==========================================
# ECHO INTELLIGENT SOLUTIONS
# AI STUDY BUDDY - SESSION SUMMARY
# ==========================================

import json

from prompts import SUMMARY_PROMPT


def prepare_summary_request(student_name, study_topic, messages):
    """
    Prepares the conversation history for the final
    AI summary request.
    """

    conversation_text = ""

    for message in messages:
        if message["role"] == "user":
            conversation_text += (
                f"\nStudent: {message['content']}\n"
            )

        elif message["role"] == "assistant":
            conversation_text += (
                f"\nAI Study Buddy: {message['content']}\n"
            )

    summary_messages = [
        {
            "role": "system",
            "content": SUMMARY_PROMPT
        },
        {
            "role": "user",
            "content": (
                f"Student Name: {student_name}\n"
                f"Study Topic: {study_topic}\n"
                f"Complete Study Conversation:\n"
                f"{conversation_text}\n\n"
                "Generate the final study session summary."
            )
        }
    ]

    return summary_messages


def calculate_performance(correct_answers, total_questions):
    """
    Calculates the student's performance percentage.
    """

    if total_questions == 0:
        return 0

    percentage = (correct_answers / total_questions) * 100

    return round(percentage, 2)


def display_summary(summary):
    """
    Displays the final study report to the student.
    """

    print("\n===================================")
    print("       STUDY SESSION SUMMARY")
    print("===================================")

    print(f"\nStudent: {summary.get('student_name', 'Unknown')}")
    print(f"Subject: {summary.get('subject', 'Not specified')}")
    print(f"Topic: {summary.get('topic', 'Not specified')}")

    print("\nPerformance:")
    print(f"Total Questions: {summary.get('total_questions', 0)}")
    print(f"Correct Answers: {summary.get('correct_answers', 0)}")
    print(f"Incorrect Answers: {summary.get('incorrect_answers', 0)}")

    print(
        f"Performance: "
        f"{summary.get('performance_percentage', 0)}%"
    )

    print("\nStrengths:")

    for strength in summary.get("strengths", []):
        print(f"- {strength}")

    print("\nTopics to Revise:")

    for topic in summary.get("topics_to_revise", []):
        print(f"- {topic}")

    print("\nRecommendations:")

    for recommendation in summary.get("recommendations", []):
        print(f"- {recommendation}")

    print("\nOverall Feedback:")
    print(summary.get("overall_feedback", "Keep learning!"))

    print("\n===================================")
    print("Thank you for studying with us!")
    print("===================================")


def parse_summary_response(response):
    """
    Converts the AI summary response into a Python dictionary.
    """

    try:
        summary = json.loads(response)

        required_fields = [
            "student_name",
            "subject",
            "topic",
            "total_questions",
            "correct_answers",
            "incorrect_answers",
            "performance_percentage",
            "strengths",
            "topics_to_revise",
            "recommendations",
            "overall_feedback"
        ]

        for field in required_fields:
            if field not in summary:
                raise ValueError(
                    f"Summary is missing required field: {field}"
                )

        if not isinstance(summary["strengths"], list):
            raise ValueError("Strengths must be a list.")

        if not isinstance(summary["topics_to_revise"], list):
            raise ValueError("Topics to revise must be a list.")

        if not isinstance(summary["recommendations"], list):
            raise ValueError("Recommendations must be a list.")

        return summary

    except json.JSONDecodeError:
        print("Error: AI returned an invalid summary format.")

    except ValueError as error:
        print(f"Summary validation error: {error}")

    return None