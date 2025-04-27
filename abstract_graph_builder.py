from pathlib import Path
import networkx as nx

from dependency_extract import imports_from_file
from path_utils import module_name_from_file_path, top_level_package

def relevant_module(module_name):
    if "test" in module_name:
        return False
    if module_name.startswith("src") or module_name.startswith("../"):
        return True
    return False

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

        for target_module in imports_from_file(file_path):
            if relevant_module(target_module):
                G.add_edge(source_module, target_module)
    return G

def abstracted_to_top_level(G, depth=1):
    aG = nx.DiGraph()
    for each in G.edges():
        src = top_level_package(each[0], depth)
        dst = top_level_package(each[1], depth)

        if src != dst:
            aG.add_edge(src, dst)

    return aG

def draw_graph(G, size=(10,10), **kwargs):
    import matplotlib.pyplot as plt
    plt.figure(figsize=size)
    nx.draw(G, **kwargs)
    plt.show()
