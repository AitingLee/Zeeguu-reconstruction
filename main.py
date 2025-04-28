from config import SOURCE_FOLDER, WEB_REPO_URL, API_REPO_URL, ENDPOINTS_FOLDER
from data_gather.endpoints_builder import build_api_endpoints_dictionary
from repo_donwloader import download_repo


download_repo(SOURCE_FOLDER,'zeeguu_web', WEB_REPO_URL)
download_repo(SOURCE_FOLDER, 'zeeguu_api', API_REPO_URL)

# Data gather
build_api_endpoints_dictionary(ENDPOINTS_FOLDER)

# Define node and edges


# Visualize