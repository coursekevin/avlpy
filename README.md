# avlpy
A high level python wrapper for Drela and Youngren's AVL (http://web.mit.edu/drela/Public/web/avl/). The intent is to be able easily script interactions with AVL for iterative aircraft design.

## Installation
### Note the package is only a wrapper for AVL and requires AVL be installed. See http://web.mit.edu/drela/Public/web/avl/ for more details

Install directly from git (recommended):

```bash
sudo pip install git+https://github.com/coursekevin/avlpy.git
```

or...

Clone the repository:

``` bash
git clone https://github.com/coursekevin/avlpy.git
```
and install the package by running:

```bash
python setup.py
```
from the avlpy/ directory

## Example AVL Scripting

From avlpy/example. Here we have predefined a wingus.avl and wingus.mass file. These files describe a model aircraft. We first import the library and initialize an avlRun object. I'm using avl3.35.
```python
import avlpy
# setup avl session
avlSess = avlpy.avlRun('avl3.35','wingus.avl','wingus.mass')
```

We now set the flight constraint to 9m/s. (A full list of flight constraints can be found in the AVL documentation).
```python
avlSess.set_flight_constraint('C1','V','9')
```

We now set the elevator so that the pitch moment is 0 at steady cruise.
```python
avlSess.set_var_constraint('D1','PM',0)
```

Write the static stablity analysis file to the avl_tmp directory (which is created at runtime).
```python
fname,proc_out = avlSess.get_flow_analysis('ST')
```
The flow analysis file is read and a dictionary containing the values from the file is stored in the dictionary.
```python
avl_dict = avlpy.read_avl_flow_analysis(fname)

print("Alpha: " + str(avl_dict['Alpha']))
print("Elevator Defl.: " + str(avl_dict['elevator']))
print("Neutral Point: " + str(avl_dict['Xnp']))
print("Cma: " + str(avl_dict["Cma"]))
print("Clb: " + str(avl_dict["Clb"]))
print("Cnb: " + str(avl_dict["Cnb"]))
```
Dynamic stability matrices are produced by AVL and the file is saved in the avl_tmp directory.
```python
fname2,proc_out2 = avlSess.get_eig_analysis('S')
```
The state matrices are read from the system matrix file and printed to the console.
```python
A,B = avlpy.read_avl_sys_mat(fname2)
print("\nDynamic 'A' Matrix: " + str(A))
```
## Example of Reading and Writing AVL Files

The predefined "wingus.avl" file is read to a list. The first element in the list is the .avl file preamble and the remaining list elements contain the various aircraft sections.

```python
surfaces = avlpy.read_avl_file('wingus.avl')
print("\nExample Surfaces File:")
print(surfaces)
```

The surfaces list is saved to a new "surfaces.avl" file. Note in this case the the aircraft configuration has not been editted.
```python
avlpy.save_avl_file('surfaces.avl',surfaces)
```
