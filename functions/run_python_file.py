import os
import subprocess
from google.genai import types


def run_python_file(working_directory, file_path, args=[]):
    try:
        abs_wd = os.path.abspath(working_directory)
        abs_file_path = os.path.abspath(os.path.join(abs_wd, file_path))

        if not abs_file_path.startswith(abs_wd):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not os.path.exists(abs_file_path):
            return f'Error: File "{file_path}" not found.'

        if not file_path.endswith('.py'):
            return f'Error: "{file_path}" is not a Python file.'
    except Exception as e:
        return f"Error: {e}"

    try:
        result = subprocess.run(["python", abs_file_path] + args, capture_output=True, timeout=30)
        result_string = f"STDOUT: {result.stdout}\nSTDERR: {result.stderr}"

        if result.returncode != 0:
            result_string += f"\nProcess exited with code {result.returncode}"

        if result.stdout == '':
            result_string += "\nNo output produced."

        return result_string
    except Exception as e:
        f"Error: executing Python file: {e}"


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Execute Python files with optional arguments, constrained to the working directory, and return the output from the interpreter. Path to file for execution provided as argument. List of optional argumnets provided as a second argument, and is optional (default is empty list)",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to python file to execute, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="Optional arguments to pass to the Python file.",
                items=types.Schema(
                    type=types.Type.STRING,
                    description="Optional arguments to pass to the Python file.",
                    ),
            )
        },
    ),
)
