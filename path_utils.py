def file_path(code_root_folder, file_name):
    return code_root_folder + file_name

def module_name_from_file_path(code_root_folder, full_path):
    file_name = full_path[len(code_root_folder):]
    file_name = file_name.replace("/", ".")
    file_name = file_name.replace(".js", "")
    return file_name

def top_level_package(module_name, depth=1):
    components = module_name.split(".")
    return ".".join(components[:depth])
