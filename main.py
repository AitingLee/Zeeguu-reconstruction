import os
from git import Repo

# download the source code
CODE_ROOT_FOLDER=os.path.join(os.path.dirname(__file__), "source/zeeguu-web/")

if not os.path.exists(CODE_ROOT_FOLDER):
  Repo.clone_from("https://github.com/zeeguu/web", CODE_ROOT_FOLDER)

# make sure a file path having the prefix
def file_path(file_name):
    return CODE_ROOT_FOLDER+file_name

_test_path = "src/landingPage/LandingPage.js"
test_file_path = file_path(_test_path)

assert (test_file_path == (os.path.join(os.path.dirname(__file__), "source/zeeguu-web/src/landingPage/LandingPage.js")))

# extracting a module name from a file name
def module_name_from_file_path(full_path):

    # e.g. ../core/model/user.py -> zeeguu.core.model.user
    file_name = full_path[len(CODE_ROOT_FOLDER):]
    file_name = file_name.replace("/",".")
    file_name = file_name.replace(".js","")
    return file_name

assert module_name_from_file_path(test_file_path) == 'src.landingPage.LandingPage'

import re

def import_from_line(line):
    try:
        # Match "from '...'" or "from \"...\""
        match = re.search(r"^import(?:.*?)from\s+(['\"])(.+?)\1", line)
        if match and match.group(2):
            return match.group(2)

        # Match "import ... from ..."
        match = re.search(r"^import\s+(?:\{\s*.*?\s*\})?\s*(?:,\s*)?\s*(\w+)?\s+from\s+(['\"])(.+?)\3", line)
        if match and match.group(3):
            return match.group(3)

        # Match "import '...'" Oor "import \"...\""
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

imported_modules = imports_from_file(test_file_path)

for module in imported_modules:
    print(module)

from pathlib import Path
import networkx as nx

def dependencies_graph(code_root_folder):
    files = Path(code_root_folder).rglob("*.js")

    G = nx.Graph()

    for file in files:
        file_path = str(file)

        module_name = module_name_from_file_path(file_path)
        if module_name not in G.nodes:
            print(module_name)
            G.add_node(module_name)
        for each in imports_from_file(file_path):
            G.add_edge(module_name, each)

    return G

import matplotlib.pyplot as plt

# a function to draw a graph
def draw_graph(G, size, **args):
    plt.figure(figsize=size)
    nx.draw(G, **args)
    plt.show()


def relevant_module(module_name):
  if "test" in module_name:
    return False
  print('relevant_module', module_name, module_name.startswith("src"))
  if module_name.startswith("src") or module_name.startswith("../"):
    return True


  return False

# However, if we think a bit more about it, we realize that a dependency graph
# is a directed graph (e.g. module A depends on m)
# with any kinds of graph either directed (nx.DiGraph) or
# non-directed (nx.Graph)

def dependencies_digraph(code_root_folder):
    files = Path(code_root_folder).rglob("*.js")

    G = nx.DiGraph()
    for file in files:
        file_path = str(file)

        source_module = module_name_from_file_path(file_path)
        if not relevant_module(source_module):
          continue

        if source_module not in G.nodes:
            print('add_node ', source_module)
            G.add_node(source_module)

        files = imports_from_file(file_path)
        print('target files = ', files)
        for target_module in files:
            if relevant_module(target_module):
              G.add_edge(source_module, target_module)
    return G



def top_level_package(module_name, depth=1):
    components = module_name.split(".")
    return ".".join(components[:depth])

assert (top_level_package("src.landingPage.LandingPage") == "src")
assert (top_level_package("src.landingPage.LandingPage", 2) == "src.landingPage")

def abstracted_to_top_level(G, depth=1):
    aG = nx.DiGraph()
    for each in G.edges():
        src = top_level_package(each[0], depth)
        dst = top_level_package(each[1], depth)

        if src != dst:
          print('add edge ', src, dst)
          aG.add_edge(src, dst)

    return aG

DG = dependencies_digraph(CODE_ROOT_FOLDER)
ADG = abstracted_to_top_level(DG, 2)
plt.figure(figsize=(10,10))
nx.draw(ADG, with_labels=True)
plt.show()