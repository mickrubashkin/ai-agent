import os
from google.genai import types
from config import MAX_CHARS


def get_file_content(working_directory, file_path):
    try:
        working_directory_abs_path = os.path.abspath(working_directory)
        abs_file_path = os.path.join(working_directory_abs_path, file_path)

        if not abs_file_path.startswith(working_directory_abs_path):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(abs_file_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        with open(abs_file_path, "r") as file:
            file_content_string = file.read(MAX_CHARS)
            next_char = file.read(1)

        is_truncated = bool(next_char)

        if is_truncated:
            return f'{file_content_string}[...File "{file_path}" truncated at 10000 characters]'

        return file_content_string

    except Exception as e:
        return f"Error: {e}"


schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Read the contents of specified file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to file to read the contents from, relative to the working directory.",
            ),
        },
    ),
)
