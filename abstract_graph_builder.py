from pathlib import Path
import matplotlib.pyplot as plt
import networkx as nx

from dependency_extract import imports_from_file
from path_utils import module_name_from_file_path, top_level_package

# ignore_modules = ['App','i18n', 'assorted', 'pages', 'hooks', 'components', 'context', 'index', 'reportWebVital', 'utils', 'hooks']

def relevant_module(module_name):

    if module_name.endswith(".sc"):
        return False
    # for ignore_module in ignore_modules:
    #     if module_name.startswith(ignore_module):
    #         return False
    return True

def dependencies_digraph(code_root_folder):
    files = Path(code_root_folder).rglob("*.js")
    G = nx.DiGraph()
    for file in files:
        file_path = str(file)
        source_module = module_name_from_file_path(code_root_folder, file_path)
        if not relevant_module(source_module):
            continue
        if source_module not in G.nodes:
            G.add_node(source_module)
        for target_module in imports_from_file(code_root_folder, file_path):
            if relevant_module(target_module):
                G.add_edge(source_module, target_module)
    return G

def abstracted_to_top_level(G, depth=1):
    aG = nx.DiGraph()
    for each in G.edges():
        src = top_level_package(each[0], depth)
        dst = top_level_package(each[1], depth)

        if src != dst:
            # print("edge :", src, " | ", dst)
            aG.add_edge(src, dst)
            if src.startswith('api'):
                print(each[0], each[1])
    return aG

def draw_graph(G, size=(10,10), **kwargs):
    plt.figure(figsize=size)
    nx.draw(G, **kwargs)
    plt.show()
