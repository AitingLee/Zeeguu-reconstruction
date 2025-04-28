from abstract_graph_builder import dependencies_digraph, abstracted_to_top_level, draw_graph
from config import SOURCE_FOLDER, WEB_REPO_URL, API_REPO_URL
from repo_donwloader import download_repo
import os

download_repo(SOURCE_FOLDER,'zeeguu_web', WEB_REPO_URL)
download_repo(SOURCE_FOLDER, 'zeeguu_api', API_REPO_URL)

DG = dependencies_digraph(os.path.join(SOURCE_FOLDER, 'zeeguu_web/src/'))
ADG = abstracted_to_top_level(DG, 1)

draw_graph(ADG, with_labels=True)