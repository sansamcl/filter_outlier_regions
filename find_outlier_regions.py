#!/usr/bin/python

#------------------------------------------------------------------------------
#generates a bedgraph with windows having values > Q3 + 1.5 * IQR
#Chris Sansam
#------------------------------------------------------------------------------

import sys, getopt
import scipy.stats as scs
import numpy as np

def main(argv):
   #read input and output filenames
   inputfile = ''
   outputfile = ''
   try:
      opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
   except getopt.GetoptError:
      print ("find_outlier_regions.py -i <inputfile> -o <outputfile>")
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print ("find_outlier_regions.py -i <inputfile> -o <outputfile>")
         sys.exit()
      elif opt in ("-i", "--ifile"):
         inputfile = arg
      elif opt in ("-o", "--ofile"):
         outputfile = arg
   #load input bedgraph file
   BEDGRPH = np.loadtxt(inputfile,dtype=np.str,delimiter='\t')
   #gets third column of counts
   counts = BEDGRPH[:,3]
   #converts counts int to float and sets to data
   data = counts.astype(float)
   #calculates inter-quartile range
   IQR = scs.iqr(data)
   #calculates median
   MED = np.median(data)
   #calculates third quartile
   Q3 = MED + (0.5 * IQR)
   #calculates upper threshold for subsetting
   UpperOut = Q3 + (1.5*IQR)
   #subsets bedgraph
   BEGRPH_out = BEDGRPH[data > UpperOut]
   #saves subsetted bedgraph
   np.savetxt(outputfile, BEGRPH_out, fmt='%3.10s', delimiter='\t')

if __name__ == "__main__":
   main(sys.argv[1:])