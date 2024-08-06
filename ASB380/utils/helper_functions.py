import os
import pandas as pd
from utils.lists_dictionaries import color_to_family


def format_strings(value):
    """
    places quotes around every column entry so the csv will format properly
    :param value: looks for white space or new line
    :return: 'example'
    """
    if value:
        return value.replace("\r", " ").replace("\n", "").strip()
    return None


def verify_row_count(collected_dfs, combined_df):
    """
    Verifies if the total number of rows in a list of DataFrames matches the number of rows in a combined DataFrame.

    :param collected_dfs: The original DataFrames.
    :param combined_df: The DataFrame resulting from combining 'collected_dfs'.

    Prints a message indicating whether the total row counts are equal and displays the counts.
    """
    total_rows = sum([len(df) for df in collected_dfs])
    new_rows = len(combined_df)

    if total_rows == new_rows:
        print(
            "Total rows match: ", "(original)", total_rows, "=", "(combined)", new_rows
        )
    else:
        print("Total rows do not match")
        print("original row count:", total_rows)
        print("new row count:", new_rows)


def process_excel_and_csv_files(dpath):
    """
    This function combines files in a directory based on their file type.
    :param dpath: (str) filepath to the directory with the files that need combined
    :return: a dataframe of all files in a directory of a given file type
    """
    data_files = [
        file for file in os.listdir(dpath) if file.lower().endswith((".xlsx", ".csv"))
    ]
    df_list = []
    total_rows = 0
    for file in data_files:
        file_path = os.path.join(dpath, file)
        if file.lower().endswith(".xlsx"):
            df = pd.read_excel(file_path, engine="openpyxl", header=0)
        elif file.lower().endswith(".csv"):
            df = pd.read_csv(file_path, header=0)
        else:
            continue

        df_list.append(df)
        rows = len(df.axes[0])
        total_rows += rows
    combined = pd.concat(df_list, ignore_index=True)
    fnames = [os.path.basename(file) for file in data_files]
    return combined, total_rows, fnames


def set_display_options():
    """
    sets the console display options
    :return: settings for viewing dataframes in console
    """
    pd.set_option("display.max_columns", None)
    pd.set_option("display.max_rows", 1500)
    pd.set_option("display.width", None)
    pd.set_option("display.max_colwidth", 20)


def convert_to_list(file_path):
    formatted_list = []
    with open(file_path, "r") as file:
        for line in file:
            stripped_line = line.strip()
            formatted_line = f"{stripped_line}"
            formatted_list.append(formatted_line)
    return formatted_list


def extract_unique(input_data: pd.DataFrame, column_name: str) -> set:
    """
    Extracts unique values from a specified column of a DataFrame.

    :param input_data: A pandas DataFrame containing the column.
    :param column_name: The name of the column to process.
    :return: A set of unique values.
    """
    unique_set = set()
    for item_string in input_data[column_name].dropna():
        for item in item_string.split(','):
            unique_set.add(item.strip().lower())
    return unique_set


def map_color_to_family(color_string: str) -> str:
    """
    Maps a comma-separated string of color names to their corresponding color families.

    :param color_string: A string containing color names separated by commas.
    :return: A string of corresponding color families separated by commas.
    """
    color_families = [color_to_family.get(color.strip(), 'Unknown') for color in color_string.split(',') if
                      color.strip()]
    return ', '.join(color_families)


