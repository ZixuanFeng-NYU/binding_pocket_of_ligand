import pandas as pd
import os
import math
def distance(ligands_COM, protein_community_COM):
    for i in ligands_COM['ligand_id'].unique():
        print(i)
        x1=float(ligands_COM[ligands_COM['ligand_id'] == i]['X'].iloc[0])
        y1=float(ligands_COM[ligands_COM['ligand_id'] == i]['Y'].iloc[0])
        z1=float(ligands_COM[ligands_COM['ligand_id'] == i]['Z'].iloc[0])
        #print(x1.dtype)
        #print(x1,y1,z1)
        for j in protein_community_COM['community_id'].unique():
            x2=float(protein_community_COM[protein_community_COM['community_id'] == j]['X'].iloc[0])
            y2=float(protein_community_COM[protein_community_COM['community_id'] == j]['Y'].iloc[0])
            z2=float(protein_community_COM[protein_community_COM['community_id'] == j]['Z'].iloc[0])
            print(j)
            print(x2,y2,z2)
            dist=math.sqrt((x2 - x1)**2 + (y2 - y1)**2 + (z2 - z1)**2)
            col_name = 'dist_to_' + j
            ligands_COM.loc[ligands_COM['ligand_id'] == i, col_name]=dist
            print(dist)
    filtered_df = ligands_COM.filter(regex='dist_to_')
    filtered_df = filtered_df.applymap(float)
    min_cols=filtered_df.idxmin(axis=1)
    ligands_COM['binding_pocket']=min_cols.apply(lambda x: x.split('_')[-1])
    return ligands_COM
