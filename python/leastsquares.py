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

ang = [45.0, 315.0]
P0 = np.array([[0,1], [0,2]])
#print(P0)

n = create_nvectors(ang)
p =intersect(P0, n)
print(p)