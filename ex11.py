##############################################################################
#   OS11 LOGISTICS
#
#   Author   : Orge, Fernando Gabriel
#   Exercise : EX11 - Shortest Path with time constraints 
#                     Lagrangian Relaxation with subgradient method
#
#   For #EX11 and T ≤ 8 hs. apply the Lagrangian Relaxation method and 
#   find the shortest path iterating between several values of lagrangian
#   multipliers using the subgradient method.
#
##############################################################################
import numpy     as np
import logistics as lg
import math
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


# initial condition for subgradient method
struct = []
lnext  = 0
lcurr  = 0
i      = 0
tol    = 0.005
diff   = math.inf
while (diff > tol):
    i     = i + 1
    lcurr = lnext
    chat  = c + lcurr*t
    res   = linprog(c=chat, A_eq=NA, b_eq=b, bounds=bounds, method='simplex')
    func  = res.fun
    xopt  = res.x
    
    lagr  = func - lcurr*T
    grad  = np.inner(t, xopt) - T
    step  = 1/i
    lnext = lcurr + step * grad
    diff  = abs(lnext - lcurr)
    struct.append([i, lagr, grad, step, lcurr, lnext, diff, xopt])

# the last element is worst than the previous one
# hence, I'll delete it
struct.pop() 
 
# I couldn't find a simple way to index my list of lists to plot the results
# That's why I've used this loop to reconstruct the i, lagr and lamb vectors
i    = []
lagr = []
lamb = []
xopt = []
for elem in struct:
    i.append(elem[0])
    lagr.append(elem[1])
    lamb.append(elem[4])
    xopt.append(elem[7])
    
plt.figure()
plt.plot(i, lagr , '.-')
plt.plot(i, 5.4*np.ones(len(lagr)), 'r')
plt.xlabel('Iterations')
plt.ylabel('Cost(i)')
plt.ylim(4,5.5)
plt.legend(('Cost(i)', 'Optimal cost = 5.4'))
plt.tight_layout()
plt.grid()
plt.savefig("ex11_a.png")

plt.figure()
plt.plot(i, lamb , '.-')
plt.plot(i, 0.4*np.ones(len(lamb)), 'r')
plt.xlabel('Iterations')
plt.ylabel('$\lambda(i)$')
plt.ylim(0,1)
plt.legend(('$\lambda$(i)', 'Optimal $\lambda$ = 0.4'))
plt.tight_layout()
plt.grid()
plt.savefig("ex11_b.png")

print('SOLUTION')
print('\t # of iterations : %d'  % i[-1])
print('\t Optimal cost    : %0f' % lagr[-1])
print('\t Optimal lambda  : %0f' % lamb[-1])
print('\t Optimal Xvector : %s'  % xopt[-1])
print('\t Path to take    : \n')
for k in range(0, len(xopt[-1])):
    if xopt[-1][k] == 1:
        print('\t\t Arc %s must be taken.' % str(lg.convert_arc(arcs[k], nodes)))
