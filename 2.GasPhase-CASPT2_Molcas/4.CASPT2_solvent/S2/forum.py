import h5py
import numpy as np
filename = 'opt_xfield.slapaf.h5'
f = h5py.File(filename, 'r')
np.savetxt('HESSIAN.txt', f['HESSIAN'])
f.close()