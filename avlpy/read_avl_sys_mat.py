def read_avl_sys_mat(fname):
	""" This function reads a filename and returns an avl_dict. The keys in the dictionary are the 
		values found in the file and avl_dict[key] is the value.

		--------------------------------------------------------------------------------
		INPUTS
			- fname: filename containing path to system matrix output

		--------------------------------------------------------------------------------
		OUTPUTS
			- A:	dynamic system marix
			- B: 	dynamic control matrix
	"""
	A = []
	B = []
	with open(fname,"r") as file:
		for line in file:
			num_match = re.search("\d",line)
			if num_match:
				line_split = line.split()
				A_row = [float(a) for a in line_split[:12]]
				A.append(A_row)
				B_row = [float(b) for b in line_split[12:]]
				B.append(B_row)

	return (A,B)