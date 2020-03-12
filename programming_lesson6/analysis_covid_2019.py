# -*- coding:utf-8 -*-
import re
import glob
import os
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
            for i, s1 in enumerate(ss):
                if s1.isdigit():
                    country = "_".join(ss[0:i])
                    n1 = int(s1)
                    break
            data1[country] = n1
            #print country, n1
        return data1

def date2day(files):
    days = [0]
    dates = []
    date_format = "%Y%m%d"
    a = datetime.strptime(files[0].replace(".txt", ""), date_format)
    #dates.append(a.strftime('%Y-%m-%d'))
    dates.append(a.strftime('%m-%d'))
    for f1 in files[1:]:
        f1 = f1.replace(".txt", "")
        b = datetime.strptime(f1, date_format)
        delta = b - a
        d1 = days[-1]
        days.append(d1 + delta.days)
        a = b
        #dates.append(b.strftime('%Y-%m-%d'))
        dates.append(b.strftime('%m-%d'))
    return days, dates


data_path = "/Users/jameszhangj/Desktop/mykidstudy/articles/0-wuhan_virus_map_show/data/"
# get the file list
ff = glob.glob(data_path + "*.txt")
files = sorted([os.path.basename(f1) for f1 in ff])
# read data from all files in the path
n_china = []
n_out_china = []
for f in files:
    data1 = read_data(data_path + f)
    n_china.append(data1["China"])
    n_all = sum([data1[i] for i in data1])
    n_out_china.append(n_all - data1["China"])
print n_china
print n_out_china

# plot data
from matplotlib import pyplot as plt
#t = [x for x in range(len(n_china))]
t, dates = date2day(files)

plt.figure(dpi=1200)
#plt.plot(t, n_china, color='tab:red', marker='o', linestyle='dashed')
#plt.plot(t, n_out_china, color='tab:blue', marker='o', linestyle='dashed')
#plt.plot(t, n_china, color='tab:red', marker='o', markersize="3", linestyle='-', linewidth="1.5")
#plt.plot(t, n_out_china, color='tab:blue', marker='o', markersize="3", linestyle='-', linewidth="1.5")
plt.plot(t, n_china, color='tab:red', marker='o', linestyle='-')
plt.plot(t, n_out_china, color='tab:blue', marker='o', linestyle='-')
plt.legend(('China', 'Oversea'), loc='upper left')
plt.xticks(t[::5], dates[::5], rotation=60)
#plt.margins(0.2)
plt.xlabel('Date', fontdict={'family': 'serif', 'color':  'black', 'weight': 'normal', 'size': 16})
plt.ylabel('Total Confirmed Cases', fontdict={'family': 'serif', 'color':  'black', 'weight': 'normal', 'size': 16})
plt.subplots_adjust(left=0.16, bottom=0.18)
plt.grid()
plt.savefig("china_vs_oversea_raw_data.png")

# fitting SIR model
plt.clf()
data_all = np.array(n_china)
data_t = np.array(t)
#print zip(data_t, data_all)
ddt = 23
for d in [ddt]:
#for d in range(150):
    tt = [i + d for i in data_t]
    b = np.array(data_all)
    data_y = np.r_[b[0], np.diff(b)]

    nS = 80000
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
        sol = solve_ivp(SIR,[0,125 + ddt],[nS,nI,nR],t_eval=np.arange(0,125 + ddt,1))
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

    sol = solve_ivp(SIR,[0,125 + ddt],[nS,nI,nR],t_eval=np.arange(0,125 + ddt,1))
    print d, np.sqrt(sum((np.cumsum(sol.y[1])[tt]-data_all)**2)), msol.x, nS * msol.x[0] / msol.x[1]
    #print np.cumsum(sol.y[1])[tt]
    #print sol.y[1][tt]

fig = plt.figure(dpi=1200)
#plt.legend(["Susceptible","Infected","Removed","Cumulative Infected","Original Data", "Original Data I"])
#plt.legend(["Susceptible","Infected","Removed","Original Data"])
#And plot the resulting curve on the data
plt.plot(t, n_china, color='tab:red', marker='o', markersize="2", linestyle="")
plt.plot(t, n_out_china, color='tab:blue', marker='o', markersize="2", linestyle="")
plt.plot(sol.t[ddt:] - ddt,np.cumsum(sol.y[1])[ddt:], color='tab:red', marker='', linestyle="dashed")
#with open('SIR_data.txt', 'w+') as fp:
#    fp.write('\n'.join('%f %i %i %i' % x for x in SIR_data))

data_all = np.array(n_out_china)
data_t = np.array(t)
#print zip(data_t, data_all)
for d in [0]:
#for d in range(150):
    tt = [i + d for i in data_t]
    b = np.array(data_all)
    data_y = np.r_[b[0], np.diff(b)]

    nS = 80000
    #nS = 175000
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
        sol = solve_ivp(SIR,[0,125],[nS,nI,nR],t_eval=np.arange(0,125,1))
        #return sum((sol.y[1][tt]-data_y)**2)
        return (sum((np.cumsum(sol.y[1])[tt]-data_all)**2))
        # Calculate negative log likelihood
        #LL = -np.sum( stats.norm.logpdf(data_all, loc=np.cumsum(sol.y[1][data_t]), scale=sd ) )
        #return LL

    msol = optimize.minimize(sumsq,[0.00001,0.1],method='Nelder-Mead', options={'maxiter':30, 'xatol':10})
    #msol = optimize.minimize(sumsq,[0.00001,0.1],method='Nelder-Mead', options={'maxiter':40, 'xatol':10})
    #msol = optimize.minimize(sumsq,[0.00001,0.1],method='Nelder-Mead')
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

    sol = solve_ivp(SIR,[0,125],[nS,nI,nR],t_eval=np.arange(0,125,1))
    print d, np.sqrt(sum((np.cumsum(sol.y[1])[tt]-data_all)**2)), msol.x, nS * msol.x[0] / msol.x[1]
    #print np.cumsum(sol.y[1])[tt]
    #print sol.y[1][tt]

plt.plot(sol.t,np.cumsum(sol.y[1]),color='tab:blue', marker='', linestyle="dashed")
#plt.legend(["Susceptible","Infected","Removed","Original Data"])
#And plot the resulting curve on the data
plt.legend(('China', 'Oversea', "China SIR Model", "Oversea SIR Model"), loc='upper left')
#plt.xticks(data_t[::5], dates[::5], rotation=60)
#plt.margins(0.2)
plt.xlabel('Days', fontdict={'family': 'serif', 'color':  'black', 'weight': 'normal', 'size': 16})
plt.ylabel('Total Confirmed Cases', fontdict={'family': 'serif', 'color':  'black', 'weight': 'normal', 'size': 16})
plt.subplots_adjust(left=0.16, bottom=0.18)
plt.grid()
plt.savefig("china_vs_oversea_SIR_fitting_data.png")
#with open('SIR_data.txt', 'w+') as fp:
#    fp.write('\n'.join('%f %i %i %i' % x for x in SIR_data))
