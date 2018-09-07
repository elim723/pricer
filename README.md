This project is Elim's solution to a job interview assignment `Pricer` by Kinetica.

It is a very fun project. Elim had zero understanding in how bid/ask works before. Elim spent about 12 hours in total to complete this assignment which includes understanding and solving the given problem as well as implementing and testing my solutions. Further explanations to the questions addressed in `Pricer/problem.html` are explained in `answers.txt`.

Solution Script
---------------

My solution to the problem is a python script `pricer.py` which took a `targetsize` argument from user and read in a text file via piping. One can use `>` carrot to write output messages to an out file:

> elims $ cat Pricer/pricer.in  | python pricer.py --targetsize 200 > Pricer/elim200.out

In short, the `pricer.py` initializes a `Book` instance, which keeps track of the standing bids and asks (see `Book.py`).

Resources
---------

Elim has also provided two scripts: `Resources/pricer.sh` and `Resources/pricer_python_standalone.py`.

First, the bash script checks the correctness of my solution script. It assumes that the input file `pricer.in` is located in `Pricer/` folder. The bash script automatically runs all three target sizes (1, 200, 10k) and print out the number of lines that are different between Elim's anwser and standard anwser by Kinetica via `sdiff`. The command line to run `pricer.sh` is 

> elims $ bash pricer.sh

The output Elim got is
>> target size 1 : differences between Elim and correct outputs = 0    
>> target size 200 : differences between Elim and correct outputs = 0  
>> target size 10000 : differences between Elim and correct outputs = 0 

This means that there are no differences between Elim's solution and the one provided by Kinetica. 

Second, a standalone python script `pricer_python_standalone.py` is also found in the `Resources/` folder. This script is the most original version by Elim that gives the correct logic (done by 09/03/2018). This script uses a python built-in `open ()` function instead of standard input (stdin) via piping. It also takes the `.gz` as the input file instead of `.in`. This script took about 7 min to run the entire input file `Pricer/pricer.in` with a target size of 200, whereas `pricer.py` via piping took about 3 min for the same inputs. To run this python script,

> elims $python pricer_python_standalone.py --targetsize 200 --verbose 0 --maxrows -1

Testing
-------

In addition, Elim wrote two unittests for `Book.py` and `pricer.py`. The test scripts are located in `test_scripts/`.