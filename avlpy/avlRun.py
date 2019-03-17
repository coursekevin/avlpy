import os
import subprocess
import datetime
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
		cmd_tmp = self.cmd_path.copy()

		[cmd_tmp.append(cmd)for cmd in cmd_list]

		if cmd_list[-1] == "q":
			cmd_bytes = "\n".join(cmd_tmp)
		else:
			cmd_list.append("q")
			cmd_bytes = "\n".join(cmd_tmp)

		return(subprocess.run(self.avl_opn_cmd, input=cmd_bytes.encode()))