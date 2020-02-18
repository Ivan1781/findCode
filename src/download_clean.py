import csv
import logging
import os
from git import Repo

# The function transforms api url in normal view.
# The function is necessary for downloading repository
# with def download_repo(...)
def transform_url(url):
    url = url.split('/')
    url.pop(2)
    url.insert(2, 'github.com')
    url.pop(3)
    url = '/'.join(url)
    return url


# The function downloads a repository. The first argument is a path to file .csv
# contains repository references. The second argument is a path to directory in which
# repository will be downloaded. If the path is missing then it will be created.
# After ending of downloading the garbage deleter starts and deletes everything
# unnecessary files
def download_repo(path_file_csv, to_path):
    logging.basicConfig(level=logging.INFO)
    logging.info('Repositories download started')
    if not os.path.exists(to_path):
        try:
            os.mkdir(to_path)
            logging.info(f'The {to_path} directory was created')
        except OSError:
            logging.exception('Path to directory is not correct')
    with open(os.path.abspath(path_file_csv), 'r', encoding='utf_8_sig') \
            as file_repo:
        reader = csv.reader(file_repo)
        for row in reader:
            if 3 > int(row[len(row) - 1]) >= 0:
                url = transform_url(row[0])
                logging.info(f'url of downloading repo is {url}')
                name_repo = url.split('/')
                repo = name_repo.pop(len(name_repo) - 1)
                path_to_repo = os.path.join(to_path, repo)
                try:
                    os.mkdir(path_to_repo)
                    logging.warning(f'Download repo to {path_to_repo}')
                    repo = Repo.clone_from(url, path_to_repo)
                    logging.info(f'Repo {path_to_repo} was created')
                except Exception:
                    logging.exception('Downloading a repo failed')
                    pass
                garbage_deleter(path_to_repo)
            else:
                pass


# The function creates a list of files that are in a directory.
def get_list_of_files(dir_name):
    list_dir = os.listdir(os.path.join(dir_name))
    all_files = list()
    for entry in list_dir:
        full_path = os.path.join(dir_name, entry)
        if os.path.isdir(full_path):
            all_files += get_list_of_files(full_path)
        else:
            all_files.append(full_path)
    return all_files


# The function deletes everything file in directory. The path to directory
# is specified at first argument. The second argument is a tuple contains a file
# extensions which will be saved in a directory. The rest of files will
# be deleted.
def garbage_deleter(dir_name, languages=(
        '.py', '.java', '.cpp', '.js', '.php', '.cs', '.rb', '.go')):
    logging.basicConfig(level=logging.INFO)
    logging.info('delete unnecessary files')
    list_files = get_list_of_files(dir_name)
    list_files = filter(lambda s: not s.endswith(languages), list_files)
    for file in list_files:
        if os.path.exists(file):
            try:
                os.remove(file)
            except PermissionError:
                os.chmod(file, 0o777)
                os.remove(file)
    logging.info('Deleting is ended')
    return list_files