import os
from google.genai import types


def write_file(working_directory, file_path, content):
    try:
        abs_wd = os.path.abspath(working_directory)
        abs_file_path = os.path.join(abs_wd, file_path)

        if not abs_file_path.startswith(abs_wd):
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

        os.makedirs(os.path.dirname(abs_file_path), exist_ok=True)

        with open(abs_file_path, "w") as f:
            f.write(content)

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error: {e}"


schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Write or overwrite files (path to the file provided as argument) with the specified content (provided as a second argument), constrained to the working directory. If the file not exists, create it. If the file exists, override it with the provided content.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to write the content, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Content to write to the file",
            )
        },
    ),
)
