import os
from git import Repo

def download_repo(target_folder, repo_url):
    if not os.path.exists(target_folder):
        Repo.clone_from(repo_url, target_folder)