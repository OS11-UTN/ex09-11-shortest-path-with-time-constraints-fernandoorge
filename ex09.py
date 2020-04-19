##############################################################################
#   OS11 LOGISTICS
#
#   Author   : Orge, Fernando Gabriel
#   Exercise : EX09 - Shortest Path with time constraints - Direct LP approach
#   
#
# 1) If a person had to travel between s and t in less than 9 hours (T). 
#    What’s the shortest path? Try to solve the problem with a simple LP model.
#
#    SOLVING PROBLEM WITH: simplex
#	     The raw solution will be        : [0. 1. 0. 0. 1. 0. 1.]
#		 Arc ('s', '3') must be taken.
#		 Arc ('3', '5') must be taken.
#		 Arc ('5', 't') must be taken.
#	     The minimum cost will be        : 5.00 
#	     The best time will be           : 9.00
#	     
# 2) What if the maximum available time that this person has drops to 8 hours? 
#    What’s the new shortest path? Understand the LP model outputs.
#
#    SOLVING PROBLEM WITH: simplex
#	     The raw solution will be        : [0.2 0.8 0.  0.2 0.8 0.  0.8]
#		 Arc ('s', '2') must be taken.
#		 Arc ('s', '3') must be taken.
#		 Arc ('2', 't') must be taken.
#		 Arc ('3', '5') must be taken.
#		 Arc ('5', 't') must be taken.
#	     The minimum cost will be        : 5.40 
#	     The best time will be           : 8.00 
#
#    **CONCLUSION:**
#       This solution is not feasible. There's no way to take two path at a time.
#       A person cannot be splitted into two parts to take 0.2 of path ('s', '2')
#       and 0.8 of path ('s', '3').
#       Either ('s', '2') path is taken or ('s', '3') is taken but not both.
#
# 3) What’s the first solution that comes to your mind in order to solve point 
#    2 issues? Is it feasible in reality?
#
#    One possible solution is to restric the decision variables to be binary, 
#    any given path is taken or not.
#
##############################################################################
import numpy     as np
import logistics as lg
from   scipy.optimize import  linprog

nodes = ['s','2','3','4','5','t']


NN = np.array([[0, 1, 1, 0, 0, 0],
               [0, 0, 0, 1, 0, 1],
               [0, 0, 0, 0, 1, 0],
               [0, 0, 0, 0, 0, 1],
               [0, 0, 0, 0, 0, 1],
               [0, 0, 0, 0, 0, 0]])

c = np.array( [2, 1, 2, 5, 2, 1, 2] )
               
NA, arcs = lg.nn2na(NN) 
b = np.array([1, 0, 0, 0, 0, -1])

t = np.array([[3, 1, 3, 1, 3, 3, 5]])
T = 9

bounds = tuple([(0, 1) for arcs in range(0, len(arcs))])

##############################################################################
# Inputs lo linprog algorithm
print('\t OPTIMIZER INPUTS                          \n'
      '\t   Minimize c*x                            \n'
      '\t     where                                 \n'
      '\t         c = %s                            \n'
      '\t                                           \n'
      '\t   Subject to                              \n'
      '\t     A_eq * X = b_eq                       \n'
      '\t       where                               \n'
      '\t         A_eq = \n%s                       \n'
      '\t         b_eq = %s                         \n'
      '\t                                           \n'
      '\t     A_ub * X = b_ub                       \n'
      '\t       where                               \n'
      '\t         A_ub = t = %s                     \n'
      '\t         b_ub = T = %s                     \n'
      '\t     Bounds of each X arc variable :   %s \n' % (c, NA, b, t, T, bounds))

name_method = 'simplex'
print('\n SOLVING PROBLEM WITH: %s' % name_method)
res = linprog(c, A_ub=t, b_ub=T, A_eq=NA, b_eq=b, bounds=bounds, method=name_method)
print('\t Solution to the problem:')
print('\t     The raw solution will be        : %s' % res.x)
for k in range(0, len(res.x)):
    if res.x[k] > 0:
        print('\t\t Arc %s must be taken.' % str(lg.convert_arc(arcs[k], nodes)))
print('\t     The minimum cost will be        : %0.2f ' % res.fun)
print('\t     The best time will be           : %0.2f ' % np.inner(res.x, t))
