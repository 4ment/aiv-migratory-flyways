# The Impact of Migratory Flyways on the Spread of Avian Influenza Virus in North America

This repository contains the data sets supporting the results of the following article:

Fourment M, Darling AE, and Holmes EC The Impact of Migratory Flyways on the Spread of Avian Influenza Virus in North America. _BMC Evolutionary Biology_, 2017, 17:118; DOI: [10.1186/s12862-017-0965-4](http://dx.doi.org/10.1186/s12862-017-0965-4).

Data sets are organised by gene (i.e. PB2, PB1, PA, NP, and MP) and each folder contains:
* a fasta file containing the nucleotide alignment (*-dna.fa)
* a tree file inferred from the nucleotide alignment (*.tree)
* a fasta file containing the geographic location of each sequence (*-geo.fa)


Other files:
* *countries.csv* contains the state/province to flyway assignment used in the study.

* *generate-models.py* is a python script that generates command line arguments on the standard output for reproducing the analyses using [_physher_](https://github.com/4ment/physher). For each genes it will generate the command line arguments for:
  * HRM: homogeneous rate model
  * 3-TRM: two-rate model with 3 flyways (Pacific, Central/Mississippi, and Atlantic)
  * 4-TRM: two-rate model with 4 flyways (Pacific, Central, Mississippi, and Atlantic)
  * 3-FRM: flyway-based model with 3 flyways
  * 4-FRM: flyway-based model with 4 flyways
  * Best model found by the genetic algorithm
