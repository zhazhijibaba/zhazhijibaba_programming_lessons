import glob
import os
import re
from datetime import datetime
import math
import random
import numpy as np
from scipy import optimize
from scipy.integrate import solve_ivp
from scipy import stats
import matplotlib.pyplot as plt

# read data from data file of WHO
def read_data(fname):
    with open(fname, "r") as f:
        data1 = {}
        lines = f.readlines()
        for line in lines:
            #print line.strip()
            # clean up file using regular expression
            p = re.compile(r'\ \([^)]*\)')
            line = re.sub(p, '', line.strip())
            ss = line.split(" ")
            flag = False
            for i, s1 in enumerate(ss):
                if s1.isdigit():
                    country = "_".join(ss[0:i])
                    n1 = int(s1)
                    flag = True
                    break
            if flag:
                data1[country] = n1
            #print country, n1
        return data1

def date2day(files):
    days = [0]
    date_format = "%Y%m%d"
    a = datetime.strptime(files[0].replace(".txt", ""), date_format)
    for f1 in files[1:]:
        f1 = f1.replace(".txt", "")
        b = datetime.strptime(f1, date_format)
        delta = b - a
        d1 = days[-1]
        days.append(d1 + delta.days)
        a = b
    return days

# read sars data
data_path = "/Users/jameszhangj/Desktop/mykidstudy/articles/0-wuhan_virus_map_show/data_sars/"
# get the file list
ff = glob.glob(data_path + "*.txt")
files = sorted([os.path.basename(f1) for f1 in ff])
# read data from all files in the path
data_all = []
for f in files:
    data1 = read_data(data_path + f)
    n1 = sum([data1[i] for i in data1])
    data_all.append(n1)
print data_all
data_all = np.array(data_all)
data_t = date2day(files)
#print zip(data_t, data_all)
ddt = 58
for d in [ddt]:
#for d in range(100):
    tt = [i + d for i in data_t]
    b = np.array(data_all)
    data_y = np.r_[b[0], np.diff(b)]

    nS = 8000
    nI = 1
    nR = 0
    # parameter fitting for SIR model
    def sumsq(p):
        #beta, gamma, sd = p
        beta, gamma = p
        def SIR(t,y):
            S = y[0]
            I = y[1]
            R = y[2]
            return([-beta*S*I, beta*S*I-gamma*I, gamma*I])
        sol = solve_ivp(SIR,[0,200],[nS,nI,nR],t_eval=np.arange(0,200,1))
        #return sum((sol.y[1][tt]-data_y)**2)
        return (sum((np.cumsum(sol.y[1])[tt]-data_all)**2))
        # Calculate negative log likelihood
        #LL = -np.sum( stats.norm.logpdf(data_all, loc=np.cumsum(sol.y[1][data_t]), scale=sd ) )
        #return LL

    #msol = optimize.minimize(sumsq,[0.00001,0.1],method='Nelder-Mead', options={'maxiter':30, 'xatol':10})
    msol = optimize.minimize(sumsq,[0.00001,0.1],method='Nelder-Mead')
    beta,gamma = msol.x
    #msol = optimize.minimize(sumsq,[0.0001,0.1, 1],method='Nelder-Mead')
    #beta,gamma, sd = msol.x
    #print msol.x

    #beta = 0.00001
    #gamma = 2

    def SIR(t,y):
        S = y[0]
        I = y[1]
        R = y[2]
        return([-beta*S*I, beta*S*I-gamma*I, gamma*I])

    sol = solve_ivp(SIR,[0,200],[nS,nI,nR],t_eval=np.arange(0,200,1))
    print d, np.sqrt(sum((np.cumsum(sol.y[1])[tt]-data_all)**2)), msol.x, nS * msol.x[0] / msol.x[1]
    #print np.cumsum(sol.y[1])[tt]
    #print sol.y[1][tt]

fig = plt.figure(dpi=1200)
plt.plot(tt, data_all, color='tab:green', marker='o', markersize="5", linestyle="")
plt.plot(sol.t,np.cumsum(sol.y[1]), color='tab:red', marker='', linestyle="dashed")
plt.legend(["SARS","SIR Model"], loc='upper left')
#plt.legend(["Susceptible","Infected","Removed","Original Data"])
#And plot the resulting curve on the data
plt.xlabel('Days', fontdict={'family': 'serif', 'color':  'black', 'weight': 'normal', 'size': 16})
plt.ylabel('Total Confirmed Cases', fontdict={'family': 'serif', 'color':  'black', 'weight': 'normal', 'size': 16})
plt.subplots_adjust(left=0.16, bottom=0.18)
plt.grid()
plt.savefig("SARS_SIR_fitting_data.png")
#plt.show()
#with open('SIR_data.txt', 'w+') as fp:
#    fp.write('\n'.join('%f %i %i %i' % x for x in SIR_data))
