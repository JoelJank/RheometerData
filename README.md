Data contains all meassurements performed up until this point (11 February 2026)  
Data in the 9kPa folder contains csv data files with three consolidation forces (3kPa, 6kPa & 9kPa)  
The Folder Structure is as followed:  
```
RheometerData/
├── Data/
│   ├── Glass/
│   │   ├── 9kPa/
│   │   │   ├── w0per_150degree
│   │   │   ├── w0per_dried
│   │   │   ├── w0per_dried_3dprint
│   │   │   ├── w0per_dried_smallcup
│   │   │   ├── w0per_undried
│   │   │   ├── w10per_mixed
│   │   │   ├── w10per_unmixed
│   │   │   ├── w20per_mixed
│   │   │   └── wMultiple/
│   │   │       ├── w2.5per_unmixed
│   │   │       ├── w5per_unmixed
│   │   │       ├── w7.5per_unmixed
│   │   │       ├── w12.5per_unmixed
│   │   │       ├── w22.5per_unmixed
│   │   │       └── w25per_unmixed
│   │   └── 15kPa/
│   │       ├── w0per_dried
│   │       ├── w5per_dried
│   │       ├── w15per_dried
│   │       └── w25per_dried
│   ├── JSC/
│   │   ├── 9kPa/
│   │   │   ├── w0per_dried
│   │   │   ├── w0per_undried
│   │   │   ├── w10per_mixed
│   │   │   └── w20per_mixed
│   │   └── smallerkPa/
│   │       └── lowstress_dried
│   └── MGS/
│       ├── 9kPa/
│       │   ├── w0per_dried
│       │   ├── w0per_undried
│       │   ├── w10per_mixed
│       │   └── w20per_mixed
│       └── smallerkPa/
│           └── lowstress_dried
├── Scripts/
│   ├── Analysis
│   └── Excel_Manipulation
└── visualization
```


Every "final" folder contains the following files:  

- csv file named the same as the parent folder: Original data.   
- png files for the plots of the original data for the corresponding consolidation force from the original data  
- combined: all mohr coulomb graphs with different consolidation forces  
- mohr_coulomb.csv: Used data to create the combined plots  

The Scripts in Scripts/ and visualization are yet to be adjusted to the relative paths  
