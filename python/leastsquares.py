import numpy as np
import matplotlib.pyplot as plt



def create_nvectors(ang): # assumes angle in degrees

    n = np.zeros((len(ang), 2))

    for i in range(len(ang)):
        for j in range(2):
            if j == 0:
                n[i][j] = np.sin(ang[i] * np.pi / 180.0)
            if j == 1:
                n[i][j] = np.cos(ang[i] * np.pi / 180.0)
    return n

def intersect(P0, n): # P0 a and n are N X 2 arrays where N is how many lines there are

    #creates all line direction vectors
    #n = (P1 - P0)/ np.linalg.norm(P1-P0, axis=1)[:,np.newaxis]

    #create an array of projectors(perpendicular distance from a point to a line), or the equation I - n*n^T 
    projs = np.eye(n.shape[1]) - n[:,:,np.newaxis]*n[:,np.newaxis]

    #create R matrix and q vector for equation Rp = q where p is intersection point
    R = projs.sum(axis=0)
    q = (projs @ P0[:,:,np.newaxis]).sum(axis=0)

    #least square for point p from R matrix and q vector p: Rp = q
    p = np.linalg.lstsq(R,q)[0]

    return p

ang = [-44.504854321138524, -42.02922380123842, -41.27857390748773, -37.145774853341386, -34.097022454778674]
P0 = np.array([[-7.07106638,  7.07106145],
       [-7.34817263,  6.78264524],
       [-7.61354115,  6.48336347],
       [-7.86671133,  6.17371816],
       [-8.10730426,  5.85419995]])
#print(P0)

n = create_nvectors(ang)
p =intersect(P0, n)
print(p)
plot(ang,P0,p)