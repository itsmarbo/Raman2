import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# LOAD DATA
data = pd.read_csv('Solv_RR_convoluted_wI39601.dat', header=None, engine='python', delim_whitespace=True)
data2 = pd.read_csv('Experimental.txt', header=None, engine='python', delim_whitespace=True)
#data3 = pd.read_csv('Experimental.txt', header=None, engine='python', delim_whitespace=True)

# osc in this case is directly Intensity 
# Because the data we have is from FCC3
energies = data[0]
osc = data[1]

energies2 = data2[0]
osc2 = data2[1]

#energies3 = data3[0]
#osc3 = data3[1]

def NormaliseData(data):
    return (data - np.min(data)) / (np.max(data) - np.min(data))

norm_osc = NormaliseData(osc)
norm_osc2 = NormaliseData(osc2)
#norm_osc3 = NormaliseData(osc3)

fig, ax = plt.subplots(figsize=(6, 4))
ax.plot(energies, norm_osc, color='blue', label='explicit + PCM', linewidth=1)
ax.plot(energies2, norm_osc2, color='red', label='EXP', linewidth=1)
#ax.plot(energies3, norm_osc3, color='black', label='EXP', linewidth=1)

# Set grid with dotted red lines
ax.grid(color='red', linestyle='dotted', linewidth=0.5)

# Set other parameters for the graphic
ax.set_title("Raman Spectra")
ax.set_xlabel("Raman Shift (cm$^-1$)", fontsize=11)
ax.xaxis.set_tick_params(labelsize=11, width=1.5)
ax.yaxis.set_tick_params(labelsize=11, width=1.5)
for axis in ['top', 'bottom', 'left', 'right']:
    ax.spines[axis].set_linewidth(1.5)
ax.set_xlim(250, 2000)
ax.set_ylabel("Intensity", fontsize=11)
ax.legend(fontsize=11)

# Find the indices of the four highest peaks for each data
#top_indices_caspt2 = np.argsort(norm_osc)[-4:]
#top_indices_tddft = np.argsort(norm_osc2)[-4:]

# Plot the peak values on the graph with the respective colors
#for i in top_indices_caspt2:
#    ax.text(energies[i], norm_osc[i], f'{norm_osc[i]:.2f}', color='blue', ha='center', va='bottom', fontsize=4)

#for i in top_indices_tddft:
#    ax.text(energies2[i], norm_osc2[i], f'{norm_osc2[i]:.2f}', color='red', ha='center', va='bottom', fontsize=4)

plt.tight_layout()

# Save the plot as a PNG file
plt.savefig('RamanSpectra_comparisonEXP4.png', dpi=300)

# Close the plot to free up resources
plt.close()
