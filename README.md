# Reproduction of Data in [Cascarina (2023)](https://www.frontiersin.org/articles/10.3389/frma.2023.1215401/full)

This directory contains all necessary information and code to reproduce the data in [**Cascarina (2023),** ***Frontiers in Research Metrics and Analytics***](https://www.frontiersin.org/articles/10.3389/frma.2023.1215401/full). Below is a list of dependencies and associated version numbers used for testing and data analysis:

| Package | Version |
| ----------- | ----------- |
| Python | 3.7.15 | 
| Numpy | 1.21.5 |
| Scipy | 1.7.3 |
| Pandas | 1.3.5 |
| Matplotlib | 3.5.3 |
| Seaborn | 0.12.0 |
| Biopython | 1.79 |
| statsmodels | 0.13.2 |
| tqdm | 4.64.1 |

To reproduce figures and tables in the paper:
1. Download the required data from Figshare: https://figshare.com/articles/dataset/Pubmed_Author_Query_Results/24069258.
2. Download all files from this Github repository.
3. Extract necessary files from compressed folders (placing them in the same folder as the scripts). Please refer to the "License info" section at the bottom of this page for important licensing information regarding these files. Files downloaded from Figshare must also be extracted and placed in the same folder as the scripts and data downloaded from this repository.
4. Run the batch file called "SelfReferencing_Replication_Batch.bat" via command-line bash/terminal. Alternatively, each individual command in the batch file can be run independently via command-line.

## License info
All code in this directory is subject to the terms of the GPLv3 license (see LICENSE in this directory). If you use data, code, or information contained in this directory or the associated manuscript, please cite:

1. Cascarina, SM (2023). Self-referencing rates in biological disciplines. *Front. Res. Metr. Anal.* https://doi.org/10.3389/frma.2023.1215401

The "ranked-authors" database (file named "Table_1_Authors_career_2021_pubs_since_1788_wopp_extracted_202209b.tsv") was originally downloaded from https://elsevier.digitalcommonsdata.com/datasets/btchxktzyw and is subject to the terms of the [CC BY NC 3.0 license](https://creativecommons.org/licenses/by-nc/3.0/legalcode). If you use any part of the ranked-authors database, please cite:

1. Ioannidis, John PA (2022). “September 2022 data-update for "Updated science-wide author databases of standardized citation indicators"”, *Elsevier Data Repository*, V5, doi: https://doi.org/10.17632/btchxktzyw.5
2. Ioannidis JPA, Boyack KW, Baas J (2020). Updated science-wide author databases of standardized citation indicators. *PLOS Biology* 18(10): e3000918. https://doi.org/10.1371/journal.pbio.3000918
