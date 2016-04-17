#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import matplotlib as mpl
mpl.use('Agg')
import numpy as np
import pylab
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import csv
from scipy import stats

nMaxSample=5

data=np.genfromtxt("table.csv", names=True, delimiter=',', dtype=None)

plotfile='plot.pdf'

pp = PdfPages(plotfile)

basename=os.path.basename(os.getcwd())

mpl.rcParams.update({'font.size': 12})

nCellsArray=np.unique(data['nCells'])
LESModelArray=np.unique(data['LESModel'])
solverArray=np.unique(data['solver'])
nProcsArray=np.unique(data['nProcs'])
values = []

pylab.subplots_adjust(top=0.83,bottom=0.5)

for nCells in nCellsArray:
    for LESModel in LESModelArray:
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
                    clockTimeM=np.zeros(len(sn))
                    clockTimeSTD=np.zeros(len(sn))
                    for i in range(len(sn)):
                        executionTime=executionTimePerStep[index0[i]:index1[i]]
                        executionTime=np.sort(executionTime)[0:min(len(executionTime),nMaxSample)]
                        executionTimeAve[i]=np.average(executionTime)
                        executionTimeSTD[i]=np.std(executionTime)

                        clockTime=clockTimePerStep[index0[i]:index1[i]]
                        clockTime=np.sort(clockTime)[0:min(len(clockTime),nMaxSample)]
                        clockTimeAve[i]=np.average(clockTime)
                        clockTimeSTD[i]=np.std(clockTime)

                        values.append((0,nProcs,sn[i],executionTimeAve[i],clockTimeAve[i]\
                                           ,executionTimeAve[i],clockTimeAve[i]))

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

#                    title=basename+"\n"+str(nCells/1e+6)+"M cells\n"+LESModels+"\n"+str(nProcs)+"MPI"
#                    plt.title(title)
#                    plt.errorbar(x, executionTimeAve, yerr=executionTimeSTD, color='b', ecolor='b'\
#                                     , label="Execution time per time step [s]")
#                    plt.xlabel('Matrix solver for pressure equation')
#                    plt.xticks(x,sn, rotation=-90)
#                    ymin, ymax = plt.ylim()
#                    ymin=0
#                    plt.xlim(xmin, xmax)
#                    plt.ylim(ymin,ymax*1.1)
#                    plt.grid()
#                    plt.legend(loc='best', fontsize=12)
#                    plt.ylabel('Execution time per time step [s]')
#                    pp.savefig()
#                    plt.clf()

                    title=basename+"\n"+str(nCells/1e+6)+"M cells\n"+LESModels+"\n"+str(nProcs)+"MPI"
                    plt.title(title)
                    plt.errorbar(x, clockTimeAve, yerr=clockTimeSTD, color='r', ecolor='r'\
                                     , label="Clock time per time step [s]")
                    plt.xlabel('Matrix solver for pressure equation')
                    plt.xticks(x,sn, rotation=-90)
                    ymin, ymax = plt.ylim()
                    ymin=0
                    plt.xlim(xmin, xmax)
                    plt.ylim(ymin,ymax*1.1)
                    plt.grid()
                    plt.legend(loc='best', fontsize=12)
                    plt.ylabel('Clock time per time step [s]')
                    pp.savefig()
                    plt.clf()

dtype =\
 [('#No', int), ('nProcs', int), ('solver', 'S100')\
  , ('executionTimePerTimeStepAve', float), ('clockTimePerTimeStepAve', float)\
  , ('executionTimePerTimeStepAve/No1', float), ('clockTimePerTimeStepAve/No1', float)\
      ]
timeAve = np.array(values, dtype=dtype)

header=["#No","nProcs","solver"\
            ,"executionTimePerTimeStepAve[s]","clockTimePerTimeStepAve[s]"\
            ,"executionTimePerTimeStepAve/No1","clockTimePerTimeStepAve/No1"]
ETPTAsort=np.sort(timeAve, order='executionTimePerTimeStepAve')
no=1
for ETPTAsortI in ETPTAsort:
    ETPTAsortI['#No']=no
    ETPTAsortI['executionTimePerTimeStepAve/No1']\
        /=ETPTAsort['executionTimePerTimeStepAve'][0]
    ETPTAsortI['clockTimePerTimeStepAve/No1']\
        /=ETPTAsort['clockTimePerTimeStepAve'][0]
    no+=1
f = open('executionTimeAve.csv', 'w')
writer = csv.writer(f, lineterminator='\n')
writer.writerow(header)
writer.writerows(ETPTAsort)
f.close()

CTPTSAsort=np.sort(timeAve, order='clockTimePerTimeStepAve')
no=1
for CTPTSAsortI in CTPTSAsort:
    CTPTSAsortI['#No']=no
    CTPTSAsortI['executionTimePerTimeStepAve/No1']\
        /=CTPTSAsort['executionTimePerTimeStepAve'][0]
    CTPTSAsortI['clockTimePerTimeStepAve/No1']\
        /=CTPTSAsort['clockTimePerTimeStepAve'][0]
    no+=1
f = open('clockTimeAve.csv', 'w')
writer = csv.writer(f, lineterminator='\n')
writer.writerow(header)
writer.writerows(CTPTSAsort)
f.close()

if len(nProcsArray)==1:
    pp.close()
    exit(0)

pylab.subplots_adjust(top=0.83,bottom=0.1)

for nCells in nCellsArray:
    for LESModel in LESModelArray:
        idxLESModel=np.where(data['LESModel']==LESModel)
        deltaArray=np.unique(data['delta'][idxLESModel])
        for delta in deltaArray:
            idxDelta=np.where(data['delta']==delta)
            calcIntervalArray=np.unique(data['calcInterval'][idxDelta])
            for calcInterval in calcIntervalArray:
                for solver in solverArray:
                    idxSolver=np.where(data['solver']==solver)
                    preArray=np.unique(data['preconditioner'][idxSolver])
                    for pre in preArray:
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
                        nTimeStepPerDayAve=np.zeros(len(mpi))
                        executionTimeSRSTD=np.zeros(len(mpi))
                        executionTimePESTD=np.zeros(len(mpi))
                        clockTimeSRSTD=np.zeros(len(mpi))
                        clockTimePESTD=np.zeros(len(mpi))
                        for i in range(len(mpi)):
                            executionTime=executionTimePerStep[index0[i]:index1[i]]
                            executionTime=np.sort(executionTime)[0:min(len(executionTime),nMaxSample)]
                            executionTimeAve[i]=np.average(executionTime)
                            executionTimeSTD[i]=np.std(executionTime)

                            clockTime=clockTimePerStep[index0[i]:index1[i]]
                            clockTime=np.sort(clockTime)[0:min(len(clockTime),nMaxSample)]
                            clockTimeAve[i]=np.average(clockTime)
                            clockTimeSTD[i]=np.std(clockTime)

                            nTimeStepPerDayAve[i]=3600.0/clockTimeAve[i]

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

#                        title=basename+"\n"+str(nCells/1e+6)+"M cells\n"+LESModels+"\n"+solver+"-"+pre
#                        plt.title(title)
#                        plt.xlabel('Number of MPI processes')
#                        plt.xticks(mpi)
#                        plt.grid()
#                        plt.errorbar(mpi, executionTimeAve, yerr=executionTimeSTD, color='b', ecolor='b'\
#                                         , label="Execution time per time step [s]")
#                        plt.ylabel('Execution time per time step [s]')
#                        ymin, ymax = plt.ylim()
#                        ymin=0
#                        plt.xlim(xmin, xmax)
#                        plt.ylim(ymin,ymax*1.1)
#                        plt.legend(loc='best', fontsize=12)
#                        pp.savefig()
#                        plt.clf()

                        title=basename+"\n"+str(nCells/1e+6)+"M cells\n"+LESModels+"\n"+solver+"-"+pre
                        plt.title(title)
                        plt.xlabel('Number of MPI processes')
                        plt.xticks(mpi)
                        plt.grid()
                        plt.errorbar(mpi, clockTimeAve, yerr=clockTimeSTD, color='r', ecolor='r'\
                                         , label="Clock time per time step [s]")
                        plt.ylabel('Clock time per time step [s]')
                        ymin, ymax = plt.ylim()
                        ymin=0
                        plt.xlim(xmin, xmax)
                        plt.ylim(ymin,ymax*1.1)
                        plt.legend(loc='best', fontsize=12)
                        pp.savefig()
                        plt.clf()

                        title=basename+"\n"+str(nCells/1e+6)+"M cells\n"+LESModels+"\n"+solver+"-"+pre
                        plt.title(title)
                        plt.xlabel('Number of MPI processes')
                        plt.xticks(mpi)
                        plt.grid()
                        plt.plot(mpi, nTimeStepPerDayAve, 'r-', label="Number of time steps per hour")
                        plt.plot([xmin, xmax]\
                                     ,[xmin*(nTimeStepPerDayAve[0]/mpi[0]), xmax*(nTimeStepPerDayAve[0]/mpi[0])]\
                                           ,'k-', label="Ideal")
                        plt.ylabel('Number of time steps per hour')
                        ymin, ymax = plt.ylim()
                        ymin=0
                        plt.xlim(xmin, xmax)
                        plt.ylim(ymin,ymax*1.1)
                        plt.legend(loc='best', fontsize=12)
                        pp.savefig()
                        plt.clf()

#                        plt.title(title)
#                        plt.xlabel('Number of MPI processes')
#                        plt.xticks(mpi)
#                        plt.grid()
#                        plt.errorbar(mpi, executionTimeSRAve, executionTimeSRSTD, color='b', ecolor='b'\
#                                         , label="Execution time base")
#                        plt.plot([xmin, xmax], [xmin/mpi[0], xmax/mpi[0]], 'k-', label="Ideal")
#                        plt.ylabel('Speedup ratio [-]')
#                        ymin, ymax = plt.ylim()
#                        ymin=0
#                        plt.xlim(xmin, xmax)
#                        plt.ylim(ymin,ymax*1.1)
#                        plt.legend(loc='best', fontsize=12)
#                        pp.savefig()
#                        plt.clf()

                        plt.title(title)
                        plt.xlabel('Number of MPI processes')
                        plt.xticks(mpi)
                        plt.grid()
                        plt.errorbar(mpi, clockTimeSRAve, clockTimeSRSTD, color='r', ecolor='r'\
                                         , label="Clock Time base")
                        plt.plot([xmin, xmax], [xmin/mpi[0], xmax/mpi[0]], 'k-', label="Ideal")
                        plt.ylabel('Speedup ratio [-]')
                        ymin, ymax = plt.ylim()
                        ymin=0
                        plt.xlim(xmin, xmax)
                        plt.ylim(ymin,ymax*1.1)
                        plt.legend(loc='best', fontsize=12)
                        pp.savefig()
                        plt.clf()

#                        plt.title(title)
#                        plt.xlabel('Number of MPI processes')
#                        plt.xticks(mpi)
#                        plt.grid()
#                        plt.errorbar(mpi, executionTimePEAve, executionTimePESTD, color='b', ecolor='b'\
#                                         , label="Execution time base")
#                        plt.plot([xmin, xmax], [100, 100], 'k-', label="Ideal")
#                        plt.ylabel('Parallel efficiency [%]')
#                        xmin, xmax = plt.xlim()
#                        ymin, ymax = plt.ylim()
#                        ymin=0
#                        plt.ylim(ymin,ymax*1.1)
#                        plt.legend(loc='best', fontsize=12)
#                        pp.savefig()
#                        plt.clf()

                        plt.title(title)
                        plt.xlabel('Number of MPI processes')
                        plt.xticks(mpi)
                        plt.grid()
                        plt.errorbar(mpi, clockTimePEAve, clockTimePESTD, color='r', ecolor='r'\
                                         , label="Clock time base")
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
