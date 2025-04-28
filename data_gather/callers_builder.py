import re
from .helper import read_file_lines, scan_files_and_build_dictionary

ignore_files = ['Zeeguu_API', 'classDef']
calling_functions = ['_post', '_appendSessionToUrl', '_getPlainText', '_getJSON', 'apiPost']

def relevant_module(module_name):
    for ignore_file in ignore_files:
        if module_name.startswith(ignore_file):
            return False
    return True

def extract_endpoints_from_file(file_path):
    endpoints = []
    inside_call = False
    lines = read_file_lines(file_path)

    for line in lines:
        # Match baseAPIurl pattern
        match_baseapi = re.search(r'this\.baseAPIurl\s*\+\s*`([^`]*)`', line)
        if match_baseapi:
            endpoints.append(match_baseapi.group(1))
            continue

        # Detect API calling functions
        if not inside_call:
            for func in calling_functions:
                if re.search(rf'this\.{func}\s*\(', line):
                    inside_call = True
                    break

        if inside_call:
            match = re.search(r'[`\'"]([^`\'"]+)[`\'"]', line)
            if match:
                endpoints.append(match.group(1))
                inside_call = False

    return endpoints

def build_api_caller_dictionary(endpoints_folder_path):
    return scan_files_and_build_dictionary(
        folder_path=endpoints_folder_path,
        file_suffix='.js',
        relevant_func=relevant_module,
        extract_func=extract_endpoints_from_file
    )