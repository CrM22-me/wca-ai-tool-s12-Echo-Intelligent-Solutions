# ==========================================
# ECHO INTELLIGENT SOLUTIONS
# AI STUDY BUDDY - SESSION MANAGER
# ==========================================

import json
import os
from datetime import datetime


# Folder where completed study sessions will be stored
SESSION_FOLDER = "samples"


def create_session_folder():
    """
    Creates the samples folder if it does not exist.
    """

    os.makedirs(SESSION_FOLDER, exist_ok=True)


def save_session(student_name, study_topic, messages, summary):
    """
    Saves the conversation and final summary
    into a dated JSON file.
    """

    create_session_folder()

    # Generate date and time for the filename
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    # Prepare the session data
    session_data = {
        "student_name": student_name,
        "study_topic": study_topic,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "conversation": messages,
        "summary": summary
    }

    # Create a safe filename
    safe_name = "".join(
        char if char.isalnum() else "_"
        for char in student_name
    )

    filename = f"{safe_name}_{timestamp}.json"

    filepath = os.path.join(SESSION_FOLDER, filename)

    # Save session data
    try:
        with open(filepath, "w", encoding="utf-8") as file:
            json.dump(session_data, file, indent=4, ensure_ascii=False)

        print(f"\nStudy session saved successfully!")
        print(f"File location: {filepath}")

        return filepath

    except OSError as error:
        print(f"Error saving session: {error}")
        return None


def open_past_session():
    """
    Displays a list of saved sessions
    and allows the student to open one.
    """

    create_session_folder()

    # Find all saved JSON session files
    files = [
        file for file in os.listdir(SESSION_FOLDER)
        if file.endswith(".json")
    ]

    if not files:
        print("\nNo previous study sessions found.")
        return

    print("\n========== PAST STUDY SESSIONS ==========")

    for index, filename in enumerate(files, start=1):
        print(f"{index}. {filename}")

    print("0. Return to main menu")

    try:
        choice = int(input("\nSelect a session to open: "))

        if choice == 0:
            return

        if choice < 1 or choice > len(files):
            print("Invalid session selection.")
            return

        selected_file = files[choice - 1]
        filepath = os.path.join(SESSION_FOLDER, selected_file)

        # Read and display the selected session
        with open(filepath, "r", encoding="utf-8") as file:
            session_data = json.load(file)

        print("\n========== SESSION DETAILS ==========")
        print(f"Student: {session_data['student_name']}")
        print(f"Topic: {session_data['study_topic']}")
        print(f"Date: {session_data['date']}")

        print("\n========== CONVERSATION ==========")

        for message in session_data["conversation"]:
            if message["role"] == "user":
                print(f"\nStudent: {message['content']}")

            elif message["role"] == "assistant":
                print(f"\nAI Study Buddy: {message['content']}")

        print("\n========== FINAL SUMMARY ==========")
        print(json.dumps(session_data["summary"], indent=4))

    except ValueError:
        print("Please enter a valid number.")

    except FileNotFoundError:
        print("The selected session file could not be found.")

    except (OSError, json.JSONDecodeError, KeyError, TypeError) as error:
        print(f"Unable to open session: {error}")