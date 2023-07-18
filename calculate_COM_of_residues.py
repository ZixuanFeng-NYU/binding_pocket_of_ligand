import numpy as np
from Bio.PDB import *
parser = PDBParser()
structure = parser.get_structure('ranked_0','ranked_0.pdb')
model = structure[0]
def center_of_mass(atoms):
    masses = np.array([atom.mass for atom in atoms])
    coordinates = np.array([atom.get_coord() for atom in atoms])
    center = np.average(coordinates, axis=0, weights=masses)
    return center
Residue_name=[]
Residue_id=[]
X=[]
Y=[]
Z=[]
for chain in model:
    #print(chain)
    for residue in chain:
        #print(residue)
        atoms = list(residue.get_atoms())
        com=center_of_mass(atoms)
        Residue_name.append(residue.get_resname())
        Residue_id.append(residue.id[1])
        X.append(com[0])
        Y.append(com[1])
        Z.append(com[2])
        #print(atoms)
        com = center_of_mass(atoms)
        #print(f'Residue {residue.get_resname()}{residue.id[1]} center of mass: {com}')
