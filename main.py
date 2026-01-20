from dotenv import load_dotenv  # type: ignore
import requests
import os

load_dotenv()


API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"
API_KEY = os.getenv("GEMINI_API_KEY")

def generate_x_post(topic: str) -> str:
    prompt = f"""
    You are an expert social media manager, and excel in creating engaging posts for X (formerly Twitter).
    
    Your task is to generate a post that is engaging, concise, and relevant to the topic provided by the user.
    
    Avoid using hashtags and lots of emojis. Focus on clarity and engagement.
    
    Keep the post short and focused, structure it using line breaks and empty lines to enhance readability.
    
    Here is the topic for the post: 
    
    <TOPIC>
    {topic}
    </TOPIC>
    """

    payload = {"contents": [{"parts": [{"text": prompt}]}]}

    response = requests.post(
        API_URL,
        json=payload,
        headers={
            "x-goog-api-key": API_KEY,
            "Content-Type": "application/json",
        },
    )

    if response.status_code == 200:
        data = response.json()
        try:
            return data['candidates'][0]['content']['parts'][0]['text']
        except (KeyError, IndexError):
            return "Error parsing API response."
    else:
        return f"Error: API request failed with status code {response.status_code}"

def main():
    user_input = input("What should the post be about? ")
    
    x_post = generate_x_post(user_input)

    print("\nGenerated Post:")
    print("------------------------------------------------")
    print(x_post)
    print("------------------------------------------------")

if __name__ == "__main__":
    main()