import re
from .helper import read_file_lines, scan_files_and_build_dictionary

def relevant_module(module_name):
    return not module_name.startswith("__init")

def extract_endpoints_from_line(line):
    pattern = r"@api\.route\(\s*['\"]\/([^'\"]+)['\"]"
    match = re.search(pattern, line)
    if match:
        return match.group(1)
    return None

def extract_endpoints_from_file(file_path):
    endpoints = []
    lines = read_file_lines(file_path)
    for line in lines:
        endpoint = extract_endpoints_from_line(line)
        if endpoint:
            endpoints.append(endpoint)
    return endpoints

def build_api_endpoints_dictionary(endpoints_folder_path):
    return scan_files_and_build_dictionary(
        folder_path=endpoints_folder_path,
        file_suffix='.py',
        relevant_func=relevant_module,
        extract_func=extract_endpoints_from_file
    )
