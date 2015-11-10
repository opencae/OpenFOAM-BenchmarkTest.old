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

parser = OptionParser()

parser.add_option("-s", "--standard",
                  action="store_true", dest="standard",
                  help="plot cases under standard conditions")

(options, args) = parser.parse_args()

dataorig=np.genfromtxt("table.csv", names=True, delimiter=',', dtype=None)

data=np.sort(dataorig)

if options.standard:
    plotfile='plot-standard.pdf'
else:
    plotfile='plot.pdf'

pp = PdfPages(plotfile)

basename=os.path.basename(os.getcwd())

mpl.rcParams.update({'font.size': 12})

nCellsArray=np.unique(data['nCells'])
LESModelArray=np.unique(data['LESModel'])
solverArray=np.unique(data['solver'])
nProcsArray=np.unique(data['nProcs'])

pylab.subplots_adjust(top=0.83,bottom=0.5)

for nCells in nCellsArray:
    if options.standard and nCells != 2995200:
        continue
    for LESModel in LESModelArray:
        if options.standard and LESModel != "laminar":
            continue
        idxLESModel=np.where(data['LESModel']==LESModel)
        deltaArray=np.unique(data['delta'][idxLESModel])
        for delta in deltaArray:
            idxDelta=np.where(data['delta']==delta)
            calcIntervalArray=np.unique(data['calcInterval'][idxDelta])
            for calcInterval in calcIntervalArray:
                for nProcs in nProcsArray:
                    idx=np.where(
                        (data['nCells']==nCells)
                        & (data['LESModel']==LESModel)
                        & (data['delta']==delta)
                        & (data['calcInterval']==calcInterval)
                        & (data['nProcs']==nProcs)
                        )

                    solver=data['solver'][idx]
                    preconditioner=data['preconditioner'][idx]
                    solvers=np.core.defchararray.add(np.core.defchararray.add(solver, "-"),preconditioner)

                    executionTimePerStep=\
                        (data['ExecutionTimeNextToLastStep'][idx]-data['ExecutionTimeFirstStep'][idx])\
                        /(data['Steps'][idx]-2.0)

                    clockTimePerStep=\
                        (data['ClockTimeNextToLastStep'][idx]-data['ClockTimeFirstStep'][idx])\
                        /(data['Steps'][idx]-2.0)

                    sn = np.unique(solvers)
                    index0=[]
                    for snI in sn:
                        index0.append(np.where(solvers==snI)[0][0])
                    index1=index0[1:]
                    index1=np.append(index1,len(executionTimePerStep))
                    executionTimeAve=np.zeros(len(sn))
                    executionTimeSTD=np.zeros(len(sn))
                    clockTimeAve=np.zeros(len(sn))
                    clockTimeSTD=np.zeros(len(sn))
                    for i in range(len(sn)):
                        executionTime=executionTimePerStep[index0[i]:index1[i]]
                        executionTimeAve[i]=np.average(executionTime)
                        executionTimeSTD[i]=np.std(executionTime)

                        clockTime=clockTimePerStep[index0[i]:index1[i]]
                        clockTimeAve[i]=np.average(clockTime)
                        clockTimeSTD[i]=np.std(clockTime)

                    LESModels=LESModel
                    if LESModel != "laminar":
                        LESModels+=",delta="+delta
                        if delta == "vanDriest":
                            LESModels+=",calcInterval="+str(calcInterval)

                    base=str(nCells)+"cells-"+LESModels+"-"+str(nProcs)+"MPI-time"
                    print base

                    x=np.arange(len(sn))

                    offset=(x[len(x)-1]-x[0])*0.05
                    xmin=x[0]-offset
                    xmax=x[len(x)-1]+offset

                    title=basename+"\n"+str(nCells/1e+6)+"M cells\n"+LESModels+"\n"+str(nProcs)+"MPI"
                    plt.title(title)
                    plt.errorbar(x, executionTimeAve, yerr=executionTimeSTD, label="Execution time per time step [s]")
                    plt.errorbar(x, clockTimeAve, yerr=clockTimeSTD, label="clock time per time step [s]")
                    plt.xlabel('Matrix solver for pressure equation')
                    plt.ylabel('Execution or clock time per time step [s]')
                    plt.xticks(x,sn, rotation=-90)
                    ymin, ymax = plt.ylim()
                    ymin=0
                    plt.xlim(xmin, xmax)
                    plt.ylim(ymin,ymax*1.1)
                    plt.grid()
                    plt.legend(loc='best', fontsize=12)
                    pp.savefig()
                    plt.clf()

if len(nProcsArray)==1:
    pp.close()
    exit(0)

pylab.subplots_adjust(top=0.83,bottom=0.1)

for nCells in nCellsArray:
    if options.standard and nCells != 2995200:
        continue
    for LESModel in LESModelArray:
        if options.standard and LESModel != "laminar":
            continue
        idxLESModel=np.where(data['LESModel']==LESModel)
        deltaArray=np.unique(data['delta'][idxLESModel])
        for delta in deltaArray:
            idxDelta=np.where(data['delta']==delta)
            calcIntervalArray=np.unique(data['calcInterval'][idxDelta])
            for calcInterval in calcIntervalArray:
                for solver in solverArray:
                    if options.standard and solver != "PCG":
                        continue
                    idxSolver=np.where(data['solver']==solver)
                    preArray=np.unique(data['preconditioner'][idxSolver])
                    for pre in preArray:
                        if options.standard and pre != "DIC":
                            continue
                        idx=np.where(
                            (data['nCells']==nCells)
                            & (data['LESModel']==LESModel)
                            & (data['solver']==solver)
                            & (data['delta']==delta)
                            & (data['calcInterval']==calcInterval)
                            & (data['preconditioner']==pre)
                            )
                        x=data['nProcs'][idx]

                        executionTimePerStep=\
                            (data['ExecutionTimeNextToLastStep'][idx]-data['ExecutionTimeFirstStep'][idx])\
                            /(data['Steps'][idx]-2.0)

                        clockTimePerStep=\
                            (data['ClockTimeNextToLastStep'][idx]-data['ClockTimeFirstStep'][idx])\
                            /(data['Steps'][idx]-2.0)

                        mpi = np.unique(x)
                        index0=[]
                        for mpiI in mpi:
                            index0.append(np.where(x==mpiI)[0][0])
                        index1=index0[1:]
                        index1=np.append(index1,len(executionTimePerStep))
                        executionTimeAve=np.zeros(len(mpi))
                        executionTimeSTD=np.zeros(len(mpi))
                        clockTimeAve=np.zeros(len(mpi))
                        clockTimeSTD=np.zeros(len(mpi))
                        executionTimeSRSTD=np.zeros(len(mpi))
                        executionTimePESTD=np.zeros(len(mpi))
                        clockTimeSRSTD=np.zeros(len(mpi))
                        clockTimePESTD=np.zeros(len(mpi))
                        for i in range(len(mpi)):
                            executionTime=executionTimePerStep[index0[i]:index1[i]]
                            executionTimeAve[i]=np.average(executionTime)
                            executionTimeSTD[i]=np.std(executionTime)

                            clockTime=clockTimePerStep[index0[i]:index1[i]]
                            clockTimeAve[i]=np.average(clockTime)
                            clockTimeSTD[i]=np.std(clockTime)

                            executionTimeSR=executionTimeAve[0]/executionTime
                            executionTimeSRSTD[i]=np.std(executionTimeSR)
                            executionTimePE=executionTimeSR/(mpi[i]/mpi[0])*100.0
                            executionTimePESTD[i]=np.std(executionTimePE)

                            clockTimeSR=clockTimeAve[0]/clockTime
                            clockTimeSRSTD[i]=np.std(clockTimeSR)
                            clockTimePE=clockTimeSR/(mpi[i]/mpi[0])*100.0
                            clockTimePESTD[i]=np.std(clockTimePE)

                        executionTimeSRAve=executionTimeAve[0]/executionTimeAve
                        executionTimePEAve=executionTimeSRAve/(mpi/mpi[0])*100

                        clockTimeSRAve=clockTimeAve[0]/clockTimeAve
                        clockTimePEAve=clockTimeSRAve/(mpi/mpi[0])*100

                        LESModels=LESModel
                        if LESModel != "laminar":
                            LESModels+=",delta="+delta
                            if delta == "vanDriest":
                                LESModels+=",calcInterval="+str(calcInterval)

                        base=str(nCells)+"cells-"+LESModels+"-"+solver+"-"+pre
                        print base

                        offset=(mpi[len(mpi)-1]-mpi[0])*0.05
                        xmin=mpi[0]-offset
                        xmax=mpi[len(mpi)-1]+offset

                        title=basename+"\n"+str(nCells/1e+6)+"M cells\n"+LESModels+"\n"+solver+"-"+pre
                        plt.title(title)
                        plt.xlabel('Number of MPI processes')
                        plt.xticks(mpi)
                        plt.grid()
                        plt.errorbar(mpi, executionTimeAve, yerr=executionTimeSTD, label="Execution time per time step [s]")
                        plt.errorbar(mpi, clockTimeAve, yerr=clockTimeSTD, label="Clock time per time step [s]")
                        plt.ylabel('Execution time per time step [s]')
                        ymin, ymax = plt.ylim()
                        ymin=0
                        plt.xlim(xmin, xmax)
                        plt.ylim(ymin,ymax*1.1)
                        plt.legend(loc='best', fontsize=12)
                        pp.savefig()
                        plt.clf()

                        plt.title(title)
                        plt.xlabel('Number of MPI processes')
                        plt.xticks(mpi)
                        plt.grid()
                        plt.errorbar(mpi, executionTimeSRAve, executionTimeSRSTD, label="Execution time base")
                        plt.errorbar(mpi, clockTimeSRAve, clockTimeSRSTD, label="Clock Time base")
                        plt.plot([xmin, xmax], [xmin/mpi[0], xmax/mpi[0]], 'k-', label="Ideal")
                        plt.ylabel('Speedup ratio [-]')
                        ymin, ymax = plt.ylim()
                        ymin=0
                        plt.xlim(xmin, xmax)
                        plt.ylim(ymin,ymax*1.1)
                        plt.legend(loc='best', fontsize=12)
                        pp.savefig()
                        plt.clf()

                        plt.title(title)
                        plt.xlabel('Number of MPI processes')
                        plt.xticks(mpi)
                        plt.grid()
                        plt.errorbar(mpi, executionTimePEAve, executionTimePESTD, label="Execution time base")
                        plt.errorbar(mpi, clockTimePEAve, clockTimePESTD, label="Clock time base")
                        plt.plot([xmin, xmax], [100, 100], 'k-', label="Ideal")
                        plt.ylabel('Parallel efficiency [%]')
                        xmin, xmax = plt.xlim()
                        ymin, ymax = plt.ylim()
                        ymin=0
                        plt.ylim(ymin,ymax*1.1)
                        plt.legend(loc='best', fontsize=12)
                        pp.savefig()
                        plt.clf()

pp.close()

