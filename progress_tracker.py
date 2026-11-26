# ==========================================
# ECHO INTELLIGENT SOLUTIONS
# AI STUDY BUDDY - PROGRESS TRACKER
# ==========================================


def initialize_progress():
    """
    Initializes the student's learning progress.
    """

    return {
        "total_questions": 0,
        "correct_answers": 0,
        "incorrect_answers": 0,
        "total_score": 0,
        "questions_to_revise": [],
        "attempted_questions": []
    }


def record_answer(progress, question, answer, is_correct, score):
    """
    Records a student's answer and updates their score.
    """

    progress["total_questions"] += 1

    progress["attempted_questions"].append({
        "question": question,
        "answer": answer,
        "is_correct": is_correct,
        "score": score
    })

    if is_correct:
        progress["correct_answers"] += 1

        # Add earned marks to the total score
        progress["total_score"] += score

        # Remove the question from the revision list
        progress["questions_to_revise"] = [
            item for item in progress["questions_to_revise"]
            if item["question"] != question
        ]

    else:
        progress["incorrect_answers"] += 1

        # Store incorrectly answered questions
        progress["questions_to_revise"].append({
            "question": question,
            "previous_answer": answer
        })

    return progress


def get_performance_percentage(progress):
    """
    Calculates the student's performance percentage.
    """

    total = progress["total_questions"]

    if total == 0:
        return 0

    percentage = (
        progress["correct_answers"] / total
    ) * 100

    return round(percentage, 2)


def get_revision_questions(progress):
    """
    Returns questions that the student needs to revise.
    """

    return progress["questions_to_revise"]


def display_progress(progress):
    """
    Displays the student's current learning progress.
    """

    print("\n========== LEARNING PROGRESS ==========")

    print(
        f"Questions Attempted: "
        f"{progress['total_questions']}"
    )

    print(
        f"Correct Answers: "
        f"{progress['correct_answers']}"
    )

    print(
        f"Incorrect Answers: "
        f"{progress['incorrect_answers']}"
    )

    print(
        f"Total Score: "
        f"{progress['total_score']}"
    )

    print(
        f"Performance: "
        f"{get_performance_percentage(progress)}%"
    )

    print("=======================================")


def prepare_progress_summary(progress):
    """
    Prepares progress information for the final AI summary.
    """

    return {
        "total_questions": progress["total_questions"],
        "correct_answers": progress["correct_answers"],
        "incorrect_answers": progress["incorrect_answers"],
        "total_score": progress["total_score"],
        "performance_percentage": get_performance_percentage(progress),
        "questions_to_revise": progress["questions_to_revise"],
        "attempted_questions": progress["attempted_questions"]
    }