import re
from pathlib import Path

def relevant_module(module_name):
    if module_name.startswith("__init"):
        return False
    return True

def extract_endpoints_from_line(line):
    pattern = r'@api\.route\("/([^"]+)", methods=\("([^"]+)",\)\)'
    match = re.search(pattern, line)
    if match:
        return match.group(1)
    else:
        return None

def extract_endpoints_from_file(file_path) -> list:
    endpoints = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                endpoint = extract_endpoints_from_line(line)
                if endpoint:
                    endpoints.append(endpoint)
    except FileNotFoundError:
        print(f"File {file_path} not found")
    return endpoints

def module_name_from_file_path(code_root_folder, full_path):
    file_name = full_path[len(code_root_folder):]
    file_name = file_name.replace("/", ".")
    file_name = file_name.replace(".py", "")
    return file_name

def build_api_endpoints_dictionary(endpoints_folder_path) -> dict:
    files = Path(endpoints_folder_path).rglob("*.py")
    endpoints_dictionary = {}
    for file in files:
        file_path = str(file)
        source_module = module_name_from_file_path(endpoints_folder_path, file_path)
        if not relevant_module(source_module):
            continue
        single_file_endpoints = extract_endpoints_from_file(file_path)
        for endpoint in single_file_endpoints:
            endpoints_dictionary[endpoint] = source_module
    return endpoints_dictionary