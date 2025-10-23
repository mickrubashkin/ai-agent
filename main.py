import os
from dotenv import load_dotenv
from google import genai
import sys



def main():
    print("Hello from ai-agent!")
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    model = "gemini-2.0-flash-001"

    if len(sys.argv) < 2:
        print("No prompt provided")
        sys.exit(1)

    question = sys.argv[1]

    response = client.models.generate_content(model=model, contents=question)

    response_text = response.text
    prompt_tokens_count = response.usage_metadata.prompt_token_count
    response_tokens_count = response.usage_metadata.candidates_token_count

    print(response_text)
    print(f"Prompt tokens: {prompt_tokens_count}")
    print(f"Response tokens: {response_tokens_count}")



if __name__ == "__main__":
    main()
