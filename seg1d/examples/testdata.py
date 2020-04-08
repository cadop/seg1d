
import pickle 
import numpy as np
import os

folder = os.path.dirname(__file__)
print(folder)

with open(folder+'/data/refData.pickle', 'rb') as f:
    refData = pickle.load(f)
# with open(folder+'/data/targData.pickle', 'rb') as f:
#     targData = pickle.load(f)
# with open(folder+'/data/weights.pickle', 'rb') as f:
#     weights = pickle.load(f)


# print(refData)
# print(targData)
# print(weights)


# np.save(folder+'/r.npy', refData)
# np.save(folder+'/t.npy', targData)
# np.save(folder+'/w.npy', weights)

r = np.load(folder+'/data/r.npy', allow_pickle=True)
t = np.load(folder+'/data/t.npy', allow_pickle=True)
w = np.load(folder+'/data/w.npy', allow_pickle=True)[()]

r0 = r[0]
r1 = r[1]
print(r)
# print(t)
print(w)

