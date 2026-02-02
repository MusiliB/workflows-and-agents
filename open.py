import json
import os
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from tenacity import retry, stop_after_attempt, wait_exponential

load_dotenv()

# Configuration
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/api/generate")
# Using a slightly larger context window by default, but relying on BS4 to reduce input size
MODEL_NAME = os.getenv("MODEL_NAME", "gemma3:4b-it-qat") 

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
def get_ai_response(
    prompt: str, 
    model: str = MODEL_NAME, 
    ctx: int = 4096,
    temperature: float = 0.7
) -> str:
    """
    Sends a prompt to the Ollama API with retries logic using Tenacity.
    """
    try:
        response = requests.post(
            OLLAMA_BASE_URL,
            json={
                "model": model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "num_ctx": ctx,
                    "temperature": temperature
                },
            },
            timeout=120 # Always add timeouts to external API calls
        )
        response.raise_for_status()
        
        data = response.json()
        if "response" not in data:
            raise ValueError("Unexpected API response format")
            
        return data["response"]
        
    except requests.RequestException as e:
        print(f"LLM Connection Error: {e}")
        raise # Re-raise to trigger Tenacity retry

def get_website_text(url: str) -> str:
    """
    Fetches HTML and strips tags using BeautifulSoup BEFORE AI processing.
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style", "nav", "footer", "aside"]):
            script.decompose()

        # Get text
        text = soup.get_text(separator=' ')
        
        # Break into lines and remove leading and trailing space on each
        lines = (line.strip() for line in text.splitlines())
        # Break multi-headlines into a line each
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        # Drop blank lines
        text = '\n'.join(chunk for chunk in chunks if chunk)
        
        # Truncate if purely massive to save initial context (approx 15k chars)
        return text[:15000] 

    except requests.RequestException as e:
        print(f"Error fetching URL: {e}")
        return None

def summarize_content(content: str) -> str:
    # Note: We skipped the "Extract Core Content" AI step because BeautifulSoup 
    # did 90% of that work for free (faster + cheaper).
    
    response = get_ai_response(
        prompt=f"""
            You are an expert summarizer. 
            Analyze the following text and provide a concise summary of the main points.
            
            TEXT:
            {content}
            
            OUTPUT FORMAT:
            - Bullet points
            - Concise
        """,
        ctx=8192 # Give it room to think
    )
    return response

def generate_x_post(summary: str) -> str:
    # Loading JSON inside function is fine for CLI, but for a web app, load this globally once.
    try:
        with open("post-examples.json", "r") as f:
            examples = json.load(f)
    except FileNotFoundError:
        print("Warning: post-examples.json not found. Using zero-shot.")
        examples = []

    # Construct examples string dynamically
    examples_str = "\n".join([
        f"Example {i+1}:\nTopic: {ex['topic']}\nPost: {ex['post']}\n"
        for i, ex in enumerate(examples)
    ])

    prompt = f"""
        Act as an expert social media manager. Write a viral X (Twitter) post based on the summary below.
        
        Style Guidelines:
        - Concise and impactful.
        - Use line breaks for readability.
        - Minimal emojis (1-2 max).
        - No hashtags.
        - Adopt the tone of the examples below.

        SUMMARY:
        {summary}

        {f'STYLE EXAMPLES:{examples_str}' if examples else ''}

        GENERATED POST:
    """
    
    return get_ai_response(prompt, temperature=0.8) # Higher temp for creativity

def main():
    website_url = input("Website URL: ")
    
    print("---------")
    print("Fetching and cleaning website content (BeautifulSoup)...")
    clean_text = get_website_text(website_url)
    
    if not clean_text:
        print("Failed to retrieve content. Exiting.")
        return

    print(f"Successfully extracted {len(clean_text)} characters of text.")

    print("---------")
    print("Summarizing content...")
    try:
        summary = summarize_content(clean_text)
        print("\n--- Summary ---\n")
        print(summary)
    except Exception as e:
        print(f"Summarization failed: {e}")
        return

    print("---------")
    print("Generating X post...")
    try:
        x_post = generate_x_post(summary)
        print("\n--- Generated Post ---\n")
        print(x_post)
    except Exception as e:
        print(f"Generation failed: {e}")

if __name__ == "__main__":
    main()