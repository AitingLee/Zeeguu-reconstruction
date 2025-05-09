import json
import os
import re
from data_gather.helper import read_file_lines
from pathlib import Path
from common.config import WEB_SRC_FOLDER, TARGET_FOLDERS


def extract_api_var_name(file_path: str):
    lines = read_file_lines(file_path)
    api_var_pattern = re.compile(r"const\s+([a-zA-Z_$][\w$]*)\s*=\s*useContext\(APIContext\);?")
    for line in lines:
        match = api_var_pattern.search(line)
        if match:
            return match.group(1)
    return None

def extract_usage_from_js_files(file_path: str, api_var_name) -> list:
    lines = read_file_lines(file_path)
    extracted_usage_list = []
    usage_pattern = re.compile(rf"{re.escape(api_var_name)}\.([a-zA-Z_$][\w$]*)\s*\(")
    for line in lines:
        for usage_match in usage_pattern.finditer(line):
            function_name = usage_match.group(1)
            if function_name not in extracted_usage_list:
                extracted_usage_list.append(function_name)
    return extracted_usage_list


def build_usage_list(
        endpoints_dict: dict,
        caller_dict: dict
) -> list:

    result_list = []

    for folder_name in TARGET_FOLDERS:
        folder_path_str = os.path.join(WEB_SRC_FOLDER, folder_name) + '/'
        files = Path(folder_path_str).rglob('*.js')

        for file_obj in files:
            file_path = str(file_obj)
            api_var_name = extract_api_var_name(file_path)
            if not api_var_name:
                continue
            usage_list = extract_usage_from_js_files(file_path, api_var_name)
            for js_function_name_usage in usage_list:
                if js_function_name_usage in caller_dict:
                    api_endpoint_string = caller_dict[js_function_name_usage]
                    if api_endpoint_string in endpoints_dict:
                        api_wrapper_file = endpoints_dict[api_endpoint_string]
                        result_list.append((folder_name, api_wrapper_file))
    return result_list