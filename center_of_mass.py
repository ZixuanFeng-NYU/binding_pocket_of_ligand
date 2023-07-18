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



