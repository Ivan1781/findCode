import requests
import re


# create an url of a user
def exist_user(url):
    req = requests.get(url)
    if req.status_code > 399:
        message = "User does not exist"
        print(message)
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
            print("-----------------ХУЙ---------------")
        else:
            name_of_repo = a.get('name')
            repos.append(name_of_repo)
    return repos