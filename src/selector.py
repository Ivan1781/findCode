import logging
import logging.config
import os
import pandas as pd
import requests


# The task of the class is to count  the stars of the repositories, the list
# of which lies in the .csv file and add to this file a new # column containing
# the number of stars of the repository. We send the path to the constructor
# to the file where the links to the gitHub repositories are stored.
class Stargazer:
    __list_of_values = []
    __length_of_column = 0
    __path_to_file = 0
    __login_passwd = 0

    def __init__(self, path):
        self.__path_to_file = path
        logging.config.fileConfig(fname='logg_config.conf', disable_existing_loggers=False)
        self.logger = logging.getLogger('selectorLogger')
        self.logger.info('Instance of Stargazer is created')

    def list_of_star(self):
        return self.__list_of_values

    # The get_user() method receives user login and password, then returns tuple
    # and saves it in the __login_passwd field. This is then required
    # to send an authorized request to gitHub.
    def get_user(self, name, passw):
        list_name_passw = [name, passw]
        self.logger.info('user_name and password is defined')
        self.logger.info(f'your password is {passw}')
        self.__login_passwd = tuple(list_name_passw)

    # The method returns a DataFrame that contains information from a file with
    # a list of repositories
    def get_file_csv(self):
        try:
            df = pd.read_csv(os.path.abspath(self.__path_to_file),
                             error_bad_lines=False, header=None,
                             index_col=False)
            self.__length_of_column = df.shape[0]
            self.logger.info('The file is converted into data_frame')
            return df
        except IOError:
            self.logger.exception('The convertion failed')
            return -1

    # The method receives a DataFrame, which is returned by the get_file_csv ()
    # method. Next, the DataFrame is crawled. Requests are sent to the links
    # contained in the dataFrame. If the repository is empty, then the line is
    # filled with the values 'Not', and # the value '-1' is set in the column
    # 'stars'. All data is saved to the list __list_of_star = [].
    def star_count(self, df):
        key_name = input('Enter a key: ')
        count = 0
        r = 0
        self.logger.info(f'Collection of {key_name} is starting')
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
                    self.logger.warning('Status of question is 401 or 403. '
                                        'Server refuse to repspond')
                    raise requests.RequestException
                else:
                    self.logger.info('The request is successful')
                    jso = r.json()
                    if jso.get('parent'):
                        value_of_key = jso.get('parent').get(key_name)
                    else:
                        value_of_key = jso.get(key_name)
                    self.logger.info(f'This repo has {value_of_key} {key_name}')
                    self.__list_of_values.append(value_of_key)
            except requests.RequestException:
                if r.status_code == 404:
                    self.logger.exception('Repository was not found')
                    self.__list_of_values.append(-1)
                    not_complete = {}
                    for a in range(df.shape[1]):
                        not_complete[a] = 'Not'
                    df.iloc[count] = not_complete
                else:
                    break
            finally:
                self.logger.info(f'The {key_name} was added to list {self.__list_of_values}')
                count += 1

        d = self.__length_of_column - len(self.__list_of_values)
        while d > 0:
            self.__list_of_values.append(-2)
            d -= 1

    # Record filled __list_of_star = [] containing the number
    # repository stars to the original csv file with repositories.
    def add_column_to_csv(self, df):
        df[df.shape[1]] = self.__list_of_values
        try:
            self.logger.warning('Adding a new star column to the source file')
            df.to_csv(self.__path_to_file, index=False, header=None)
            self.logger.info(f'List of stars: {self.__list_of_values}')
            self.logger.info('Adding star column was successful')
            return True
        except IOError:
            self.logger.exception('Adding star column was failed')
            return -1


