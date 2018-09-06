This is Elim's solution to a job interview
assignment `Pricer` by Kinetica.

NOTE :: Given that Elim was given the task
within the past 30 hours, she is able to get
the logic and implementation working right.
Elim has also provided an easy test against
the provided answers given target sizes of 1,
200, 10000. However, Elim is planning to
write a unittest for this project. 

There are three options to run `pricer`. All
options use the same logic.

Option 1
--------

> elims $ cat Pricer/pricer.in  | python pricer.py --targetsize 200 > Pricer/elim200.out

This option is the solution that the problem set
asks for. It uses bash I/O pipe to due with in and
out put text messages. First, `cat` read the input
file as one line and is fed to the python script.
The python script took the infile as standard input
(stdin), as well as the input targetsize of 200. The
out messages are `carroted` (>) to a dedicated output
file `Pricer/elim200.out`.

Option 2
--------

> elims $ bash pricer.sh

>> target size 1 : differences between Elim and correct outputs = 0    
>> target size 200 : differences between Elim and correct outputs = 0  
>> target size 10000 : differences between Elim and correct outputs = 0 

This option assumes that pricer.in is located in
Pricer/. This bash script also automatically runs
all three target sizes (1, 200, 10k) and print out
(`echo`) the differences between Elim's anwser and
standard anwser by Kinetica. The `sdiff` comparison
serves as a simple test between my answer and the
correct answer.

Option 3
--------

> elims $python pricer_python_standalone.py --targetsize 200 --verbose 0 --maxrows -1 (--test if use test file)

This is the most originated version that gives
the correct logic (done by 09/03/2018). This
script uses a python built-in `open ()` function
instead of standard input (stdin) via bash and
takes the .gz as the input file instead of .out.
This version of `pricer.py` is the slowest
(about 7 min) to run the entire Pricer/pricer.in,
whereas Option 2 took about 3 min for the same input.