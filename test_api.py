import os
from dotenv import load_dotenv
from google import genai

# Load the API key
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("API key not found. Check your .env file.")

else:
    try:
        client = genai.Client(api_key=api_key)

        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents="Say hello to Echo Intelligent Solutions Study Buddy."
        )

        print("\nGemini connection successful!")
        print(response.text)

    except Exception as error:
        print("\nGemini connection failed:")
        print(error)