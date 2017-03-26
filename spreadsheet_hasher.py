import pandas as pd
import hashlib


def _encrypt(data, algorithm):
    '''hashes passed string with provided algorithm'''
    encoder = hashlib.new(algorithm)
    encoder.update(str(data).encode('utf-8'))
    return encoder.hexdigest()


class SpreadsheetHasher:
    '''Simple class that allows to quickly cut off some parts of spreadsheet, and hash
    vulnerable data one would like to anonymize. Works with basic file formats: csv, xlsx, encoded with utf-8.
    Hashing can be done with multiple, standard algorithms like: md5, sha1, sha224, sha256,
    sha384, and sha512'''

    def __init__(self):
        self._df = None

    def load_data(self, input_filename):
        '''loads spreadsheet, filename/path should contain file extension'''
        if input_filename.endswith('.csv'):
            self._df = pd.read_csv(input_filename)
        elif input_filename.endswith('.xlsx'):
            self._df = pd.read_excel(input_filename)
        else:
            raise ValueError("Not supported input format")

    def drop_columns(self, columns_to_drop):
        '''drop provided columns, arg can be single string or list of many string names'''
        self._df = self._df.drop(columns_to_drop, axis=1)

    def keep_selected_columns(self, columns_to_keep):
        '''drops all columns not contained in provided list of column names, can be single string in case of
        only one column selected'''
        self._df = self._df[columns_to_keep]

    def hash_column(self, column_name, new_column_name=None, algorithm='md5'):
        '''hashes content in selected column, column will be renamed as well if new_column_name is provided
        algorithm arg specifies hashing algorithm, default is md5, available: md5, sha1, sha224, sha256,
         sha384, and sha512'''
        self._df[column_name] = self._df[column_name].apply(lambda x: _encrypt(x, algorithm))
        if new_column_name is not None:
            self._df.insert(0, new_column_name, self._df[column_name])
            self._df = self._df.drop(column_name, axis=1)

    def save_data(self, output_filename, output_format='csv'):
        '''saves data to output_filename (do not provide extension in that argument), output_format can
        be specified in output_format arg, default csv, available: csv, xlsx'''
        if output_format == 'csv':
            output_filename += ".csv"
            self._df.to_csv(output_filename, index=False, encoding='utf-8')
        elif output_format == 'xlsx':
            output_filename += ".xlsx"
            self._df.to_excel(output_filename, index=False, encoding='utf-8')
        else:
            raise ValueError("Not supported output format")


