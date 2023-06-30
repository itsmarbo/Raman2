import h5py
import numpy as np
import sys
#np.set_printoptions(threshold=sys.maxsize)

filename = 'hessian_2.slapaf.h5'
f = h5py.File(filename, 'r')
np.savetxt('HESSIAN.txt', f['HESSIAN'])
f.close()
