# Setting up the sinngle turbine NREL5MW case in AMR-Wind

**Contents**
- [Prerequisites](#prerequisites)
- [Step 1: create the run directory](#step-1-create-the-run-directory)
- [Step 2: download the openfast model](#step-2-download-the-openfast-model)
- [Step 3: edit the file locations](#step-3-edit-the-file-locations)
- [Step 4: submit the run](#step-4-submit-the-run)

## Prerequisites

1.  Download the benchmarks repository

	```bash
	$ git clone --recursive git@github.com:Exawind/exawind-benchmarks.git BENCHMARKDIR
	```
    
    
    Here the optional argument `BENCHMARKDIR` is the location where you'd like the 
    benchmark repository to be cloned.  If it not provided, then the repo will be cloned into `exawind-benchmarks` in the current directory.


2.  Run the [slightly convective ABL benchmark](https://github.com/Exawind/exawind-benchmarks/tree/main/amr-wind/atmospheric_boundary_layer/convective_abl_nrel5mw) case.

    The NREL5MW case depends on initial conditions and boundary
    condition data which is generated during that ABL benchmark case,
    so it needs to be run before the NREL5MW case can be run.

3.  Download the [AMR-Wind frontend](https://github.com/Exawind/amr-wind-frontend) tool.

	The AMR-Wind frontend tool has useful utilities which can be used
    for setting up the OpenFAST turbine model and postprocessing
    results.  It is available on github and can be downloaded via

	```bash
	$ git clone --recursive git@github.com:Exawind/amr-wind-frontend.git AMRWINDFEDIR
	```

    where `AMRWINDFEDIR` is the location you'd like the tool to be
    located.  For the basic use of frontend-tool, the usual python 3
    libraries (numpy, scipy, pandas, etc.) are required.

## Step 1: create the run directory

Prepare a location where this case can be run.  This will likely be a location on the HPC where larger jobs can be run, and where lots of data (many gigabytes) can be stored.  First create the directory: 

```bash
$ mkdir RUNDIR
```

Then copy the necessary input files into `RUNDIR`

```bash
$ cp BENCHMARKDIR/amr-wind/actuator_line/NREL5MW_ALM_BD/input_files/NREL5MW_ALM_BD_OFv402.inp RUNDIR
$ cp BENCHMARKDIR/amr-wind/actuator_line/NREL5MW_ALM_BD/input_files/avg_theta.dat RUNDIR
$ cp BENCHMARKDIR/amr-wind/actuator_line/NREL5MW_ALM_BD/setup/nrel5mw_v402.yaml RUNDIR
```

## Step 2: download the openfast model

By default, the NREL5MW files required for the single turbine simulation are not included with the benchmarking repository.  However, they can be easily downloaded using some provided utilities.  First navigate to the run directory:

```bash
$ cd RUNDIR
```

Then use the [`downloadOFmodel.py`](https://github.com/Exawind/amr-wind-frontend/blob/main/utilities/downloadOFmodel.py) to download all of the required turbine files.

```bash
$ AMRWINDFEDIR/utilities/downloadOFmodel.py nrel5mw_v402.yaml
```

The `downloadOFmodel.py` will pull the necessary files straight from the OpenFAST repo, ensure files are from the right OpenFAST version, and make edits to the OpenFAST parameters so that the turbine is correctly configured for this case.

**Note**: The `downloadOFmodel.py` utility will also try to compile the turbine controller library (`DISCON.dll`) as it downloads the files.  Make sure that any modules or compiler paths are properly loaded before calling the `downloadOFmodel.py` utility.  Ideally, the same c/c++/fortran compilers that were used to compile AMR-Wind and OpenFAST are used for the `DISCON.dll` library.

Then change the name of the directory to match what is used in the input file
```bash
$ mv NREL5MW_v402/ T0_NREL5MW_v402/
```

## Step 3: edit the file locations

There are two edits required to the input file `NREL5MW_ALM_BD_OFv402.inp` in order to properly refer to the right locations.  The first is the location of the restart file: 

```
io.restart_file                          = /gpfs/lcheung/HFM/exawind-benchmarks/Neutral_ABL/chk30000
```

The second is the location of the boundary I/O files: 

```
ABL.bndry_file                           = /gpfs/lcheung/HFM/exawind-benchmarks/convective_abl/bndry_file
```

In each of these lines, change the path to match the location where the precursor directory was run.

## Step 4: submit the run

On many HPC platforms, a submission script needs to used to launch the case.  For slurm based systems, a submit script like this `submit.sh` file is used:
```bash
#!/bin/bash
#SBATCH --nodes=8
#SBATCH --time=47:59:59        # Wall clock time (HH:MM:SS) - once the job exceeds this time, the job will be terminated (default is 5 minutes)
#SBATCH --job-name=NREL5MW # Name of job
#SBATCH --partition=batch      # partition/queue name: short or batch
#SBATCH --qos=normal           # Quality of Service: long, large, priority or normal 
export nodes=$SLURM_JOB_NUM_NODES

module purge
module load aue/gcc/12.1.0 aue/openmpi/4.1.6-gcc-12.1.0 aue/hdf5/1.14.2-gcc-12.1.0-openmpi-4.1.6 aue/netcdf-c/4.9.2-gcc-12.1.0-openmpi-4.1.6  aue/cmake/3.27.7 
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$NETCDF_ROOT/lib

export EXE=/projects/wind_uq/lcheung/AMRWindBuilds/hfm.20250211/amr-wind/build/amr_wind

# Number MPI processes to run on each node (a.k.a. PPN)
export cores=112
export ncpus=$((nodes * cores))
export OMP_PROC_BIND=spread 
export OMP_PLACES=threads

time mpiexec --bind-to core --npernode $cores --n $ncpus $EXE NREL5MW_ALM_BD_OFv402.inp 
```

Then, for slurm based queueing systems, submit the run with a command like:  
```
$ sbatch submit.sh
```