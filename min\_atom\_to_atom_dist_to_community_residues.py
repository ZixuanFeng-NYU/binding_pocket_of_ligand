import math
import os
import pandas as pd
from Bio.PDB import PDBParser, Selection

def ligand_atoms_rename(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
    new_lines = []
    atom_num_dict = {}
    existed = []
    for line in lines:
        if line.startswith("ATOM"):
            atom_name = line[12:16].strip()
            if atom_name in existed:
                atom_num = atom_num_dict[atom_name] + 1
            else:
                atom_num = 1
                existed.append(atom_name)
            atom_num_dict[atom_name] = atom_num
            element = line[76:78].strip()
            new_atom_name = f"{element}{atom_num:d}".ljust(4)
            new_line = line[:12] + new_atom_name + line[16:]
            new_lines.append(new_line)
        else:
             new_lines.append(line)
    with open(os.path.splitext(filename)[0] + "_renamed.pdb", 'w') as f:
        f.writelines(new_lines)

def calculate_min_dis(pose_folder, community_dir):
    community_0_file = os.path.join(community_dir, 'community_0.pdb')
    community_3_file = os.path.join(community_dir, 'community_3.pdb')
    community_11_file = os.path.join(community_dir, 'community_11.pdb')
    poses=pose_folder+'/poses'
    output_top1pose = pd.read_csv(os.path.join(pose_folder, 'output_top1pose.csv'))
    atom_to_atom_min_dis = pd.DataFrame()
    col_names = []
    for community_file in [community_0_file,community_3_file,community_11_file]:
        community_id = community_file.split('/')[-1].split('.')[0].split('_')[-1]
        community = PDBParser().get_structure('community', community_file)
        community_atoms = Selection.unfold_entities(community, 'A')
        for community_residue in community.get_residues():
            residue_type=community_residue.get_resname()
            residue_id=community_residue.get_id()[1]
            residue=str(community_id)+'_'+str(residue_type)+str(residue_id)
            col_names.append(residue)
    print('col_names:',col_names)
    print('col_names len:',len(col_names))
    lig,poses_id=[],[]
    for i in output_top1pose['poses_id']:
        print(i)
        ligand=i.split('_')[0]
        lig.append(ligand)
        poses_id.append(i)
        pose_file = pose_folder+'/poses/'+i+'.pdb'
        ligand_atoms_rename(pose_file)
        pose_renamed=pose_folder+'/poses/'+i+'_renamed.pdb'
        pose = PDBParser().get_structure('pose', pose_renamed)
        pose_atoms = Selection.unfold_entities(pose, 'A')
        print(pose_atoms)
        all_community_min_distance=[]
        for community_file in [community_0_file,community_3_file,community_11_file]:
            community_id = community_file.split('/')[-1].split('.')[0].split('_')[-1]
            community = PDBParser().get_structure('community', community_file)
            community_atoms = Selection.unfold_entities(community, 'A')
            min_dists = []

            for community_residue in community.get_residues():
                residue_type=community_residue.get_resname()
                residue_id=community_residue.get_id()[1]
                residue=str(community_id)+'_'+str(residue_type)+str(residue_id)
                min_dist = float('inf')
                for community_atom in community_residue.get_atoms():
                    x1,y1,z1=community_atom.get_coord()
                    min_dist = float('inf')
                    for pose_atom in pose_atoms:
                        x2,y2,z2=pose_atom.get_coord()
                        dist = math.sqrt((x2 - x1)**2 + (y2 - y1)**2 + (z2 - z1)**2)
                        if dist < min_dist:
                            min_dist = dist
                min_dists.append(min_dist)

            all_community_min_distance.extend(min_dists)
        print("all_community_min_distance len:", len(all_community_min_distance))
        atom_to_atom_min_dis = atom_to_atom_min_dis.append(pd.Series(all_community_min_distance), ignore_index=True)
    
    atom_to_atom_min_dis.columns=col_names
    atom_to_atom_min_dis['lig']=lig
    atom_to_atom_min_dis['poses_id']=poses_id
    print(atom_to_atom_min_dis)
    return atom_to_atom_min_dis
