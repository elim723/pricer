#!/bin/bash 

### loop through targetsizes of 1, 200, 10000
for ts in 1 200 10000; do
    ## print output to Pricer/elim1(or 200 or 10000).out
    cat Pricer/pricer.in  | python pricer.py --targetsize ${ts} > Pricer/elim${ts}.out;
    ## test by countint differences in output via sdiff by grepping `|` which indicates differences
    length=`sdiff Pricer/elim${ts}.out Pricer/pricer.out.${ts} | grep \| | wc -l`
    ## print out differences between mine and standard outputs from Kinetica
    echo "target size ${ts} : differences between Elim and correct outputs = ${length}"
done
