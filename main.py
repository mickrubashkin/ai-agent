import os
from dotenv import load_dotenv
from google import genai



def main():
    print("Hello from ai-agent!")
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    model = "gemini-2.0-flash-001"
    question = "Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum."

    response = client.models.generate_content(model=model, contents=question)

    response_text = response.text
    prompt_tokens_count = response.usage_metadata.prompt_token_count
    response_tokens_count = response.usage_metadata.candidates_token_count

    print(response_text)
    print(f"Prompt tokens: {prompt_tokens_count}")
    print(f"Response tokens: {response_tokens_count}")



if __name__ == "__main__":
    main()
