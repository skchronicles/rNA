from __future__ import print_function
import sys




def global_maxima(mylist):
	"""
	Returns the max index and global maxima of the list.
	"""
	maxima = -1
	index = -1
	for i in range(0, len(mylist), 1):
		distance = float(mylist[i])
		if distance > maxima:
			maxima = distance
			index = i
	return index, maxima	



if __name__ == '__main__':

	try:
		input_file = sys.argv[1]
	except IndexError:
		print('USAGE: python {} mqc_rseqc_inner_distance_plot_Percentages.txt'.format(sys.argv[0]))

	outfile = open("mqc_rseqc_inner_distance_plot_Percentages_parsed.txt", "w")
	outfile.write("Sample\tInner_Dist_Maxima\n")

	with open(input_file, 'r') as file:
		header = next(file)
		header = header.strip().split('\t')[1:] # skip sample header
		for line in file:
			linelist = line.strip().split('\t')
			sample, *distances = linelist
			index, maxima = global_maxima(distances)
			mdist = header[index]
			outfile.write("{}\t{}\n".format(sample, mdist))
