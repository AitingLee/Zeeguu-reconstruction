import re
from pathlib import Path
from data_gather.helper import read_file_lines, module_name_from_file_path, normalize_endpoint_string

def relevant_module(module_name: str) -> bool:
    return not module_name.startswith("__init")

def extract_global_constants(lines: list[str]) -> dict[str, str]:
    constants = {}
    pattern = r"^\s*([A-Z_][A-Z0-9_]*)\s*=\s*['\"]([^'\"]+)['\"]\s*(?:#.*)?$"
    for line in lines:
        match = re.match(pattern, line)
        if match:
            var_name = match.group(1)
            var_value = match.group(2)
            constants[var_name] = var_value
    return constants

def resolve_path_string(path_definition_str: str, constants_map: dict[str, str]) -> str | None:
    path_def_str_stripped = path_definition_str.strip()
    if path_def_str_stripped.startswith('f"') or path_def_str_stripped.startswith("f'"):
        f_string_content = path_def_str_stripped[2:-1]
        def replace_var(match_obj):
            var_name = match_obj.group(1)
            return constants_map.get(var_name, f"{{{var_name}}}")
        resolved_path = re.sub(r"\{([A-Z_][A-Z0-9_]*)\}", replace_var, f_string_content)
        return resolved_path
    elif path_def_str_stripped.startswith('"') or path_def_str_stripped.startswith("'"):
        if path_def_str_stripped.startswith('"""') and path_def_str_stripped.endswith('"""'):
            return path_def_str_stripped[3:-3].strip()
        elif path_def_str_stripped.startswith("'''") and path_def_str_stripped.endswith("'''"):
            return path_def_str_stripped[3:-3].strip()
        return path_def_str_stripped[1:-1]
    else:
        return None


def extract_route_definitions_from_file(file_path: str) -> list[str]:
    all_lines = read_file_lines(file_path)
    if not all_lines:
        return []

    constants = extract_global_constants(all_lines)
    defined_routes = []

    file_content = "\n".join(all_lines)
    route_decorator_pattern = re.compile(
        r"@api\.route\s*\(\s*"
        r"([fF]?(?:\"\"\"(?:.|\n)*?\"\"\"|'''(?:.|\n)*?'''|\"(?:\\.|[^\"\\])*\"|'(?:\\.|[^'\\])*'))"
    )

    for match in route_decorator_pattern.finditer(file_content):
        path_definition_argument = match.group(1)
        resolved_path = resolve_path_string(path_definition_argument, constants)

        if resolved_path is not None:
            normalized_endpoint = normalize_endpoint_string(resolved_path)
            if normalized_endpoint not in defined_routes:
                defined_routes.append(normalized_endpoint)

    return defined_routes


def build_api_endpoints_dictionary(folder_path: str) -> dict:
    file_suffix = '.py'
    base_path = Path(folder_path)
    files = base_path.rglob(f'*{file_suffix}')
    result_dictionary = {}

    for file_obj in files:
        file_path_str = str(file_obj)
        source_module = module_name_from_file_path(folder_path, file_path_str, file_suffix)
        if not relevant_module(source_module):
            continue
        endpoints_in_file = extract_route_definitions_from_file(file_path_str)

        for endpoint in endpoints_in_file:
            result_dictionary[endpoint] = source_module

    return result_dictionary
