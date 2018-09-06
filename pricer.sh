#!/bin/bash 

####
#### By Elim Thompson (09/04/2018)
####
#### This bash script is served as a test
#### procedure for the correctness.
####
#### For each target size (1, 200, 10000), 
#### I run the pricer.py with the corresponding
#### input files. Then I compare my output
#### file to the answer provided by Kinetica.
#### It then print out the differences between
#### my output and the provided answer. If
#### my output is correct, the count should
#### by 0.
####
#######################################################

### loop through targetsizes of 1, 200, 10000
for ts in 1 200 10000; do
    ## print output to Pricer/elim1(or 200 or 10000).out
    cat Pricer/pricer.in  | python pricer.py --targetsize ${ts} > Pricer/elim${ts}.out;
    ## test by countint differences in output via sdiff by grepping `|` which indicates differences
    length=`sdiff Pricer/elim${ts}.out Pricer/pricer.out.${ts} | grep \| | wc -l`
    ## print out differences between mine and standard outputs from Kinetica
    echo "target size ${ts} : differences between Elim and correct outputs = ${length}"
done
