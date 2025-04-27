import re

def import_from_line(line):
    try:
        match = re.search(r"^import(?:.*?)from\s+(['\"])(.+?)\1", line)
        if match and match.group(2):
            return match.group(2)

        match = re.search(r"^import\s+(?:\{\s*.*?\s*\})?\s*(?:,\s*)?\s*(\w+)?\s+from\s+(['\"])(.+?)\3", line)
        if match and match.group(3):
            return match.group(3)

        match = re.search(r"^import\s+(['\"])(.+?)\2", line)
        if match and match.group(2):
            return match.group(2)

        return None

    except Exception as e:
        print(f"Error in import line: {line}")
        return None

def imports_from_file(file_path):
    imports = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                imported_module = import_from_line(line.strip())
                if imported_module:
                    imports.append(imported_module)
    except FileNotFoundError:
        print(f"File {file_path} not found")
    return imports

def relevant_module(module_name):
    if "test" in module_name:
        return False
    if module_name.startswith("src") or module_name.startswith("../"):
        return True
    return False
