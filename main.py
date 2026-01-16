from dotenv import load_dotenv
import requests
import os


load_dotenv()


# API Configuration
API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"
API_KEY = os.getenv("GEMINI_API_KEY")


def generate_x_post(user_input: str) -> str:
    #     curl "https://generativelanguage.googleapis.com/v1beta/models/gemini-3-flash-preview:generateContent" \
    #   -H "x-goog-api-key: $GEMINI_API_KEY" \
    #   -H 'Content-Type: application/json' \
    #   -X POST \
    #   -d '{
    #     "contents": [
    #       {
    #         "parts": [
    #           {
    #             "text": "Explain how AI works in a few words"
    #           }
    #         ]
    #       }
    #     ]
    #   }'

    payload = {"contents": [{"parts": [{"text": user_input}]}]}

    requests.post(
        API_URL,
        json=payload,
        headers={
            "x-goog-api-key": API_KEY,
            "Content-Type": "application/json",
        },
    )

    pass


def main():
    # print("Hello from essentials!")

    user_input = input("What should the post be about?")

    x_post = generate_x_post(user_input)

    print("Generated Post:")
    print(x_post)


if __name__ == "__main__":
    main()
