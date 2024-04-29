import os
import pandas as pd
import numpy as np
import re
import shutil

def count_star_systems(directory_path):
    # List to hold the file names and star system counts
    star_counts = []

    # Iterate over all files in the directory
    for filename in os.listdir(directory_path):
        if filename.endswith(".csv"):
            # Full path to the file
            file_path = os.path.join(directory_path, filename)
            try:
                with open(file_path, 'r') as file:
                    star_system_count = 0
                    for line in file:
                        # Check if the line starts with 'system,' and has exactly four commas
                        if line.startswith('system,') or line.startswith('"system",'):
                            star_system_count += 1
                    # Append the results to the list
                    star_counts.append((filename, star_system_count))
            except Exception as e:
                print(f"Error reading file {filename}: {e}")

    # Create a DataFrame from the list
    df = pd.DataFrame(star_counts, columns=['File Name', 'Number of Star Systems'])
    return df

def extract_series_name(file_name):
    pattern = re.compile(r'(\s\d+)')
    # Remove numbers and leading/trailing whitespace or special characters
    series_name = pattern.sub('', file_name).strip()
    return series_name

def generate_series_info(df):
    df['Series Name'] = df['File Name'].apply(extract_series_name)
    
    # Group by 'Series Name' and aggregate the data
    series_info = df.groupby('Series Name').agg(
        Number_of_Maps=('Number of Star Systems', 'size'),
        P0th_Percentile=('Number of Star Systems', lambda x: x.quantile(0.0)),
        P25th_Percentile=('Number of Star Systems', lambda x: x.quantile(0.25)),
        P50th_Percentile=('Number of Star Systems', lambda x: x.quantile(0.50)), # This is the median
        P75th_Percentile=('Number of Star Systems', lambda x: x.quantile(0.75)),
        P100th_Percentile=('Number of Star Systems', lambda x: x.quantile(1.0)) # This is the max
    ).reset_index()
    
    return series_info

def whitelist_maps(star_system_df, series_info_df, source_dir, archive_dir):
    # Ensure the archive directory exists
    if not os.path.exists(archive_dir):
        os.makedirs(archive_dir)

    # Add the series name to the star system DataFrame
    star_system_df['Series Name'] = star_system_df['File Name'].apply(extract_series_name)
    
    # Whitelist DataFrame to hold the names of files to be kept
    whitelist = pd.DataFrame()

    for _, row in series_info_df.iterrows():
        if row['Number_of_Maps'] <= 5:
            # Whitelist all maps in series with 5 or fewer maps
            series_maps = star_system_df[star_system_df['Series Name'] == row['Series Name']]
        else:
            # Whitelist maps in the specified percentiles
            percentiles = [row['P0th_Percentile'], row['P25th_Percentile'], row['P50th_Percentile'], 
                           row['P75th_Percentile'], row['P100th_Percentile']]
            series_maps = star_system_df[(star_system_df['Series Name'] == row['Series Name']) & 
                                         (star_system_df['Number of Star Systems'].isin(percentiles))]
        
        # Append the qualifying maps to the whitelist DataFrame
        whitelist = pd.concat([whitelist, series_maps], ignore_index=True)

    # Get the list of files to move to archive
    files_to_archive = star_system_df[~star_system_df['File Name'].isin(whitelist['File Name'])]

    # Move the non-whitelisted files
    for file_name in files_to_archive['File Name']:
        shutil.move(os.path.join(source_dir, file_name), os.path.join(archive_dir, file_name))

    print("Whitelisting complete. Non-whitelisted files moved to", archive_dir)


pd.set_option('display.max_rows', None)  # Shows all rows
pd.set_option('display.max_columns', None)  # Shows all columns
pd.set_option('display.width', None)  # Uses maximum width to display each column
pd.set_option('display.max_colwidth', None)  # Displays full content of each cell

source_dir = './Maps'  # Path where the original maps are stored
archive_dir = './Archived_Maps'  # Path where non-whitelisted maps will be moved
star_system_df = count_star_systems(source_dir)
#print(star_system_df)

series_info_df = generate_series_info(star_system_df)
print(series_info_df)

whitelist_maps(star_system_df, series_info_df, source_dir, archive_dir)