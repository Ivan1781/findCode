import os
import pandas as pd
import requests


# The task of the class is to count  the stars of the repositories, the list of which lies in
# the .csv file and add to this file a new column 'stars' containing the number of stars of
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

    # The get_user () method receives user login and password, then returns tuple
    # and saves it in the __login_passwd field. This is then required to send an authorized
    # request to gitHub.
    def get_user(self, name, passw):
        list_name_passw = [name, passw]
        self.__login_passwd = tuple(list_name_passw)

    # The method returns a DataFrame that contains information from a file with a list of repositories
    def get_file_csv(self):
        try:
            df = pd.read_csv(os.path.abspath(self.__path_to_file), error_bad_lines=False, header=None)
            self.__length_of_column = df.shape[0]
            return df
        except IOError:
            return -1

    # The method receives a DataFrame, which is returned by the get_file_csv () method.
    # Next, the DataFrame is crawled. Requests are sent to the links contained in the dataFrame.
    # If the repository is empty, then the line is filled with the values 'Not', and
    # the value '-1' is set in the column 'stars'. All data is saved to the list __list_of_star = [].

    def star_count(self, df):
        count = 0
        while count < self.__length_of_column:
            if df[0][count] == '0' or df[0][count] == 'nan':
                count += 1
                continue
            url = df[0][count]
            try:
                r = requests.get(url, auth=self.__login_passwd)
                if r.status_code == 404:
                    raise requests.RequestException
                elif r.status_code == 403:
                    break
                else:
                    jso = r.json()
                    star = jso.get('stargazers_count')
                    self.__list_of_star.append(star)
            except requests.RequestException:
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
            df.to_csv(self.__path_to_file, index=False, header=None)
            return True
        except IOError:
            return -1

