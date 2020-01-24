import requests
import random
import pdb


# The function generates url
def get_url():
    names = ['Alex', 'John', 'Ivan', 'Petr', 'Nicol', 'Andr', 'Eugen']
    r_for_numb = random.randint(0, 100)
    r_for_name = random.randint(0, 6)
    pdb.set_trace()
    str_for_url = names.pop(r_for_name) + str(r_for_numb)
    url = 'https://api.github.com/users/' + str_for_url + '/repos'
    return url


# The function allows manually or automatically to receive an user
# If args is empty then calling the function that automatically creates user url
# Elif args has an value that is an url of user
def get_info_user(*args):
    if len(args) == 0:
        url = get_url()
        print(url)
        user = requests.get(url)
        pdb.set_trace()
        return user
    else:
        url = args[0]
        user1 = requests.get(url)
        pdb.set_trace()
        return user1


# The main class method get_exist_user returns URL of existing and not empty user.
class Checker:
    __MESSAGE = "Wrong object"
    __STATUS = 399

    def __init__(self):
        self.__user = get_info_user()

    def get_user(self):
        return self.__user

    # In case if it's necessary to define concrete URL manually
    def set_user(self, url):
        self.__user = get_info_user(url)

    # This is an auxiliary method for get_exist_user
    def __exist_user(self):
        if self.__user.status_code > self.__STATUS:
            print(self.__MESSAGE)
            return False
        else:
            return True

    # This is an auxiliary method for get_exist_user
    def __empty_user(self):
        if (not self.__exist_user()) or self.__user.text == 2:
            print(self.__MESSAGE)
            return False
        else:
            return True

    def get_exist_user(self):
        while not self.__exist_user:
            self.__user = get_info_user()
        return self.__user

    @property
    def message(self):
        return self.__MESSAGE

    @property
    def status(self):
        return self.__STATUS


# The class find and return file from user repositories
# class Finder:
#     def get_list_repo_user(self, url):
#         repos = []
#         user = get_info_user(url)
#
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


