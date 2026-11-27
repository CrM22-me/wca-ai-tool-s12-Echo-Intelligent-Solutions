# ==========================================
# ECHO INTELLIGENT SOLUTIONS
# AI STUDY BUDDY - MAIN APPLICATION
# ==========================================

from study_buddy import run_study_session
from session_manager import open_past_session


# ==========================================
# 1. MAIN MENU
# ==========================================

def main_menu():

    print("\n========================================")
    print("       ECHO INTELLIGENT SOLUTIONS")
    print("              STUDY BUDDY")
    print("========================================")
    print("1. New Study Session")
    print("2. Open Past Session")
    print("3. Exit")
    print("========================================")


# ==========================================
# 2. NEW STUDY SESSION
# ==========================================

def new_study_session():

    print("\n========================================")
    print("          CREATE NEW SESSION")
    print("========================================")

    student_name = input("Enter student name: ").strip()

    if not student_name:
        print("\nStudent name cannot be empty.")
        return

    study_topic = input("Enter study topic: ").strip()

    if not study_topic:
        print("\nStudy topic cannot be empty.")
        return

    print("\nPreparing your study session...")

    try:

        result = run_study_session(
            student_name,
            study_topic
        )

        if result is None:
            print("\nStudy session could not be completed.")
            return

        messages, progress = result

        print("\n========================================")
        print("          SESSION ENDED")
        print("========================================")

        print(f"Student: {student_name}")
        print(f"Topic: {study_topic}")

        print("\nYour learning progress has been recorded.")

    except Exception as error:

        print(f"\nSession error: {error}")


# ==========================================
# 3. OPEN PREVIOUS SESSION
# ==========================================

def view_past_sessions():

    print("\nOpening previous study sessions...")

    try:

        open_past_session()

    except Exception as error:

        print(f"\nUnable to open past sessions: {error}")


# ==========================================
# 4. MAIN APPLICATION LOOP
# ==========================================

def main():

    print("\nWelcome to Echo Intelligent Solutions!")
    print("Your AI-powered learning companion.")

    while True:

        main_menu()

        choice = input(
            "\nEnter your choice (1-3): "
        ).strip()

        if choice == "1":

            new_study_session()

        elif choice == "2":

            view_past_sessions()

        elif choice == "3":

            print("\n========================================")
            print("Thank you for using STUDY BUDDY!")
            print("Keep learning. Keep growing.")
            print("========================================")

            break

        else:

            print("\nInvalid selection.")

            print("Please enter 1, 2 or 3.")


# ==========================================
# 5. APPLICATION ENTRY POINT
# ==========================================

if __name__ == "__main__":

    main()