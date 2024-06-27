#!/usr/bin/python3
import argparse
import requests
import tarfile
import os
import shutil
import tempfile

def recursive_chown(path, uid, gid):
    for dirpath, dirnames, filenames in os.walk(path):
        os.chown(dirpath, uid, gid)
        for filename in filenames:
            os.chown(os.path.join(dirpath, filename), uid, gid)

def get_folder_owner_and_group(folder_path):
    # Get the folder's status
    folder_stat = os.stat(folder_path)
    
    # Extract the UID and GID
    uid = folder_stat.st_uid
    gid = folder_stat.st_gid
    
    return uid, gid

def download_github_release(repo, tag, temp_dir):
    """
    Downloads a GitHub release tar.gz file.
    
    Args:
    repo (str): GitHub repository in the format 'owner/repo'
    tag (str): Release tag to download
    temp_dir (str): Path to temporary directory for storing the downloaded file
    
    Returns:
    str: Path to the downloaded file, or None if download fails
    """
    base_url = f"https://github.com/{repo}/archive/refs/tags/"
    download_url = f"{base_url}{tag}.tar.gz"
    
    try:
        response = requests.get(download_url)
        response.raise_for_status()
        
        # Create filename in the temporary directory
        filename = os.path.join(temp_dir, f"{repo.split('/')[-1]}-{tag}.tar.gz")
        with open(filename, 'wb') as file:
            file.write(response.content)
        
        print(f"Successfully downloaded: {filename}")
        return filename
    except requests.exceptions.RequestException as e:
        print(f"Error downloading the release: {e}")
        return None

def extract_tarfile(filename, extract_path):
    """
    Extracts the downloaded tar.gz file.
    
    Args:
    filename (str): Path to the downloaded tar.gz file
    extract_path (str): Path where the contents will be extracted
    
    Returns:
    bool: True if extraction is successful, False otherwise
    """
    try:
        with tarfile.open(filename, "r:gz") as tar:
            tar.extractall(path=extract_path)
        print(f"Successfully extracted: {filename}")
        return True
    except tarfile.TarError as e:
        print(f"Error extracting the tar.gz file: {e}")
        return False

def map_folders(extract_path, mappings):
    """
    Maps folders from the extracted content to specified destinations.
    
    Args:
    extract_path (str): Path where the tar.gz contents were extracted
    mappings (list): List of strings in the format 'source:destination'
    """
    for mapping in mappings:
        src, dest = mapping.split(':')
        # Construct full path for source
        src_path = os.path.join(extract_path, src)
        if os.path.exists(src_path):
            # Create destination directory if it doesn't exist
            if not os.path.exists(dest):
                os.makedirs(dest)
            # Move the source to destination
            shutil.copytree(src_path, dest, dirs_exist_ok=True)
            uid, gid = get_folder_owner_and_group(dest)
            # The script is usually execute in the container as root to allow host user has permission
            # to the files created do recursive chown to the destination path with the original uid/gid
            # of that folder
            recursive_chown(dest, uid, gid) 
            print(f"Moved {src_path} to {dest}")
        else:
            print(f"Source path {src_path} does not exist")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download, extract, and map folders from a GitHub release tar.gz file")
    parser.add_argument("--repo", "-r", help="GitHub repository in the format 'owner/repo'")
    parser.add_argument("--tag", "-t", help="Release tag to download")
    parser.add_argument("--map", "-m", action='append', help="Mapping in the format 'source:destination'. Can be provided multiple times.")
    parser.add_argument("--local-repo", "-l", action='store', help="Specify weather we want a local repo or not")
    args = parser.parse_args()
    
    if args.local_repo:
        if os.path.exists(args.local_repo):
            map_folders(args.local_repo, args.map)
            print("Local content pull successful")
            exit(0)
        else:
            print("Local path does not exist, terminating")
            exit(-1)

    with tempfile.TemporaryDirectory() as temp_dir:
        tar_filename = download_github_release(args.repo, args.tag, temp_dir)
        if tar_filename:
            # Extract the tar.gz into the same location
            # i.e.
            # Extract /tmp/tmp5w_d_x9g/ysyx-docs-content-0.0.1.tar.gz
            # into /tmp/tmp5w_d_x9g/ysyx-docs-content-0.0.1
            # which has the the structure
            # ysyx-docs-content-0.0.1
            # |-- en
            # `-- zh
            extract_path = os.path.join(temp_dir, f"{args.repo.split('/')[-1]}-{args.tag}")
            if extract_tarfile(tar_filename, temp_dir):
                if args.map:
                    map_folders(extract_path, args.map)
        print("Cleanup complete. Temporary directory will be automatically removed.")
