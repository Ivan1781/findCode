import requests
import re


def get_user(url):
    try:
        user = requests.get(url)
        return user
    except requests.RequestException as ex:
        print(ex)


class Checker:
    __MESSAGE = "This does not fit"
    __STATUS = 399


    def exist_user(self, url):
        user = get_user(url)
        if user.status_code > self.__STATUS:
            print(self.__MESSAGE)
            return False
        else:
            return True

    def empty_user(self, url):
        user = get_user(url)
        if user.text == 2:
            print(self.__MESSAGE)
            return False
        else:
            return True

    @property
    def message(self):
        return self.__MESSAGE

    @property
    def status(self):
        return self.__STATUS

# class Finder:
#     def get_all_repo_user(self, url):
#         repos = []
#         url = url
#         print(url)
#         get_repositories = exist_user()
#
#         if len(get_repositories.text) == 2:
#             print("It's empty user")
#             get_all_repo_user(build_url_user())
#
#         r = get_repositories.json()
#         for a in r:
#             if type(a) is str:
#                 print('-------------------------------------')
#                 print(r)
#                 print(a)
#                 print("-----------------000---------------")
#             else:
#                 name_of_repo = a.get('name')
#                 repos.append(name_of_repo)
#         return repos
