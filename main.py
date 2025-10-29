import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

from config import MAX_ITERS
from prompts import system_prompt
from call_function import available_functions, call_function


def main():
    load_dotenv()

    verbose = "--verbose" in sys.argv
    args = []
    for arg in sys.argv[1:]:
        if not arg.startswith("--"):
            args.append(arg)

    if not args:
        print("AI Code Assistant")
        print("\nUsage: uv main.py \"your prompt here\"")
        print("Example: uv main.py \"How do I build a calculator app?\"")
        sys.exit(1)

    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    user_prompt = " ".join(args)

    if verbose:
        print(f"User prompt: {user_prompt}")

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    for i in range(MAX_ITERS):
        try:
            response = generate_content(client, messages, verbose)
        except Exception as e:
            print(f"Error generating content.\n[ERROR] {type(e).__name__}: {e}")
        if response:
            print("Final response:")
            print(response)
            break

    print(f"Maximum of {MAX_ITERS} iterations reached.")
    sys.exit(1)


def generate_content(client, messages, verbose):
    model_name = "gemini-2.0-flash-001"

    response = client.models.generate_content(
        model=model_name,
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=system_prompt
        ),
    )

    if verbose:
        print("Prompt tokens:", response.usage_metadata.prompt_token_count)
        print("Response tokens:", response.usage_metadata.candidates_token_count)

    called_tool = False

    for candidate in response.candidates:
        messages.append(candidate.content)
        for part in candidate.content.parts:
            if part.function_call:
                result = call_function(part.function_call, verbose)
                messages.append(result)
                called_tool = True

    if called_tool:
        return None
    elif response.text:
        return response.text
    else:
        return None


if __name__ == "__main__":
    main()
