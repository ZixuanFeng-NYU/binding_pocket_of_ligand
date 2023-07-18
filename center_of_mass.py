import __main__
__main__.pymol_argv = [ 'pymol', '-qc']            #quiet and no GUI
import sys, time, os
import pymol

pymol.finish_launching()

##### Reading user input #####
spath = os.path.abspath(sys.argv[1])
filename = spath.split('/')[-1].split('.')[0]

##### Loading structures #####
pymol.cmd.load(spath, filename)
pymol.cmd.disable("all")
pymol.cmd.enable(filename)
pymol.cmd.centerofmass(filename)

##### Getting output in a file #####
output = pymol.cmd.centerofmass(filename)
sys.stdout = open('COM/'+filename+'.txt','w')
print ((filename), (output))

##### Quiting #####
pymol.cmd.quit()


\end{lstlisting}

\begin{lstlisting}[language=bash,breaklines,caption={center\_of\_mass.sh}(run it out of singularity)]
#!/bin/bash

mkdir COM
for i in $(ls highest_XGB_pose)
do
        ~/pymol-2.5.4/run-pymol-2.5.4.bash python center_of_mass.py highest_XGB_pose/${i}/${i}_*.pdb
done
