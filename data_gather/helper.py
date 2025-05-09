import re

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

def normalize_endpoint_string(endpoint_str: str) -> str:
    normalized_str = re.sub(r'<[^>]+>', r'${}', endpoint_str)
    normalized_str = re.sub(r'\$\{[^}]+\}', r'${}', normalized_str)
    normalized_str = normalized_str.split('?', 1)[0]
    if normalized_str.startswith('/'):
        normalized_str = normalized_str[1:]
    return normalized_str
