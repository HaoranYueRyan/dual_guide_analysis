import os
import pandas as pd


def create_directories(*paths):
    for path in paths:
        try:
            os.makedirs(path, exist_ok=True)
            print(f"Directory '{path}' created successfully.")
        except OSError as error:
            print(f"Directory '{path}' cannot be created: {error}")


def get_file_stem_and_extension(file_path):
    stem, extension = os.path.splitext(os.path.basename(file_path))
    return stem, extension


def read_csv(file_path):
    return pd.read_csv(file_path)


def calculate_intervals(df):
    df['start_50'] = df['start'] - 50
    df['start_30'] = df['start'] + 30
    df['end_30'] = df['end'] - 30
    df['end_50'] = df['end'] + 50
    return df


def merge_dataframes(df_left, df_right, suffixes=('_x', '_y'), on='chr'):
    merged_df = pd.merge(df_left, df_right, on=on, suffixes=suffixes, how='inner')
    return merged_df


def save_dataframe(df, directory, file_stem, suffix, extension):
    file_path = os.path.join(directory, f"{file_stem}{suffix}{extension}")
    df.to_csv(file_path, index=False)
    print(f"Saved: {file_path}")


def main(ori_list, fil_list, path_element_ori, path_check):
    create_directories(path_element_ori, path_check)

    for ori_file, fil_file in zip(ori_list, fil_list):
        ori_stem, ori_ext = get_file_stem_and_extension(ori_file)
        fil_stem, fil_ext = get_file_stem_and_extension(fil_file)

        if ori_ext == fil_ext:
            print(f"Processing original file: {ori_stem}, filter file: {fil_stem}")
            df_ori = read_csv(ori_file)
            df_filter = read_csv(fil_file)
            # Perform interval calculations and any other transformations needed
            df_ori = calculate_intervals(df_ori)
            # Example merge operation (you need to adjust the conditions and logic here)
            df_merged = merge_dataframes(df_ori, df_filter)

            # Save the processed dataframes
            save_dataframe(df_merged, path_check, ori_stem, '_processed', ori_ext)

        else:
            print(f"File extension mismatch between {ori_file} and {fil_file}")


# Example usage
if __name__ == "__main__":
    ori_files = ['path/to/original1.csv', 'path/to/original2.csv']
    fil_files = ['path/to/filter1.csv', 'path/to/filter2.csv']
    path_element_ori = 'path/to/output/ori'
    path_check = 'path/to/output/check'

    main(ori_files, fil_files, path_element_ori, path_check)
