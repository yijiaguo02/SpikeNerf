#!/bin/bash
#SBATCH --time=70:00:00   # walltime
#SBATCH --ntasks=1   # number of processes (i.e. tasks)
#SBATCH --nodes=1   # number of nodes
#SBATCH --cpus-per-task=16 #of cpu cores per task
#SBATCH --gres=gpu:a100:1 #of gpu you need
##SBATCH --gres=gpu:1
##SBATCH --mem-per-cpu=80720M   # memory per CPU core
##SBATCH -w node1 #to submit to a specific node
##SBATCH -J "test"   # job name
##SBATCH -p internal
echo "Start time: `date`"
echo "SLURM_JOB_ID: $SLURM_JOB_ID"
echo "SLURM_NNODES: $SLURM_NNODES"
echo "SLURM_TASKS_PER_NODE: $SLURM_TASKS_PER_NODE"
echo "SLURM_NTASKS: $SLURM_NTASKS"
echo "SLURM_JOB_PARTITION: $SLURM_JOB_PARTITION"
#!/bin/bash
#python3 /home/huliwen/test/cut_spike.py
hostname
# >>> conda initialize >>>
# !! Contents within this block are managed by 'conda init' !!
__conda_setup="$('/home/huliwen/anaconda3/bin/conda' 'shell.bash' 'hook' 2> /dev/null)"
if [ $? -eq 0 ]; then
    eval "$__conda_setup"
else
    if [ -f "/home/huliwen/anaconda3/etc/profile.d/conda.sh" ]; then
        . "/home/huliwen/anaconda3/etc/profile.d/conda.sh"
    else
        export PATH="/home/huliwen/anaconda3/bin:$PATH"
    fi
fi
unset __conda_setup
conda activate nerf
export HDF5_USE_FILE_LOCKING=FALSE
pwd
nvidia-smi
echo $CUDA_VISIBLE_DEVICES
cd /home/huliwen/nerf-pytorch
#unzip spift_dark.zip
#tar -cvf phm_img.tar phm_img/
#scp /home/huliwen/denoise/Generative_spike_net.py ./
python run_nerf_mask.py --config configs/spike_lego_mask.txt