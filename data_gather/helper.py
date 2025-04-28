import re
from pathlib import Path

def read_file_lines(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return [line.strip() for line in f]
    except FileNotFoundError:
        print(f"File {file_path} not found")
        return []

def module_name_from_file_path(code_root_folder, full_path, suffix_to_strip):
    file_name = full_path[len(code_root_folder):]
    file_name = file_name.replace("/", ".")
    file_name = file_name.replace("\\", ".")
    file_name = file_name.replace(suffix_to_strip, "")
    return file_name

def scan_files_and_build_dictionary(folder_path, file_suffix, relevant_func, extract_func):
    files = Path(folder_path).rglob(f'*{file_suffix}')
    result_dictionary = {}
    for file in files:
        file_path = str(file)
        source_module = module_name_from_file_path(folder_path, file_path, file_suffix)
        if not relevant_func(source_module):
            continue
        endpoints = extract_func(file_path)
        for endpoint in endpoints:
            result_dictionary[endpoint] = source_module
    return result_dictionary
