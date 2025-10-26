import os


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
