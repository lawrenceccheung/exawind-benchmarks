# AMR-Wind code performance

## Overview

The relevant code versions are
- AMR-Wind version: [26063277b57415e735274c0d366ff702ca14fc14](https://github.com/Exawind/amr-wind/commit/26063277b57415e735274c0d366ff702ca14fc14)
- OpenFAST version: [Release 4.02](https://github.com/OpenFAST/openfast/releases/tag/v4.0.2)

The job was run on an HPC cluster using 
| Job type        | Characteristic |
|---              |---  |
| Number of nodes | 8   |
| Number of CPUs  | 896 |
| Wall-time       | 23.3 hours|
| CPU-hours       | 20862     | 


Average time spent every iteration in
|Category| Time [s]|
|---            | --- |
|Pre-processing | 0.135061|
|Solve          | 1.214|
|Post-processing| 0.0937338|
|**Total**      | 1.44281 |

## Log file
**Header**

```
==============================================================================
                AMR-Wind (https://github.com/exawind/amr-wind)

  AMR-Wind version :: v3.4.0-16-g26063277
  AMR-Wind Git SHA :: 26063277b57415e735274c0d366ff702ca14fc14
  AMReX version    :: 25.02-23-g06b4a5b105f5

  Exec. time       :: Tue Mar 11 12:19:32 2025
  Build time       :: Mar 11 2025 12:12:38
  C++ compiler     :: GNU 12.1.0

  MPI              :: ON    (Num. ranks = 896)
  GPU              :: OFF
  OpenMP           :: OFF

  Enabled third-party libraries: 
    NetCDF    4.9.2
    OpenFAST  

           This software is released under the BSD 3-clause license.           
 See https://github.com/Exawind/amr-wind/blob/development/LICENSE for details. 
------------------------------------------------------------------------------
```

**Footer**
```
Time spent in InitData():    16.40593849
Time spent in Evolve():      83821.48584
```