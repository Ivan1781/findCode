import os
import requests
import pandas as pd
import csv
from git import Repo
import logging
import sys
import argparse


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
        formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
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
        while count < self.__length_of_column:
            self.logger.info('Counting of stars was started')
            if df[0][count] == '0' or df[0][count] == 'nan':
                count += 1
                continue
            url = df[0][count]
            try:
                r = requests.get(url, auth=self.__login_passwd)
                if r.status_code == 404:
                    self.logger.warning('Status of question is 404')
                    raise requests.RequestException
                elif r.status_code == 403:
                    self.logger.warning('Status of question is 403. Request Limit Exceeded')
                    break
                else:
                    self.logger.info('The request is successful')
                    jso = r.json()
                    star = jso.get('stargazers_count')
                    self.__list_of_star.append(star)
            except requests.RequestException:
                self.logger.exception('Repository was not found')
                self.__list_of_star.append(-1)
                not_complete = {}
                for a in range(df.shape[1]):
                    not_complete[a] = 'Not'
                df.iloc[count] = not_complete
            finally:
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
    logging.info('Repositories download started')
    with open(os.path.abspath(path_file_csv), 'r', encoding='utf_8_sig') as file_repo:
        reader = csv.reader(file_repo)
        for row in reader:
            if 3 > int(row[len(row) - 1]) >= 0:
                url = transform_url(row[0])
                logging.info(f'url of downloading repo is {url}')
                name_repo = url.split('/')
                repo = name_repo.pop(len(name_repo) - 1)
                path1 = to_path + '/' + repo
                try:
                    os.mkdir(path1)
                    logging.warning(f'Download repo to {path1}')
                    repo = Repo.clone_from(url, path1)
                    logging.info(f'Repo {path1} was created')
                except Exception:
                    logging.exception('Dowload a repo failed')
                    pass
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
    return list_files


def main(path_to_file, user_name, user_passw, dir_name):
    star = Stargazer(path_to_file)
    star.get_user(user_name, user_passw)
    df = star.get_file_csv()
    star.star_count(df)
    star.add_column_to_csv(df)
    # dir_name = 'G://directory'
    download_repo(path_to_file, dir_name)
    garbage_deleter(dir_name)


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('path_to_file', nargs='?')
    parser.add_argument('user_name', nargs='?')
    parser.add_argument('user_passw', nargs='?')
    parser.add_argument('dir_name', nargs='?')
    return parser


if __name__ == '__main__':
    parser = create_parser()
    namespace = parser.parse_args(sys.argv[1:])
    main(namespace.path_to_file, namespace.user_name, namespace.user_passw, namespace.dir_name)
