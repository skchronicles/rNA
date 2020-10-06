from __future__ import print_function
from functools import reduce
import pandas, os, sys


def filepath2samplename(s):
	bn = os.path.basename(s)
	sn = bn.split(".p2.Aligned.")[0]
	return sn


def read_tin_xls(s,sn):
	df = pandas.read_csv(s,sep="\t",header=0,usecols=['geneID','TIN'])
	df.columns=['geneID', sn]
	return df


def readit(s):
	return read_tin_xls(s,filepath2samplename(s))


if __name__ == '__main__':


	files=sys.argv[1:]

	if not files:
		# User did not provide a list of files to merge!
		print("Usage Error: Failed to provide any files\npython {} /path/to/TIN/output/*tin.xls".format(sys.argv[0]))
		sys.exit(1)

	df=reduce(lambda a,b:pandas.merge(a,b), map(lambda x:read_tin_xls(x, filepath2samplename(x)), files))
	df.to_csv("combined_TIN.tsv", sep="\t", header=True, index=False)

