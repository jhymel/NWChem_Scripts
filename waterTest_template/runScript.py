import os

home = os.getcwd()

runFiles = [f for f in os.listdir(os.path.join(home)) if f.endswith('.slurm')]

for f in runFiles:
	os.system('sbatch %s' % f)
