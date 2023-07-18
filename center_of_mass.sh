#!/bin/bash

mkdir COM
for i in $(ls highest_XGB_pose)
do
        ~/pymol-2.5.4/run-pymol-2.5.4.bash python center_of_mass.py highest_XGB_pose/${i}/${i}_*.pdb
done
