from common.config import SOURCE_FOLDER, WEB_REPO_URL, API_REPO_URL, ENDPOINTS_FOLDER, CALLERS_FOLDER
from data_gather.callers_builder import build_api_caller_dictionary
from data_gather.endpoints_builder import build_api_endpoints_dictionary
from common.repo_donwloader import download_repo
from visualization.graph_builder import build_graph, draw_graph

download_repo(SOURCE_FOLDER,'zeeguu_web', WEB_REPO_URL)
download_repo(SOURCE_FOLDER, 'zeeguu_api', API_REPO_URL)


# Data gather
endpoints_dict = build_api_endpoints_dictionary(ENDPOINTS_FOLDER)
caller_dict = build_api_caller_dictionary(CALLERS_FOLDER)

# Visualize node and edges

graph = build_graph(endpoints_dict, caller_dict)
draw_graph(graph)