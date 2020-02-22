import os
import re
import download_clean


languages = {'Python': ['.py', '.pyc', '.pyo', '.pyd', '.whl'],
             'Ruby': ['.rb', '.rbw'], 'Go': ['.go'],
             'Java': ['.java', '.j', '.jav'], 'JavaScript': ['.js'],
             'C': ['.c', '.h'], 'C++': ['.cpp', '.cc', '.cxx', '.c++', '.hh', '.hpp'],
             'C#': ['.cs'], 'PHP': ['.php', '.phps']
             }


def to_count_rows_in_file(path_to_file):
    with open(path_to_file, 'r', encoding='utf-8',  errors='ignore') as file:
        rows = file.readlines()
        numbers_of_rows = len(rows)
    return numbers_of_rows


def to_count_rows_in_repo(list_files):
    count_rows = 0
    for file in list_files:
        count_rows += to_count_rows_in_file(file)
    return count_rows


# The function counts the number of repository files
def numbers_of_files_repo(path_to_repo):
    return len(download_clean.get_list_of_files(path_to_repo))


# The function counts the number of project languages
def technologies_of_project(list_of_repo_file):
    langs_of_repo = set()
    for file in list_of_repo_file:
        parts_file = file.split('.')
        extension = '.' + parts_file[len(parts_file)-1]
        for lang in languages:
            if extension in languages.get(lang):
                langs_of_repo.add(lang)
            else:
                pass
    return len(langs_of_repo)