def main_menu():
    print("\n================================")
    print("   ECHO INTELLIGENT SOLUTIONS")
    print("          STUDY BUDDY")
    print("================================")
    print("1. New Session")
    print("2. Open Past Session")
    print("3. Exit")


def main():
    while True:
        main_menu()

        choice = input("\nEnter your choice (1-3): ")

        if choice == "1":
            print("\n--- NEW STUDY SESSION ---")

            student_name = input("Enter your name: ")
            study_topic = input("What would you like to study today? ")

            print(f"\nWelcome, {student_name}!")
            print(f"Your study topic is: {study_topic}")
            print("\nPreparing your study session...")

        elif choice == "2":
            print("\nOpening past sessions...")

        elif choice == "3":
            print("\nThank you for using Study Buddy!")
            break

        else:
            print("\nInvalid choice. Please select 1, 2, or 3.")


if __name__ == "__main__":
    main()