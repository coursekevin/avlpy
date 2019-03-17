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