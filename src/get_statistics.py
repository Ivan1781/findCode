from src.download_clean import get_list_of_files
import re

languages = {'Python': ['.py', '.pyc', '.pyo', '.pyd', '.whl'],
             'Ruby': ['.rb', '.rbw'], 'Go': ['.go'],
             'Java': ['.java', '.j', '.jav'], 'JavaScript':['js'],
             'C': ['.c', '.h'], 'C++': ['.cpp', '.cc', '.cxx', '.c++', '.hh', '.hpp'],
             'C#': ['cs'], 'PHP': ['.php', '.phps']
             }


def to_count_rows_in_file(path_to_file):
    with open(path_to_file, 'r') as file:
        number_rows = 0
        while True:
            row = file.readline()
            row = row.lstrip()
            if len(row) == 0:
                break
            elif len(row) == 1:
                pass
            else:
                number_rows += 1
        return number_rows


def to_count_rows_in_repo(path_to_repo):
    all_files_repo = get_list_of_files(path_to_repo)
    count_rows = 0
    for file in all_files_repo:
        count_rows += to_count_rows_in_file(file)
    return count_rows


def numbers_of_files_repo(path_to_repo):
    return len(get_list_of_files(path_to_repo)) - 1


def technologies_of_project(list_of_repo_file):
    langs_of_repo = set()
    lang_pattern = r'\.[a-z]*'
    for file in list_of_repo_file:
        extended_file = re.search(lang_pattern, file)
        for lang in languages:
            if extended_file.group() in languages.get(lang):
                langs_of_repo.add(lang)
            else:
                pass
    return langs_of_repo