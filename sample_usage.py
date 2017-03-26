from spreadsheet_hasher import SpreadsheetHasher

column_to_hash = "user_login"
# data_columns_to_keep = ['user_login']
data_columns_to_drop = ['likes_spaghetti']
input_filename = "sample_input.csv"
output_filename = "sample_output"


def main():
    sh = SpreadsheetHasher()
    sh.load_data(input_filename) # note that loading data is required before any other work
    # sh.keep_selected_columns(data_columns_to_keep)
    sh.drop_columns(data_columns_to_drop)
    sh.hash_column(column_to_hash, new_column_name="ID", algorithm='sha224')
    sh.save_data(output_filename, output_format='csv')

main()