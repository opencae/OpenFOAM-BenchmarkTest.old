#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import matplotlib as mpl
mpl.use('Agg')
import numpy as np
import pylab
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from optparse import OptionParser

dataorig=np.genfromtxt("table.csv", names=True, delimiter=',', dtype=None)

data=np.sort(dataorig)

plotfile='comparison.pdf'

pp = PdfPages(plotfile)

basename=os.path.basename(os.getcwd())

mpl.rcParams.update({'font.size': 12})

nCellsArray=np.unique(data['nCells'])
LESModelArray=np.unique(data['LESModel'])
solverArray=np.unique(data['solver'])
nProcsArray=np.unique(data['nProcs'])

pylab.subplots_adjust(bottom=0.1)

nCells = 2995200
LESModel = "laminar"
solver = "PCG"
pre = "DIC"
idx=np.where(
    (data['nCells']==nCells)
    & (data['LESModel']==LESModel)
    & (data['solver']==solver)
    & (data['preconditioner']==pre)
)
x=data['nProcs'][idx]
y=data['ExectutionTimeStepss'][idx]

mpi,index0 = np.unique(x, return_index=True)
index1=index0[1:]
index1=np.append(index1,len(y))
executionTimeAve=np.zeros(len(mpi))
executionTimeSTD=np.zeros(len(mpi))
srSTD=np.zeros(len(mpi))
peSTD=np.zeros(len(mpi))
for i in range(len(mpi)):
    executionTime=y[index0[i]:index1[i]]
    executionTimeAve[i]=np.average(executionTime)
    executionTimeSTD[i]=np.std(executionTime)

    sr=executionTimeAve[0]/executionTime
    srSTD[i]=np.std(sr)

    pe=sr/(mpi[i]/mpi[0])*100.0
    peSTD[i]=np.std(pe)

srAve=executionTimeAve[0]/executionTimeAve
peAve=srAve/(mpi/mpi[0])*100

base=str(nCells)+"cells-"+LESModel+"-"+solver+"-"+pre
print base

offset=(mpi[len(mpi)-1]-mpi[0])*0.05
xmin=mpi[0]-offset
xmax=mpi[len(mpi)-1]+offset

plt.title(basename+"\n"+
          str(nCells/1e+6)+"M cells, "+LESModel+" ,"+solver+"-"+pre+")")
plt.xlabel('Number of MPI processes')
plt.xticks(mpi)
plt.grid()
plt.plot(mpi,executionTimeAve, label="Execution time per time step [s]", linewidth=1)
plt.errorbar(mpi, executionTimeAve, yerr=executionTimeSTD, fmt='.', linewidth=2)
plt.ylabel('Execution time per time step [s]')
ymin, ymax = plt.ylim()
ymin=0
plt.xlim(xmin, xmax)
plt.ylim(ymin,ymax*1.1)
pp.savefig()

pp.close()
