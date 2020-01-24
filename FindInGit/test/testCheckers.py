import pytest
import random
import requests
from main.requestGit import Checker
from main.requestGit import get_url


def test_get_exist_user():
    r = Checker()
    user = r.get_exist_user()
    print(user.status_code)
    assert user.status_code < r.status


