import csv
import getpass
import logging
import os
from git import Repo
import pandas as pd
import requests
from transform_file import FileTransformer


# The task of the class is to count  the stars of the repositories, the list of which lies in
# the .csv file and add to this file a new column containing the number of stars of
# the repository
# We send the path to the constructor to the file where the links to the gitHub repositories
# are stored.
class Stargazer:
    __list_of_star = []
    __length_of_column = 0
    __path_to_file = 0
    __login_passwd = 0

    def __init__(self, path):
        self.__path_to_file = path
        self.logger = logging.getLogger('STARGAZER')
        self.logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        handler.setLevel(logging.INFO)
        formatter = logging.Formatter('%(levelname)s : %(name)s : %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.info('Instance of Stargazer is created')

    def list_of_star(self):
        return self.__list_of_star 

    # The get_user() method receives user login and password, then returns tuple
    # and saves it in the __login_passwd field. This is then required to send an authorized
    # request to gitHub.
    def get_user(self, name, passw):
        list_name_passw = [name, passw]
        self.logger.info('user_name and password is defined')
        self.logger.info(f'your password is {passw}')
        self.__login_passwd = tuple(list_name_passw)

    # The method returns a DataFrame that contains information from a file with a list of repositories
    def get_file_csv(self):
        try:
            df = pd.read_csv(os.path.abspath(self.__path_to_file), error_bad_lines=False, header=None,
                             index_col=False)
            self.__length_of_column = df.shape[0]
            self.logger.info('The file is converted into data_frame')
            return df
        except IOError:
            self.logger.exception('The convertion failed')
            return -1

    # The method receives a DataFrame, which is returned by the get_file_csv () method.
    # Next, the DataFrame is crawled. Requests are sent to the links contained in the dataFrame.
    # If the repository is empty, then the line is filled with the values 'Not', and
    # the value '-1' is set in the column 'stars'. All data is saved to the list __list_of_star = [].
    def star_count(self, df):
        count = 0
        r = 0
        self.logger.info('Counting of stars is starting')
        while count < self.__length_of_column:
            if df[0][count] == '0' or df[0][count] == 'nan':
                count += 1
                continue
            url = df[0][count]
            try:
                self.logger.info(f'The request to {url}')
                r = requests.get(url, auth=self.__login_passwd)
                if r.status_code == 404:
                    self.logger.warning('Status of question is 404')
                    raise requests.RequestException
                elif r.status_code == 401 or r.status_code == 403:
                    self.logger.warning('Status of question is 401 or 403. Server refuse to repspond')
                    raise requests.RequestException
                else:
                    self.logger.info('The request is successful')
                    jso = r.json()
                    star = jso.get('stargazers_count')
                    self.logger.info(f'This repo has {star} stars')
                    self.__list_of_star.append(star)
            except requests.RequestException:
                if r.status_code == 404:
                    self.logger.exception('Repository was not found')
                    self.__list_of_star.append(-1)
                    not_complete = {}
                    for a in range(df.shape[1]):
                        not_complete[a] = 'Not'
                    df.iloc[count] = not_complete
                else:
                    break
            finally:
                self.logger.info(f'The star was added to list {self.__list_of_star}')
                count += 1

        d = self.__length_of_column - len(self.__list_of_star)
        while d > 0:
            self.__list_of_star.append(-2)
            d -= 1

    # Record filled __list_of_star = [] containing the number
    # repository stars to the original csv file with repositories.
    def add_column_to_csv(self, df):
        df[df.shape[1]] = self.__list_of_star
        try:
            self.logger.warning('Adding a new star column to the source file')
            df.to_csv(self.__path_to_file, index=False, header=None)
            self.logger.info(f'List of stars: {self.__list_of_star}')
            self.logger.info('Adding star column was successful')
            return True
        except IOError:
            self.logger.exception('Adding star column was failed')
            return -1


def transform_url(url):
    url = url.split('/')
    url.pop(2)
    url.insert(2, 'github.com')
    url.pop(3)
    url = '/'.join(url)
    return url


def download_repo(path_file_csv, to_path):
    logging.basicConfig(level=logging.INFO)
    logging.info('Repositories download started')
    if not os.path.exists(to_path):
        try:
            os.mkdir(to_path)
            logging.info(f'The {to_path} directory was created')
        except OSError:
            logging.exception('Path to directory is not correct')
    with open(os.path.abspath(path_file_csv), 'r', encoding='utf_8_sig') as file_repo:
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


def garbage_deleter(dir_name):
    logging.basicConfig(level=logging.INFO)
    logging.info('delete unnecessary files')
    list_files = get_list_of_files(dir_name)
    languages = ('.py', '.java', '.cpp', '.js', '.php', '.cs', '.rb', '.go')
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


def main():
    path_to_file = input('Enter a path to file contains info about repos: ')
    trans = FileTransformer()
    number_rows_file = trans.info_source_file(path_to_file)
    if number_rows_file > 5000:
        new_df = trans.create_new_data_frame()
        path_to_file = trans.create_file_csv(new_df)
        logging.warning("New file was created")
    dir_name = input('Enter a path to folder where repos will be saved: ')
    user_name = input('Enter gitHub user_login: ')
    user_passw = getpass.getpass('Enter gitHub user_password: ')
    star = Stargazer(path_to_file)
    star.get_user(user_name, user_passw)
    df = star.get_file_csv()
    star.star_count(df)
    star.add_column_to_csv(df)
    download_repo(path_to_file, dir_name)


if __name__ == '__main__':
    main()
