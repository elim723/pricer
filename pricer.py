#!/usr/bin/env python

####
#### By Elim Thompson (09/04/2018)
####
#### This script runs the pricer.py solution for
#### the Kinetica job application assignment.
####
#### This script requires a python 3.X. and the
#### following standard python packages:
####  optparse, os, sys, gzip, time
#### and a class `Book` from book.py
####
#### command to run this script:
####
#### $ python pricer.py --targetsize 200
####                    --verbose 0
<<<<<<< HEAD
####    < cat <input filename>
#### OR
#### $ cat <input filename> | python pricer.py
=======
####                   (--maxrows -1 for processing all rows)
####                   (--test if use test file)
>>>>>>> 474ec0ad3ce8fa4a284b78dca64a6728999da3a1
####
###########################################

###########################################
### import packages
###########################################
from optparse import OptionParser
from book import Book
import os, sys, gzip, time

###########################################
### parse options 
###########################################
usage = "usage: %prog [--targetsize 200 --verbose 0 (--test)]"
parser = OptionParser (usage=usage)
parser.add_option ('--targetsize', type='int', default=200,
                   help = "number of shares to keep track of.")
parser.add_option ('--verbose', type='int', default=0,
                   help = "If 0, no print out; If 1, print details")
<<<<<<< HEAD
(options, args) = parser.parse_args ()

targetsize = options.targetsize
verbose    = options.verbose     
lines      = args
=======
parser.add_option ('--maxrows', type='int', default=-1,
                   help = "maximum number of lines to process. -1 for all lines.")
parser.add_option ('--test', action='store_true', default=False,
                   help = "If --test, use test input file instead")
(options, args) = parser.parse_args ()

targetsize = options.targetsize
verbose    = options.verbose
maxrows    = options.maxrows
test       = options.test
>>>>>>> 474ec0ad3ce8fa4a284b78dca64a6728999da3a1

###########################################
### define variables
###########################################
## this directory
thisdir = os.path.dirname (os.path.abspath (__file__)) + '/'

###########################################
<<<<<<< HEAD
=======
### function to load input file
###########################################
def load_input ():

    ''' load the input file '''

    ## define input files
    infile  = 'Pricer/test.in.gz' if test else \
              'Pricer/pricer.in.gz'

    try:
        ## try to open the infile
        ## read infile - pricer.in.gz
        with gzip.open (infile, 'rb') as f:
            intxt = f.read ()
        f.close ()
        ## return individual lines in a list
        return intxt.decode ('utf-8').split ('\n')
    except IOError:
        ## no infile is found .. print error message
        print ('unable to read file: {0}'.format (infile))
        sys.exit()

###########################################
>>>>>>> 474ec0ad3ce8fa4a284b78dca64a6728999da3a1
### function to process each line
###########################################
def process (*data):

    ''' process a line of data

        :param data (list): [timestamp, add, order, side, price, size] or
                            [timestamp, reduce, order, size]

        :return message (str): If None, income / expanses remain the same
                               If not None, income / expanses is/are updated
                                            message print to outfile
    '''

    ## first two columns (timestamp and A/R) are ignored
    ## data with 4 elements -> reduce order
    ## data with 6 elements -> add order
    length, args = len (data), data[2:]
    ## data has only 4 or 6 elements
    ## ignore invalid line
    if not length in [4, 6]: return None

    ## print the given line of data
    if verbose: print ('data: {0}'.format (data))

    if length == 6:
        ## data with 6 elements -> add order
        ## *args has 4 elements
        print_income, print_expanse = book.add_order (*args)
    elif length == 4:
        ## data with 4 elements -> reduce order
        ## *args has 2 elements
        print_income, print_expanse = book.reduce_order (*args)

    ## get message (None if nothing is updated
    message = get_message (data[0].decode ('utf-8'),
                           print_S=print_income,
                           print_B=print_expanse)
    return message

###########################################
### function to get message
###########################################
def get_message (timestamp, print_S=False, print_B=False):

    ''' obtain message for output file if print_S or print_B

        :param timestamp (str) : time when income/expanse is updated
        :param print_S   (bool): If True, seller sells! Income is updated
        :param print_B   (bool): If True, buyer buys! Expanse is updated

        :return message (str): message to be printed in output file
    '''
    
    ## if either income / expanse is updated,
    ## nothing to be printed
    if not print_S and not print_B: return None
    ## print whether action from a 'S'eller or a 'B'uyer
    E = 'S' if print_S else 'B'
    ## get the updated values of money exchange (income / expanse)
    exchange = book.income if print_S else book.expanse
    ## if the value is changed to None, print 'NA'
    ## else the value has two decimal points
    exchange = 'NA' if exchange==None else '{:.2f}'.format (exchange) 
    ## print the array in one string
    return ' '.join ([timestamp, E, exchange, '\n'])

###########################################
### execution :)
###########################################
if __name__ == '__main__' :

    ## define output file
    outfile = thisdir + 'Pricer/elim.out'

    ## initialize a book instance
    book = Book (targetsize=targetsize,
                 verbose=verbose)

    ## start timer
    start_time = time.time ()

    ## open outfile
    with open (outfile, 'wb') as f:

        ## get all available lines
        lines = load_input ()        
        ## keep track of number of lines
        nlines = 0
        ## if maxrows is -1, read all lines
        if maxrows==-1: maxrows = len (lines) 

        ## loop through each input line
<<<<<<< HEAD
        for line in sys.stdin:
=======
        for line in lines:
>>>>>>> 474ec0ad3ce8fa4a284b78dca64a6728999da3a1
            # get data from current line
            data = line.split (' ')
            message = process (*data)
            # write message to new line if updated
<<<<<<< HEAD
            if message:
                f.write (message)
=======
            if message: f.write (message)
            # count nline 
            nlines += 1
            # break when maxrows is reached
            if nlines >= maxrows: break
>>>>>>> 474ec0ad3ce8fa4a284b78dca64a6728999da3a1

    ## close outfile
    f.close ()

    ## end timer
    dtime = (time.time () - start_time) / 60.
    print ('This script took {0} minuites to complete the task.'.format (dtime))
