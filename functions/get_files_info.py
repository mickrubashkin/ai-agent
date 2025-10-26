from genericpath import isfile
import os


def get_files_info(working_directory, directory="."):
    try:
        path = os.path.join(working_directory, directory)
        work_dir_path = os.path.abspath(working_directory)
        is_in_workdir = os.path.abspath(path).startswith(work_dir_path)

        if not is_in_workdir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        if not os.path.isdir(path):
            return f'Error: "{directory}" is not a directory'

        files_info = []
        dir_files = os.listdir(path)

        for file_name in dir_files:
            file_path = os.path.join(path, file_name)
            is_dir = os.path.isdir(file_path)
            file_size = calc_size(file_path)
            file_info = f"- {file_name}: file_size={file_size}bytes, is_dir={is_dir}"
            files_info.append(file_info)

        return "\n".join(files_info)

    except Exception as e:
        return f"Error: {e}"


def calc_size(path, size=0):
    if os.path.isfile(path):
        return os.path.getsize(path)

    total_size = size
    children = os.listdir(path)

    for child in children:
        child_path = os.path.join(path, child)
        if os.path.isfile(child_path):
            total_size += os.path.getsize(child_path)
        else:
            total_size += calc_size(child_path, size=total_size)

    return total_size
