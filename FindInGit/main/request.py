import requests
import re


class Checker:
    MESSAGE = "User does not exist"

    def exist_user(self, url):
        req = requests.get(url)
        if req.status_code > 399:
            print(self.MESSAGE)
        else:
            return req

# def empty_user():
# It's necessary to handle a case with empty repo

    def get_all_repo_user(url):
        repos = []
        url = url
        print(url)
        get_repositories = exist_user()

        if len(get_repositories.text) == 2:
            print("It's empty user")
            get_all_repo_user(build_url_user())

        r = get_repositories.json()
        for a in r:
            if type(a) is str:
                print('-------------------------------------')
                print(r)
                print(a)
                print("-----------------000---------------")
            else:
                name_of_repo = a.get('name')
                repos.append(name_of_repo)
        return repos