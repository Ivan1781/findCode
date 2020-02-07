import os
import pandas as pd
import requests


# The task of the class is to count the stars of the repositories, the list of which lies in
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
        list_name_passw = []
        list_name_passw.append(name)
        list_name_passw.append(passw)
        self.__login_passwd = tuple(list_name_passw)
        return self.__login_passwd

    # The method returns a DataFrame that contains information from a file with a list of repositories
    def get_file_csv(self):
        try:
            df = pd.read_csv(os.path.abspath(self.__path_to_file), header=None, error_bad_lines=False)
        except Exception:
            return 'File not found'
        self.__length_of_column = df.shape[0]
        return df

    # The method receives a DataFrame, which is returned by the get_file_csv () method.
    # Next, the DataFrame is crawled. Requests are sent to the links contained in the dataFrame.
    # If the repository is empty, then the line is filled with the values 'Not', and
    # the value '-1' is set in the column 'stars'. All data is saved to the list __list_of_star = [].

    def __star_count(self, df):
        count = 0
        while count < self.__length_of_column:
            url = df[0][count]
            print(count)
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
                df.iloc[count] = {'0': 'Not', '1': 'Not', '2': 'Not'}
            finally:
                count += 1
        return self.__list_of_star

    # Record filled __list_of_star = [] containing the number
    # repository stars to the original csv file with repositories.
    def add_column_to_csv(self, df):
        # list_stars = self.__star_count(df)
        df['stars'] = self.__list_of_star
        try:
            df.to_csv(self.__path_to_file, index=False)
        except OSError:
            return 'Не удалось записать файл'
        return True

