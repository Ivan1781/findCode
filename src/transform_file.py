import logging
import logging.config
import os
import pandas as pd


# The class contains functions for working with a file. A file may contain a
# large number of rows. For this reason, the file must be shortened.
class FileTransformer:
    df = 0
    number_of_rows = 0

    def __init__(self):
        logging.config.fileConfig(fname='logg_config.conf', disable_existing_loggers=False)
        self.logger = logging.getLogger('selectorLogger')

        # The method returns a number of rows files. The path to the file is
    # specified as a parameter.
    def info_source_file(self, path_to_file):
        self.df = pd.read_csv(os.path.abspath(path_to_file), error_bad_lines=False,
                              header=None, index_col=False)
        self.number_of_rows = self.df.shape[0]
        self.logger.info(f'Your file contains {self.number_of_rows} rows')
        return self.number_of_rows

    # The method creates a new data_frame from the source CSV file. The user enters
    # row numbers which are contain in the source file. Everything rows between those
    # rows will become a new data frame which is returned by method.
    def create_new_data_frame(self):
        self.logger.info(f" It's necessary to cut the file.")
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
            self.logger.exception("It's not correct values")

    # The method creates a new source csv file from pandas data_frame whose size is
    # satisfactory. For default a new file will be named as a 'newSource.csv' and will
    # be saved in a directory which is specified by user.
    def create_file_csv(self, data_fr, new_source_file='newSource.csv'):
        new_path_to_file = input("Enter a new path: ")
        if not os.path.exists(new_path_to_file):
            try:
                os.mkdir(new_path_to_file)
            except OSError:
                self.logger.exception("On this path it's not possible to create a folder")
        self.logger.warning("To record the file.csv")
        new_path = os.path.join(new_path_to_file, new_source_file)
        data_fr.to_csv(new_path, index=False, header=None)
        return new_path



