import re
from pathlib import Path
from data_gather.helper import read_file_lines, normalize_endpoint_string

ignore_files = ['Zeeguu_API', 'classDef']
calling_functions = ['_post', '_appendSessionToUrl', '_getPlainText', '_getJSON', 'apiPost']

def extract_js_function_and_api_endpoint_pairs(file_path):
    lines = read_file_lines(file_path)
    if not lines:
        return []

    extracted_pairs = []
    current_js_function_name = None
    local_variable_definitions: dict[str, str] = {}

    func_def_pattern_method = re.compile(r'\.([a-zA-Z_$][\w$]*)\s*=\s*(?:async\s+)?function')
    var_assignment_pattern = re.compile(
        r"^\s*(?:let|const|var)\s+([a-zA-Z_$][\w$]*)\s*=\s*(([`'\"])(?:\\.|(?!\3).)*\3)\s*;?"
    )
    string_literal_content_pattern = re.compile(r"^[`'\"](.*)[`'\"]$", re.DOTALL)
    base_api_url_pattern = re.compile(r'this\.baseAPIurl\s*\+\s*`([^`]*)`')

    api_call_arg_pattern = re.compile(
         rf"this\.({'|'.join(map(re.escape, calling_functions))})\s*\(\s*(.*?)[,)]",
         re.DOTALL
    )

    for i in range(len(lines)):
        line_content = lines[i]

        # 1. Find api function
        match_func_def = func_def_pattern_method.search(line_content)
        if match_func_def:
            current_js_function_name = match_func_def.group(1)
            local_variable_definitions = {}
            continue
        if not current_js_function_name:
             continue

        # 2. Catch local variables
        match_var_assign = var_assignment_pattern.match(line_content)
        if match_var_assign:
            var_name = match_var_assign.group(1)
            raw_value_with_quotes = match_var_assign.group(2)
            local_variable_definitions[var_name] = raw_value_with_quotes

        # 3. Match `this.baseAPIurl + \`...\`` pattern
        match_baseapi = base_api_url_pattern.search(line_content)
        if match_baseapi:
            endpoint_content = match_baseapi.group(1).strip()
            if endpoint_content:
                normalized_endpoint = normalize_endpoint_string(endpoint_content)
                if current_js_function_name:
                     if (current_js_function_name, normalized_endpoint) not in extracted_pairs:
                          extracted_pairs.append((current_js_function_name, normalized_endpoint))

        # 4. Match `calling_functions` pattern
        combined_line = line_content
        if i + 1 < len(lines):
            combined_line += lines[i+1]
        match_api_call_arg = api_call_arg_pattern.search(combined_line)

        if match_api_call_arg and current_js_function_name:
            raw_arg = match_api_call_arg.group(2).strip()
            endpoint_to_normalize = None
            match_literal_content = string_literal_content_pattern.fullmatch(raw_arg)
            if match_literal_content:
                endpoint_to_normalize = match_literal_content.group(1)
            elif raw_arg in local_variable_definitions:
                raw_value_with_quotes = local_variable_definitions[raw_arg]
                match_stored_literal_content = string_literal_content_pattern.fullmatch(raw_value_with_quotes)
                if match_stored_literal_content:
                    endpoint_to_normalize = match_stored_literal_content.group(1)

            if endpoint_to_normalize is not None:
                normalized_endpoint = normalize_endpoint_string(endpoint_to_normalize)
                if (current_js_function_name, normalized_endpoint) not in extracted_pairs:
                    extracted_pairs.append((current_js_function_name, normalized_endpoint))

    return extracted_pairs

def build_api_caller_dictionary(endpoints_folder_path: str) -> dict:
    folder_path = endpoints_folder_path
    file_suffix = '.js'
    files = Path(folder_path).rglob(f'*{file_suffix}')
    result_dictionary = {}

    for file_obj in files:
        file_path_str = str(file_obj)
        extracted_pairs = extract_js_function_and_api_endpoint_pairs(file_path_str)
        for pair in extracted_pairs:
            result_dictionary[pair[0]] = pair[1]

    return result_dictionary
