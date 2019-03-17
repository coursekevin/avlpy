import subprocess
import datetime
import re
import os

def read_avl_file(fname):
	""" This function reads an avl file into a list of dictionaries for each surface

		-------------------------------------------------------------------------------
		INPUTS
			- fname:	filename string

		-------------------------------------------------------------------------------
		OUTPUTS
			- surfaces: list containing dictionaries of avl sections

	"""
	surfaces = []
	with open(fname,"r") as file:
		line_list = [line for line in file if not re.match("^#|^\s*$",line)]

		for (line,idx) in zip(line_list,range(len(line_list))):



			surf_match = re.search("SURFACE",line)
			ydup_match = re.search("YDUP",line)
			angl_match = re.search("ANGLE",line)
			scal_match = re.search("SCALE",line)
			tran_match = re.search("TRANSLATE",line)
			sect_match = re.search("SECTION",line)
			afil_match = re.search("AFIL",line)
			cntr_match = re.search("CONTROL",line)


			if idx == 0:
				surfaces.append({'case':line.split()[0]})

			elif idx == 1:
				surfaces[-1]['mach'] = line.split()[0]

			elif idx == 2:
				surfaces[-1]['sym'] = line.split()[:3]

			elif idx == 3:
				surfaces[-1]['aref'] = line.split()[:3]

			elif idx == 4:
				surfaces[-1]['mref'] = line.split()[:3]

			elif idx == 5:
				surfaces[-1]['CD0'] = line.split()[0]

			elif surf_match:
				surfaces.append({'SURFACE':line_list[idx+1].split()[0]})
				line_tmp = line_list[idx+2].split()
				surfaces[-1]['Nc|Cs|Ns|Ss'] = line_tmp[:4]

			elif ydup_match:
				surfaces[-1]['YDUPLICATE'] = line_list[idx+1].split()[0]

			elif angl_match:
				surfaces[-1]['ANGLE'] = line_list[idx+1].split()[0]

			elif scal_match:
				line_tmp = line_list[idx+1].split()
				surfaces[-1]['SCALE'] = line_tmp[:3]

			elif tran_match:
				line_tmp = line_list[idx+1].split()
				surfaces[-1]['TRANSLATE'] = line_tmp[:3]

			elif sect_match:
				line_tmp = line_list[idx+1].split()
				surfaces[-1]["SECTION_" + str(idx)] = line_tmp

			elif afil_match:
				line_tmp = line_list[idx+1].split()
				surfaces[-1]["AFIL_" + str(idx)] = line_tmp[0]

			elif cntr_match:
				line_tmp = line_list[idx+1].split()
				surfaces[-1]["CONTROL_" + str(idx)] = line_tmp

	return(surfaces)

def save_avl_file(fname,surfaces):
	""" This function saves a surface list to an avl file

		---------------------------------------------------------------------------------
		INPUTS
			- fname: 		filename to be saved 
			- surfaces:		surfaces list containing dictionaries of sections
	"""
	line_count = 0;
	with open(fname,'w') as file:
		for surface in surfaces:
			for key in surface.keys():
				if line_count < 5:
					if type(surface[key]) == list:
						file.write('   '.join(surface[key]) + '\n')
					else:
						file.write(surface[key] + '\n')		
				elif line_count == 5:
						file.write(surface[key] + '\n#\n')	
				elif key == 'Nc|Cs|Ns|Ss':
					file.write(" ".join(surface[key]) + '\n#\n')

				elif key == "SURFACE":
					file.write("#\n#\n" + key.split("_")[0] + '\n')
					file.write(surface[key] + '\n')					
				elif key == "TRANSLATE":
					file.write(key.split("_")[0] + '\n')
					file.write('   ' + '   '.join(surface[key]) + '\n#\n#\n')
				elif key.split("_")[0] == "SECTION":
					file.write(key.split("_")[0] + '\n')
					file.write('   ' + '   '.join(surface[key]) + '\n')
				else:
					file.write(key.split("_")[0] + '\n')
					

					if type(surface[key]) == list:
						file.write('   ' + '   '.join(surface[key]) + '\n#\n')
					else:
						file.write('   ' + surface[key] + '\n#\n')

				line_count += 1

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

class  avlRun:
	""" This function takes in a terminal command which would open avl (ie. "avl3.35") and a list
		of strings containting avl commands to be executed in sequence (ie. ["load plan.avl", ....]).
		returns whether or not the commands were executed successfully 

		--------------------------------------------------------------------------------------------
		INPUTS
			- avl_opn_cmd: 	string that would open avl from terminal
			- cmd_list:		list of avl commands in string form

		--------------------------------------------------------------------------------------------
		OUTPUTS
			- avl_out:		subprocess object  indicating whether avl ran successfully

	"""
	def __init__(self,avl_opn_cmd,avl_file,mass_file):
		""" This is the initialization function for the avlRun class

			----------------------------------------------------------------------------------------
			INPUTS
				- avl_file:  file path to avl file
				- mass_file: file path to mass file for avl
		"""

		# default command start
		self.avl_opn_cmd = avl_opn_cmd

		self.cmd_path = ['load ' + avl_file,
						 'mass ' + mass_file,
					     'mset 0']

		self.tmp_dir = "tmp_avl"			     
		os.makedirs(self.tmp_dir, exist_ok = True)
    # ---------------------------------------------------------------------------------------------
    # SETTING FLIGHT CONSTRAINTS
    # ---------------------------------------------------------------------------------------------
	def set_flight_constraint(self,fregime,var,value):
		""" This function sets a constraint 

			----------------------------------------------------------------------------------------
			INPUTS
				- fregime:		flight regime ('C1' or 'C2')
				- var:			variable ('v', 'CL', etc.)
				- value:		value to be set
		"""

		new_cmd = ['oper','C1',var,str(value),'\n','\n']
		
		[self.cmd_path.append(j) for j in new_cmd]

	def set_var_constraint(self,var,cnstr,value):
		""" This function sets a variable constraint

			----------------------------------------------------------------------------------------
			INPUTS
				- var:			variable to be set (ie. D1)
				- cnstr:		constaint variable (ie. PM)
				- value:		value to set cnstr to (ie PM = 0 through D1)
		"""


		new_cmd = ['oper',var,cnstr,str(value),'\n']

		[self.cmd_path.append(j) for j in new_cmd]

    # ---------------------------------------------------------------------------------------------
    # RUNNING AVL PROCESSES
    # ---------------------------------------------------------------------------------------------
	def get_flow_analysis(self,output):
		""" This function returns the flow analysis computed using avl

			---------------------------------------------------------------------------------------
			INPUTS
				- output:		OPER output (typically FT, ST, etc.)

			---------------------------------------------------------------------------------------
			OUTPUTS
				- fname:		file save name
				- proc_out:		subprocess out
		"""
		fname = self.tmp_dir + "/avlFA_"+output +"_" +datetime.datetime.now().strftime("%Y%m%d-%H%M%S") + ".txt"

		new_cmd = ['oper','x',output,fname,'\n','q']

		cmd_tmp = self.cmd_path.copy()

		[cmd_tmp.append(j) for j in new_cmd]

		cmd_bytes = "\n".join(cmd_tmp)

		with open(self.tmp_dir + '/stdout.txt','wb') as outfile:
			proc_out = subprocess.run(self.avl_opn_cmd, input=cmd_bytes.encode(), stdout = outfile)
		
		return((fname,proc_out))

	def get_eig_analysis(self,output):
		""" This function returns the eigen analysis using avl

			---------------------------------------------------------------------------------------
			INPUTS
				- output
		"""
		fname = self.tmp_dir +"/avlEA_"+output +"_" +datetime.datetime.now().strftime("%Y%m%d-%H%M%S") + ".txt"

		new_cmd = ['oper','x','\n','mode','0','n',output,fname,'\n','q']

		cmd_tmp = self.cmd_path.copy()

		[cmd_tmp.append(j) for j in new_cmd]

		cmd_bytes = "\n".join(cmd_tmp)

		with open(self.tmp_dir + '/stdout.txt','wb') as outfile:
			proc_out = subprocess.run(self.avl_opn_cmd, input=cmd_bytes.encode(), stdout = outfile)
		
		return((fname,proc_out))

	def custom_cmd(self,cmd_list):
		""" This function runs the custom command sequence given in cmd_list

			--------------------------------------------------------------------------------------
			INPUTS
				- cmd_list: list of string
		"""
		if cmd_list[-1] == "q":
			cmd_bytes = "\n".join(cmd_list)
		else:
			cmd_list.append("q")
			cmd_bytes = "\n".join(cmd_list)


		return(subprocess.run(avl_opn_cmd, input=cmd_bytes.encode()))

if __name__ == '__main__':
	# setting up avlRun class

	# --------------------------------------------------------------------------------------------
	# AVL Runs
	# --------------------------------------------------------------------------------------------
	avlMKI = avlRun('avl3.35','wingus.avl','wingus.mass')
	avlMKI.set_flight_constraint('C1','V','9')
	avlMKI.set_var_constraint('D1','PM',0)

	fname,proc_out = avlMKI.get_flow_analysis('ST')
	avl_dict = read_avl_flow_analysis(fname)

	fname2,proc_out2 = avlMKI.get_eig_analysis('S')

	A,B = read_avl_sys_mat(fname2)

	print("Alpha: " + str(avl_dict['Alpha']))
	print("Elevator Defl.: " + str(avl_dict['elevator']))
	print("Neutral Point: " + str(avl_dict['Xnp']))
	print("Cma: " + str(avl_dict["Cma"]))
	print("Clb: " + str(avl_dict["Clb"]))
	print("Cnb: " + str(avl_dict["Cnb"]))

	# -------------------------------------------------------------------------------------------
	# Reading avl files
	# -------------------------------------------------------------------------------------------
	surfaces = read_avl_file('wingus.avl')
	#print(surfaces)

	save_avl_file('surfaces.avl',surfaces)
