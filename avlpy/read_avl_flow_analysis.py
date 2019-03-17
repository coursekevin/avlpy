import re

def read_avl_flow_analysis(fname,printValues = False):
	""" This function reads a filename and returns an avl_dict. The keys in the dictionary are the 
		values found in the file and avl_dict[key] is the value.

		---------------------------------------------------------------------------------
		INPUTS
			- fname: filename of flow analysis file to be read

		---------------------------------------------------------------------------------
		OUTPUTS
			- avl_dict: dictionary containing all values computed through flow analysis
	"""
	avl_dict = {}
	with open(fname,"r") as file:
		for line in file:
			comment_match = re.search('#',line)

			# check for comment
			if comment_match:
				continue
			else:
				
				assignment_match = re.search("=",line)
				if assignment_match:
					if printValues:
						print(line)
					data = line.split()
					idx = [idx for item,idx in zip(data,range(len(data))) if item == "="]

					curr_keys = avl_dict.keys()
					update_list = [(data[i-1], float(data[i+1])) for i in idx if data[i-1] not in curr_keys]
					avl_dict.update(update_list)
				else:
					continue

	return avl_dict