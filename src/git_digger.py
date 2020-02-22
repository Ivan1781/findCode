import getpass
import download_clean as dc
import selector as sel
import transform_file as tran


def main(number_requests=5000):
    path_to_file = input('Enter a path to file contains info about repos: ')
    trans = tran.FileTransformer()
    number_rows_file = trans.info_source_file(path_to_file)
    if number_rows_file > number_requests:
        new_df = trans.create_new_data_frame()
        path_to_file = trans.create_file_csv(new_df)
    dir_name = input('Enter a path to folder where repos will be saved: ')
    user_name = input('Enter gitHub user_login: ')
    user_passw = getpass.getpass('Enter gitHub user_password: ')
    star = sel.Stargazer(path_to_file)
    star.get_user(user_name, user_passw)
    df = star.get_file_csv()
    # ---------------------
    star.star_count(df)
    star.add_column_to_csv(df)
    # ---------------------
    download_repo = input('To download repos? : ')
    if download_repo == 'y':
        dc.download_repo(path_to_file, dir_name)
    else:
        pass
    print(dc.DataCollector.df)
    e = dc.DataCollector()
    dc.DataCollector.create_statist_file(dir_name)


if __name__ == '__main__':
    main()
