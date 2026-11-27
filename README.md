ECHO INTELLIGENT SOLUTIONS

AI-POWERED STUDY BUDDY

1. Project Overview

Echo Intelligent Solutions – AI Study Buddy is an AI-powered educational assistant designed to help students learn, understand academic concepts, and improve their study experience.

The application integrates Google's Gemini AI API to provide interactive, personalized learning assistance through multi-turn conversations.

It maintains conversation memory, allowing students to continue learning from previous interactions. It also tracks student progress and generates session summaries for future reference.

2. Key Features

- Interactive Learning: Students can ask questions and receive AI-generated explanations.
- Conversation Memory: Maintains context throughout a study session.
- Session Management: Allows students to create new sessions and reopen previous sessions.
- Progress Tracking: Records student learning progress.
- AI-Generated Summaries: Generates summaries of completed study sessions.
- Persistent Storage: Saves session information for future reference.
- Gemini Integration: Uses Google's Gemini AI model to power intelligent responses.

3. Technologies Used

- Python – Main programming language.
- Google Gemini API – AI integration.
- "google-genai" – Gemini API Python SDK.
- "python-dotenv" – Environment variable management.
- JSON – Structured data storage and processing.

4. Requirements

Before running the application, ensure you have:

- Python 3.10 or later.
- An active Google Gemini API key.
- Internet connectivity.
- Required Python packages.

5. Installation and Setup

Step 1: Clone the repository

git clone https://github.com/CrM22-me/wca-ai-tool-s12-Echo-Intelligent-Solutions

Navigate into the project directory:

cd wca-ai-tool-s12-Echo-Intelligent-Solutions

Step 2: Install dependencies

pip install -r requirements.txt

Step 3: Configure the API key

Create a file named ".env" in the project's root directory.

Add your Gemini API key:

GEMINI_API_KEY=your_actual_api_key

Replace "your_actual_api_key" with your valid Google Gemini API key.

Important: Keep your API key private. Never upload the ".env" file to GitHub.

Step 4: Run the application

From the project root directory, execute:

python main.py

Follow the instructions displayed in the terminal to interact with the Study Buddy.

6. How to Use the Application

1. Launch the application using "python main.py".
2. Select New Session to begin a study session.
3. Enter the student's name.
4. Enter the academic topic to be studied.
5. Interact with the AI assistant by asking questions.
6. Receive explanations and learning support.
7. Continue the conversation while the application maintains context.
8. End the session to generate and save a session summary.
9. Select Open Past Session to access previously saved sessions.

7. Project Structure

The project is organized into separate Python modules to support modular development and easier maintenance.

- "main.py" – Application entry point and main menu.
- "study_buddy.py" – Core study assistant functionality.
- "memory.py" – Conversation memory management.
- "prompts.py" – AI instruction and prompt definitions.
- "requirements.txt" – Project dependencies.
- ".env" – Stores the Gemini API key (excluded from GitHub).
- "samples/" – Stores sample project data, where applicable.

8. Security

The application uses environment variables to protect sensitive API credentials.

The ".env" file should be excluded from version control using ".gitignore".

Example ".gitignore" entries:

.env
__pycache__/
*.pyc

9. Development Team

Echo Intelligent Solutions – Project Team

1. Simon Willy Sitati
2. Akinyi Mercy
3. Harrison Njogu

10. Project Purpose

The purpose of Echo Intelligent Solutions – AI Study Buddy is to demonstrate how artificial intelligence, memory management, and structured data processing can be integrated into a practical educational tool.

The project aims to make learning more interactive, accessible, and personalized through AI-powered assistance.

---

Developed as part of the WECAN Academy Artificial Intelligence Course – Season 12, Months 1–3 End of Module Project.