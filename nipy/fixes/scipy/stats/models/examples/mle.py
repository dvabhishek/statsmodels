from numpy import dot,  outer, random, argsort
from scipy import io, linalg, optimize
from scipy.sparse import speye

def R(v):
    rq = dot(v.T,A*v)/dot(v.T,B*v)
    res = (A*v-rq*B*v)/linalg.norm(B*v)
    data.append(linalg.norm(res))
    return rq

def Rp(v):
    """ Gradient """
    result = 2*(A*v-R(v)*B*v)/dot(v.T,B*v)
    print "Rp: ", result
    return result

def Rpp(v):
    """ Hessian """
    result = 2*(A-R(v)*B-outer(B*v,Rp(v))-outer(Rp(v),B*v))/dot(v.T,B*v)
    print "Rpp: ", result
    return result


A = io.mmread('nos4.mtx') # clustered eigenvalues
#B = io.mmread('bcsstm02.mtx.gz')
#A = io.mmread('bcsstk06.mtx.gz') # clustered eigenvalues
#B = io.mmread('bcsstm06.mtx.gz')
n = A.shape[0]
B = speye(n,n)
random.seed(1)
v_0=random.rand(n)

print "try fmin_bfgs"

data=[]
v,fopt, gopt, Hopt, func_calls, grad_calls, warnflag,allvecs = optimize.fmin_bfgs(R,v_0,fprime=Rp,full_output=1,retall=1)
if warnflag == 0:
   semilogy(arange(0,len(data)),data)
   print 'Rayleigh quotient BFGS',R(v)


print "fmin_bfgs OK"

print "try fmin_ncg"

#
# WARNING: the program may hangs if fmin_ncg is used
#
data=[]
v,fopt, fcalls, gcalls, hcalls, warnflag,allvecs = optimize.fmin_ncg(R,v_0,fprime=Rp,fhess=Rpp,full_output=1,retall=1)
if warnflag==0:
   semilogy(arange(0,len(data)),data)
   print 'Rayleigh quotient NCG',R(v)
