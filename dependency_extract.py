import re

from path_utils import path_restore, module_name_from_file_path

def import_from_line(line):
    try:
        # Match from "..." or from '...'
        match = re.search(r'from\s+["\'](.+?)["\']', line)
        if match:
            return match.group(1)

        # Match import "..." or import '...'
        match = re.search(r'^import\s+["\'](.+?)["\']', line)
        if match:
            return match.group(1)

        return None

    except Exception as e:
        print(f"Error in import line: {line}")
        return None

def imports_from_file(code_root_folder, file_path):
    imports = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                imported_module_raw = import_from_line(line.strip())
                if imported_module_raw:
                    restored_path = path_restore(imported_module_raw, file_path)
                    imported_module = module_name_from_file_path(code_root_folder, restored_path)
                    if imported_module != '':
                        imports.append(imported_module)
    except FileNotFoundError:
        print(f"File {file_path} not found")
    return imports

