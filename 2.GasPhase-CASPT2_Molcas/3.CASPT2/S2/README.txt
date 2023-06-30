-----------------------------------------------------------------
				README
-----------------------------------------------------------------
In this folder you will find all the necessary files after calculating
a CASPT2 method in thymine. For the 2 excited state, first bright state.

	name: thymine 2ES

FILE			OBJECTIVE
hessian_2.log		CASPT2 calculation + gradients modules
hessian_2.slapaf.h5	printed hessian after the CASPT2 calculation
rassi_s2.log		printed electric dipole after CASPT2 calculation

PARSING FILES
parssian.py		extract all information from CASPT2 calculations and generates
			the input FCC3 file.
try3.py			extract the hessian from the filename.h5 file
edipole.py		extract the electric dipole from RASSI calculation found in
			rassi_s2.log and generate an FCC3 co-input file. 
