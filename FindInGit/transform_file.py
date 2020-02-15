import pandas as pd
import os
import logging


class FileTransformer:
    df = 0
    number_of_rows = 0

    def info_source_file(self, path_to_file):
        self.df = pd.read_csv(os.path.abspath(path_to_file), error_bad_lines=False, header=None, index_col=False)
        self.number_of_rows = self.df.shape[0]
        print(f'Your file contains {self.number_of_rows} rows')
        return self.number_of_rows

    def create_new_data_frame(self):
        print(f" It's necessary to cut the file.")
        index = input("Please, enter an index of begining row: ")
        index1 = input("Please, enter an index of ending row: ")
        if int(index) < self.number_of_rows and int(index1) < self.number_of_rows:
            new_df = self.df.iloc[int(index):int(index1)]
            return new_df

    def create_file_csv(self, data_fr):
        new_path_to_file = input("Enter a new path: ")
        if not os.path.exists(new_path_to_file):
            try:
                os.mkdir(new_path_to_file)
            except OSError:
                return -1
        logging.warning("To record the file.csv")
        new_path = os.path.join(new_path_to_file, 'newSource.csv')
        data_fr.to_csv(new_path, index=False, header=None)
        return new_path



