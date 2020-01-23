import pytest
import random


# An aim this function is to generate url for test
def build_url_user():
    names = ['Alex', 'John', 'Ivan', 'Petr', 'Nicol', 'Andr', 'Eugen']
    r_for_numb = random.randint(0, 100)
    r_for_name = random.randint(0, 6)

    str_for_url = names.pop(r_for_name) + str(r_for_numb)
    url = 'https://api.github.com/users/' + str_for_url + '/repos'
    return url

def test_exist_user():
