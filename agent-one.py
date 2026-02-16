import re
from dotenv import load_dotenv
import os
import requests

load_dotenv()

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
MODEL_NAME = os.getenv("MODEL_NAME", "gemma3:4b-it-qat")


def call_llm(prompt: str) -> str:
    response = requests.post(
        f"{OLLAMA_BASE_URL}/api/generate",
        json={
            "model": MODEL_NAME,
            "prompt": prompt,
            "stream": False,
            "options": {
                "num_ctx": 4096,
                "temperature": 0.2,
                "num_predict": 200,
            },
        },
        timeout=300,
    )

    response.raise_for_status()
    data = response.json()

    if "response" not in data:
        raise ValueError(f"Unexpected API response: {data}")

    return data["response"].strip()


def get_temperature(city: str) -> float:
    """Fake tool"""
    print(f"Calling tool: get_temperature({city})")
    return 20.0


def main():
    user_input = input("Your question: ")

    agent_prompt = f"""
You are a helpful assistant.

You can use tools:
- get_temperature(city): Returns the current temperature of a city.

If you want to use a tool, output ONLY:

get_temperature: CITY_NAME

User question:
{user_input}
"""

    llm_response = call_llm(agent_prompt)

    # ----- TOOL DETECTION -----
    tool_match = re.match(r"^get_temperature:\s*(.+)$", llm_response)

    if tool_match:
        city = tool_match.group(1).strip()
        temperature = get_temperature(city)

        final_prompt = f"""
You are a helpful assistant.

User question:
{user_input}

Tool result:
The temperature in {city} is {temperature}°C.

Answer the user in a friendly way.
"""

        final_answer = call_llm(final_prompt)
        print("\nAI:", final_answer)
        return

    # ----- NO TOOL NEEDED -----
    print("\nAI:", llm_response)


if __name__ == "__main__":
    main()
