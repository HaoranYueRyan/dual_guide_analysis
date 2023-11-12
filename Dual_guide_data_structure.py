import os
import pandas as pd

def get_file_name(path):
    """
    Extracts the file name without extension from the given path.
    """
    _, file_name = os.path.split(path)
    file_name_without_extension, _ = os.path.splitext(file_name)
    return file_name_without_extension

def filter_data(df):
    """
    Filters a DataFrame based on 'gRNA-ID_x' and 'gRNA-ID_y' values.
    Processes the DataFrame and returns a new filtered DataFrame.
    """
    # Check if 'gRNA-ID_x' contains '.', if so, remove the last two characters from both 'gRNA-ID_x' and 'gRNA-ID_y'
    if df['gRNA-ID_x'].astype(str).str.contains('.').any():
        df['gRNA-ID_x'] = df['gRNA-ID_x'].astype(str).str[:-2]
        df['gRNA-ID_y'] = df['gRNA-ID_y'].astype(str).str[:-2]
    else:
        raise ValueError('Error! gRNA-ID_x,gRNA-ID_y do not contain expected format.')

    # Split the DataFrame based on matching 'gRNA-ID_x' and 'gRNA-ID_y'
    df_same = df[df['gRNA-ID_x'] == df['gRNA-ID_y']]
    df_diff = df[df['gRNA-ID_x'] != df['gRNA-ID_y']]

    # Further process 'df_diff' if it's not empty
    if not df_diff.empty:
        # Split 'gRNA-ID_y' into 'CHR_y' and 'gRNA-ID_start_end_y', and then into 'gRNA-ID_start_y', 'gRNA-ID_end_y'
        df_diff[['CHR_y', 'gRNA-ID_start_end_y']] = df_diff['gRNA-ID_y'].str.split(":", expand=True)
        df_diff[['gRNA-ID_start_y', 'gRNA-ID_end_y']] = df_diff['gRNA-ID_start_end_y'].str.split("-", expand=True)

        # Keep rows where 'end_x' is less than 'gRNA-ID_start_y'
        df_diff = df_diff[df_diff['end_x'].astype(int) < df_diff['gRNA-ID_start_y'].astype(int)]

        # Concatenate the processed 'df_same' and 'df_diff'
        df = pd.concat([df_same, df_diff])

    unique_gRNA_ids = df['gRNA-ID_x'].unique().tolist()
    print(f"Unique gRNA-ID_x count: {len(unique_gRNA_ids)}")

    df_filtered_all = pd.DataFrame()
    for index, unique_id in enumerate(unique_gRNA_ids):
        df_temp = df[df['gRNA-ID_x'] == unique_id].reset_index(drop=True)
        df_temp['id'] = [f'uce5M{index+1}_p{i+1}' for i in range(len(df_temp))]
        df_filtered_all = pd.concat([df_filtered_all, df_temp], ignore_index=True)

    # Split 'gRNA-ID_x' into 'CHR', 'gRNA-ID_start_end', and then into 'gRNA-ID_start', 'gRNA-ID_end'
    df_filtered_all[['CHR', 'gRNA-ID_start_end']] = df_filtered_all['gRNA-ID_x'].str.split(":", expand=True)
    df_filtered_all[['gRNA-ID_start', 'gRNA-ID_end']] = df_filtered_all['gRNA-ID_start_end'].str.split("-", expand=True)

    # Adjust 'gRNA-ID_start' and 'gRNA-ID_end' values
    df_filtered_all['gRNA-ID_start'] = df_filtered_all['gRNA-ID_start'].astype(int) + 49
    df_filtered_all['gRNA-ID_end'] = df_filtered_all['gRNA-ID_end'].astype(int) - 50

    return df_filtered_all

def get_difference(df1, df2):
    """
    Returns a list of differences in 'gRNA-ID_start' between two DataFrames.
    """
    set_diff = set(df1['gRNA-ID_start']) - set(df2['start'])
    return list(set_diff)
