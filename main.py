import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

from prompts import system_prompt
from call_function import available_functions

from functions.get_file_content import get_file_content
from functions.get_files_info import get_files_info
from functions.run_python_file import run_python_file
from functions.write_file import write_file


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

    generate_content(client, messages, verbose)


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

    if not response.function_calls:
        print("Response: ", response.text)

    for function_call_part in response.function_calls:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
        function_call_result = call_function(function_call_part)

        if not function_call_result.parts[0].function_response.response:
            raise RuntimeError("Fatal: cannot continue")

        if verbose:
            print(f"-> {function_call_result.parts[0].function_response.response}")


def call_function(function_call_part, verbose=False):
    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")


    print(f" - Calling function: {function_call_part.name}")

    fn_dict = {
        'get_file_content': get_file_content,
        'get_files_info': get_files_info,
        'run_python_file': run_python_file,
        'write_file': write_file
    }

    function_name = function_call_part.name
    function_args = {
        **function_call_part.args,
        'working_directory': "./calculator",
    }

    if function_name not in fn_dict:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"}
                )
            ]
        )

    function_result = fn_dict[function_name](**function_args)

    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": function_result},
            )
        ],
    )


if __name__ == "__main__":
    main()
