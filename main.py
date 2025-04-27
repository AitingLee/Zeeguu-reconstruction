import os

from abstract_graph_builder import dependencies_digraph, abstracted_to_top_level, draw_graph
from repo_donwloader import download_repo

CODE_ROOT_FOLDER = os.path.join(os.path.dirname(__file__), "source/zeeguu-web/")
REPO_URL = "https://github.com/zeeguu/web"

download_repo(CODE_ROOT_FOLDER, REPO_URL)

DG = dependencies_digraph(CODE_ROOT_FOLDER)
ADG = abstracted_to_top_level(DG, 2)

draw_graph(ADG, with_labels=True)
