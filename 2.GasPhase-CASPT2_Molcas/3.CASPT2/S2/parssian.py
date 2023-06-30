#!/usr/bin/env python3
"""
FCC3 Parser
This file is meant to collect all those important sections of a MOLCAS output 
and convert them into a FCC3 input file.
"""
#---------------------------------------------------------------------------
#                                Import libraries
#----------------------------------------------------------------------------

import sys

# Check input
if len(sys.argv) != 2:
    raise ValueError("No file provided for parsing!")

# Check for the .log extension
if sys.argv[1][-4:] != ".log":
    raise ValueError(".log file missing")

# Get the name of the .log file
file_name = sys.argv[1]
# Removing the .log extension from the filename
job_name = file_name[:-4]

#---------------------------------------------------------------------------
#                                Reading .log file
#----------------------------------------------------------------------------

# Open the log file and read it completely
# Store the data in a variable as a lost of strings;
# one line per string in the list
with open(file_name, 'r') as log_f:
    log_data = log_f.readlines()
#   
# The format its divided in five topics: INFO, GEOM, ENER, GRAD and HESS all of them in UNITS = AU
#    
#---------------------------------------------------------------------------
#                                Finding line numbers
#----------------------------------------------------------------------------

coords = []
gradient_lines = []
all_energies = []

# Iterate over all lines
for line_number, line in enumerate (log_data):

    # Look for the title
    if "Cartesian Coordinates / Bohr, Angstrom" in line:
        atom_init = line_number + 4                      # Extract the number where coordinates begin
        for i in range(atom_init, len(log_data)):        # Iterate over next lines
            temp_atom = log_data[i].split()              # Break line by spaces
            if len(temp_atom) > 0:                       # If there is text in the line ...
                coords.append([
                    # ... add atom number and symbol ...
                    int(temp_atom[0]), temp_atom[1] ] +\
                    # ... and all coordinates in Angstrom
                     [float(c) for c in temp_atom[5:]
                ])
            else:                                        # If there's not text in the line ...
                natom = coords[-1][0]                    # ... get the last atom's number as number of atoms
                break                                    # ... and exit the loop.
    
    # Total ENERGY
    if "::" in line:
        all_energies.append(line_number)                 # Get the lines where Total Energy is shown
    
    # Gradients
    if "Molecular gradients" in line:
        gradient_lines.append(line_number)               # Get the lines where the gradient appears

# Extract the last energy shown by the log file
total_energy = float(log_data[all_energies[-1]].split()[-1])

# Get the last Molecular gradient position
last_gradient_line = gradient_lines[-1]

# Extract the gradient data
gradientes = []                                          # Define a new list for the gradients
for g in range(last_gradient_line + 8, last_gradient_line + 8 + natom): # Iterate over them
    temp_grad = log_data[g].split()                      # Split the line by spaces
    gradientes += [float(i) for i in temp_grad[1:]]      # Add the values of the gradient

# Extract the Hessian
with open("HESSIAN.txt", "r") as file:                   # Open the file
    data = file.read()                                   # Extract data as single line

data = data.replace("[", " ").replace("]", " ")          # Remove extra characters
pre_hessian = data.split()                               # Split the data by spaces
hessian = [float(h) for h in pre_hessian]                # Turn everything into floats
        
#---------------------------------------------------------------------------
#                                Creating fcc input
#----------------------------------------------------------------------------
# Formatting the output
output = []

output.append("INFO\n")
output.append(f"State file generated from file:{file_name} (format: Open Molcas)\n\n")
output.append("GEOM      UNITS=ANGS\n")
output.append(f"    {natom}\n")
output.append(f"Geometry from {file_name} in xyz format (with filter: all)\n")

for c in coords:
    output.append(f"{c[1][0]}      {c[2]:12.8f} {c[3]:12.8f} {c[4]:12.8f}\n")

output.append("\nENER      UNITS=AU\n")
output.append(f"{total_energy:16.8e}\n")
output.append("\nGRAD      UNITS=AU")

temp = ""
for i, g in enumerate(gradientes):                       # Iterate over all gradient values
    if i % 5 != 0:                                       # FCC uses a 5-column format
        temp += f"{g:16.8e}"                             # If this is not the 5th value, add it to the row
    else:                                                # Or else ... if it is the 5th value
        output.append(temp + "\n")                       # Add the previous line to the output
        temp = f"{g:16.8e}"                              # And create a new line with the 5th value at the 0th column

if temp != "":                                           # If there were remaining values (not a multiple of 5)
    output.append(temp + "\n")                           # ... add them!


output.append("\nHESS      UNITS=AU")

temp2 = ""
for i, h in enumerate(hessian):                          # Same story as above, but with the hessian
    if i % 5 != 0:
        temp2 += f"{h:16.8e}"
    else:
        output.append(temp2 + "\n")
        temp2 = f"{h:16.8e}"

if temp2 != "":
    output.append(temp2 + "\n")

# ----------------------------------------------------------------------------
#                           Writing the final input
# ----------------------------------------------------------------------------
# Write the output to a file with the same name as the input, but with .fcc extension
output_file_name = job_name + ".fcc"
with open(output_file_name, 'w') as f:
 	f.writelines(output)
