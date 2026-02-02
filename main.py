from google import genai
from dotenv import load_dotenv
import os
import json  # <--- 1. Import the json module

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def generate_x_post(topic: str) -> str:
    # 2. Parse the JSON file
    with open("post-examples.json", "r") as f:
        examples = json.load(f) # Use json.load instead of f.read()

    examples_str = ""
    
    # Now 'examples' is a list, and 'example' is a dictionary
    for i, example in enumerate(examples, 1):
        examples_str += f"""
        <example - {i}>
        <topic>
        {example["heading"]}
        </topic>
        
        <generated post>
        {example["body"]}
        </generated post>
        </example - {i}>
        """

    prompt = f"""
    You are an expert social media manager, and excel in creating engaging posts for X (formerly Twitter).
    
    Your task is to generate a post that is engaging, concise, and relevant to the topic provided by the user.
    
    Avoid using hashtags and lots of emojis. Focus on clarity and engagement.
    
    Keep the post short and focused, structure it using line breaks and empty lines to enhance readability.
    
    Here is the topic for the post: 
    
    <TOPIC>
    {topic}
    </TOPIC>


    Here are some examples of well-structured posts:
    
    <EXAMPLES>

    {examples_str}
    
    </EXAMPLES>
    
    Please use the tone, language, and structure from the examples above to create a post about the provided topic.
    """

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash", 
            contents=prompt
        )

        return response.text

    except Exception as e:
        return f"An error occurred: {e}"


def main():
    user_input = input("What should the post be about? ")

    x_post = generate_x_post(user_input)

    print("\nGenerated Post:")
    print("------------------------------------------------")
    print(x_post)
    print("------------------------------------------------")


if __name__ == "__main__":
    main()