import pandas as pd
import numpy as np
import sys

def community(ligands_data, communities_data):
    # Define a function to calculate Euclidean distance
    def calculate_distance(row, communities):
        distances = np.sqrt((communities['X'] - row['X'])**2 +
                            (communities['Y'] - row['Y'])**2 +
                            (communities['Z'] - row['Z'])**2)
        min_index = np.argmin(distances)
        return communities.iloc[min_index]['community_id'], distances.iloc[min_index]

    # Apply distance calculation for each ligand
    ligands_data[['nearest_community', 'min_distance']] = ligands_data.apply(
        lambda row: pd.Series(calculate_distance(row, communities_data)), axis=1
    )
    return ligands_data


if __name__ == '__main__':
    # Read input CSV files
    ligands_file = sys.argv[1]
    communities_file = sys.argv[2]
    output_file = sys.argv[3]

    # Load data
    ligands_data = pd.read_csv(ligands_file)
    communities_data = pd.read_csv(communities_file)

    # Process data
    ligands_data = community(ligands_data, communities_data)

    # Save output to CSV
    ligands_data.to_csv(output_file, index=False)
