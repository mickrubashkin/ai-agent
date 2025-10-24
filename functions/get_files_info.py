import os


def get_files_info(working_directory, directory="."):
    path = os.path.join(working_directory, directory)
    work_dir_path = os.path.abspath(working_directory)
    is_in_workdir = os.path.abspath(path).startswith(work_dir_path)

    if not is_in_workdir:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

    if not os.path.isdir(path):
        return f'Error: "{directory}" is not a directory'

    # Build and return a string representing the contents of the directory. It should use this format:
    # - README.md: file_size=1032 bytes, is_dir=False
    # - src: file_size=128 bytes, is_dir=True
    # - package.json: file_size=1234 bytes, is_dir=False
    print("Path: ", path)
    print("Path is inside workdir: ", is_in_workdir)
    print(os.listdir(path))

    return 'hey hey, maybe later'
