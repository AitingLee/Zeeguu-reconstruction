import json

from common.config import SOURCE_FOLDER, WEB_REPO_URL, API_REPO_URL, ENDPOINTS_FOLDER, CALLERS_FOLDER
from data_gather.callers_builder import build_api_caller_dictionary
from data_gather.endpoints_builder import build_api_endpoints_dictionary
from common.repo_donwloader import download_repo
from data_gather.usage_scanner import build_usage_list
from visualization.graph_builder import visualize_with_graph, draw_graph

download_repo(SOURCE_FOLDER,'zeeguu_web', WEB_REPO_URL)
download_repo(SOURCE_FOLDER, 'zeeguu_api', API_REPO_URL)

# Data gather
endpoints_dict = build_api_endpoints_dictionary(ENDPOINTS_FOLDER)
caller_dict = build_api_caller_dictionary(CALLERS_FOLDER)
print(json.dumps(endpoints_dict))
print(json.dumps(caller_dict))

usage_list = build_usage_list(endpoints_dict, caller_dict)
print(json.dumps(caller_dict))

# Visualize node and edges
visualize_with_graph(usage_list, 1)
