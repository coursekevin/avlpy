from . import avlpy

# --------------------------------------------------------------------------------------------
# AVL SESSION
# --------------------------------------------------------------------------------------------
# setup avl session
avlSess = avlpy.avlRun('avl3.35','wingus.avl','wingus.mass')

# set cruise condition to 9 m/s
avlSess.set_flight_constraint('C1','V','9')

# set elevator to pitch such that pitch moment is 0 at cruise
avlSess.set_var_constraint('D1','PM',0)

# write flow analysis to default avl_tmp location
fname,proc_out = avlSess.get_flow_analysis('ST')

# read avl flow analysis to dictionary
avl_dict = avlpy.read_avl_flow_analysis(fname)

# print some important constants
print("Alpha: " + str(avl_dict['Alpha']))
print("Elevator Defl.: " + str(avl_dict['elevator']))
print("Neutral Point: " + str(avl_dict['Xnp']))
print("Cma: " + str(avl_dict["Cma"]))
print("Clb: " + str(avl_dict["Clb"]))
print("Cnb: " + str(avl_dict["Cnb"]))

# perform avl dynamic value analysis
fname2,proc_out2 = avlSess.get_eig_analysis('S')

# read state matrices to python arrays
A,B = avlpy.read_avl_sys_mat(fname2)

# run custom command (navigate to oper menu then exit the menu)
avlSess.custom_cmd(['oper','\n'])

# --------------------------------------------------------------------------------------------
# READING AVL FILES
# --------------------------------------------------------------------------------------------
surfaces = avlpy.read_avl_file('wingus.avl')

# save surfaces to new surfaces.avl file
avlpy.save_avl_file('surfaces.avl',surfaces)