import pandas as pd
import hashlib


def _encrypt(data, algorithm):
    encoder = hashlib.new(algorithm)
    encoder.update(str(data).encode('utf-8'))
    return encoder.hexdigest()


class SpreadsheetHasher:

    def __init__(self):
        self._df = None

    def load_data(self, input_filename):
        if input_filename.endswith('.csv'):
            self._df = pd.read_csv(input_filename)
        elif input_filename.endswith('.xlsx'):
            self._df = pd.read_excel(input_filename)
        else:
            raise ValueError("Wrong format of data file")

    def drop_columns(self, columns_to_drop):
        self._df = self._df.drop(columns_to_drop, axis=1)

    def keep_selected_columns(self, columns_to_keep):
        self._df = self._df[columns_to_keep]

    def hash_column(self, column_name, new_column_name=None, algorithm='md5'):
        self._df[column_name] = self._df[column_name].apply(lambda x: _encrypt(x, algorithm))
        if new_column_name is not None:
            self._df.insert(0, new_column_name, self._df[column_name])#[new_column_name] = self._df[column_name]
            self._df = self._df.drop(column_name, axis=1)

    def save_data(self, output_filename, output_format='csv'):
        if output_format == 'csv':
            output_filename += ".csv"
            self._df.to_csv(output_filename, index=False, encoding='utf-8')
        elif output_format == 'xlsx':
            output_filename += ".xlsx"
            self._df.to_excel(output_filename, index=False, encoding='utf-8')
        else:
            raise ValueError("Not supported output format")


