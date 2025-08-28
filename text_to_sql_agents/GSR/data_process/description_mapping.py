import json
import os

import chardet
import pandas as pd

# 检测文件的编码
def detect_encoding(file_path):
    with open(file_path, 'rb') as f:
        result = chardet.detect(f.read(10000))  # Detect the first 10,000 bytes
    return result['encoding']

# Define a function that processes a single CSV file to generate two dictionaries
def generate_mappings_for_csv(file_path):
    print(file_path)
    # Detect the file's encoding and use it to read the CSV
    encoding = detect_encoding(file_path)
    df = pd.read_csv(file_path, encoding=encoding)

    # Create mapping relationships
    mapping = df.set_index('original_column_name')[['column_description', 'value_description']]

    # Create two dictionaries, one to map column_description, one to map value_description
    column_description_mapping = mapping['column_description'].to_dict()
    value_description_mapping = mapping['value_description'].to_dict()

    return column_description_mapping, value_description_mapping


# Iterate over all CSV files in the folder
def process_all_csv_files(root_folder):
    result = {}

    # Traverse all folders and files in the root folder using os.walk
    for foldername, subfolders, filenames in os.walk(root_folder):
        for filename in filenames:
            if filename.endswith('.csv'):  # CSV files only
                file_path = os.path.join(foldername, filename).replace("\\","/")

                database_name = file_path.rsplit('/',3)[1]
                # Generate two dictionaries for each CSV file
                column_desc_mapping, value_desc_mapping = generate_mappings_for_csv(file_path)

                database_file = database_name + '/' + filename.lower()
                # Save the dictionary to the result, using the filename as the key
                result[database_file] = {
                    'column_description_mapping': column_desc_mapping,
                    'value_description_mapping': value_desc_mapping
                }

    return result
