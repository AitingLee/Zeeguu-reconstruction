import os
from git import Repo

def download_repo(root, folder, repo_url):
    target_folder = os.path.join(root, folder)
    if not os.path.exists(target_folder):
        Repo.clone_from(repo_url, target_folder)