##############################################################################
#   OS11 LOGISTICS
#
#   Author   : Orge, Fernando Gabriel
#   Exercise : EX10 - Shortest Path with time constraints - Lagrangian Relaxation
#   
#
#    1) For #EX11 and T ≤ 8 hs. apply the Lagrangian Relaxation method and find 
#       a solution iterating for different values of lagrangian multipliers (λ) 
#       between 0 and 1.
#    2) Plot all the objective function primal solutions for the set of 
#       lagrangian multipliers used in 1).
#    3) What should be the optimum λ related to the shortest path solution?
#
##############################################################################
import numpy     as np
import logistics as lg
import matplotlib
import matplotlib.pyplot as plt
from   scipy.optimize import  linprog


nodes = ['s','2','3','4','5','t']


NN = np.array([[0, 1, 1, 0, 0, 0],
               [0, 0, 0, 1, 0, 1],
               [0, 0, 0, 0, 1, 0],
               [0, 0, 0, 0, 0, 1],
               [0, 0, 0, 0, 0, 1],
               [0, 0, 0, 0, 0, 0]])
NA, arcs = lg.nn2na(NN) 

c = np.array([2, 1, 2, 5, 2, 1, 2])
t = np.array([3, 1, 3, 1, 3, 3, 5])               
b = np.array([1, 0, 0, 0, 0, -1])
T = 8
bounds = tuple([(0, 1) for arcs in range(0, len(arcs))])


param = np.arange(0, 1, 0.02)
lprob = []
for k in range(0, len(param)):
    newc = c + param[k]*t
    res = linprog(c=newc, A_eq=NA, b_eq=b, bounds=bounds, method='simplex')
    lprob.append(-param[k]*T + res.fun)
    
max_lprob = max(lprob)
idx_lprob = lprob.index(max_lprob)

plt.plot(param, lprob, '.-')
plt.plot(param[idx_lprob], max_lprob, 'ro')
plt.text(param[idx_lprob], max_lprob, 
    "($\lambda$,costs($\lambda$)) = (%0f, %0f)" % (param[idx_lprob], max_lprob))
plt.title('Lagrange Relaxation')
plt.xlabel('$\lambda$')
plt.ylabel('costs($\lambda$)')
plt.grid()
plt.savefig("ex10.png")
