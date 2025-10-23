import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types



def main():
    load_dotenv()

    args = sys.argv[1:]

    if not args:
        print("AI Code Assistant")
        print("\nUsage: uv main.py \"your prompt here\"")
        print("Example: uv main.py \"How do I build a calculator app?\"")
        sys.exit(1)

    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    user_prompt = " ".join(filter(lambda arg: arg[:2] != "--", args))
    flags = list(filter(lambda arg: arg.startswith("--"), args))
    is_verbose = "--verbose" in flags

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]



    response = generate_content(client, messages)
    prompt_tokens = response.usage_metadata.prompt_token_count
    response_tokens = response.usage_metadata.candidates_token_count
    response_text = response.text

    if is_verbose:
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {prompt_tokens}")
        print(f"Response tokens: {response_tokens}")

    print("Response:")
    print(response_text)



def generate_content(client, messages):
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
    )

    return response


if __name__ == "__main__":
    main()
