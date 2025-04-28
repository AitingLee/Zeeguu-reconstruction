import re
from pathlib import Path

ignore_files = ['Zeeguu_API', 'classDef']
calling_functions = ['_post', '_appendSessionToUrl', '_getPlainText', '_getJSON', 'apiPost']

def relevant_module(module_name):
    if  module_name in ignore_files:
        return False
    return True


def extract_endpoints_from_file(file_path) -> list:
    endpoints = []
    inside_call = False

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                # Check if match 'this.baseAPIurl + \{endpoint}' pattern
                match_baseapi = re.search(r'this\.baseAPIurl\s*\+\s*`([^`]*)`', line)
                if match_baseapi:
                    endpoint = match_baseapi.group(1)
                    endpoints.append(endpoint)
                    continue

                # Check if match 'this.calling_function + \{endpoint}' pattern
                if not inside_call:
                    for func in calling_functions:
                        pattern = rf'this\.{func}\s*\('
                        if re.search(pattern, line):
                            inside_call = True

                if inside_call:
                    match = re.search(r'[`\'"]([^`\'"]+)[`\'"]', line)
                    if match:
                        endpoint = match.group(1)
                        endpoints.append(endpoint)
                        inside_call = False
                        continue
    except FileNotFoundError:
        print(f"File {file_path} not found")

    return endpoints

def module_name_from_file_path(code_root_folder, full_path):
    file_name = full_path[len(code_root_folder):]
    file_name = file_name.replace("/", ".")
    file_name = file_name.replace(".js", "")
    return file_name

def build_api_caller_dictionary(endpoints_folder_path) -> dict:
    files = Path(endpoints_folder_path).rglob('*.js')
    caller_dictionary = {}
    for file in files:
        file_path = str(file)
        source_module = module_name_from_file_path(endpoints_folder_path, file_path)
        if not relevant_module(source_module):
            continue
        single_file_endpoints = extract_endpoints_from_file(file_path)
        for endpoint in single_file_endpoints:
            caller_dictionary[endpoint] = source_module
    return caller_dictionary