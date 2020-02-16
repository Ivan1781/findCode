import logging
import os
import pandas as pd


class FileTransformer:
    df = 0
    number_of_rows = 0

    def info_source_file(self, path_to_file):
        self.df = pd.read_csv(os.path.abspath(path_to_file), error_bad_lines=False,
                              header=None, index_col=False)
        self.number_of_rows = self.df.shape[0]
        logging.info(f'Your file contains {self.number_of_rows} rows')
        return self.number_of_rows

    def create_new_data_frame(self):
        logging.info(f" It's necessary to cut the file.")
        try:
            beginning_of_file = int(input("Please, enter an index of begining file row: "))
            ending_of_file = int(input("Please, enter an index of ending file row: "))
            if beginning_of_file < self.number_of_rows \
                    and ending_of_file < self.number_of_rows:
                new_df = self.df.iloc[int(beginning_of_file):int(ending_of_file)]
                return new_df
            else:
                self.create_new_data_frame()
        except ValueError:
            logging.exception("It's not correct values")


    def create_file_csv(self, data_fr, new_source_file='newSource.csv'):
        new_path_to_file = input("Enter a new path: ")
        if not os.path.exists(new_path_to_file):
            try:
                os.mkdir(new_path_to_file)
            except OSError:
                logging.exception("On this path it's not possible to create a folder")
        logging.warning("To record the file.csv")
        new_path = os.path.join(new_path_to_file, new_source_file)
        data_fr.to_csv(new_path, index=False, header=None)
        return new_path



