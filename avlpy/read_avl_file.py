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