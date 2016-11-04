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
import sys

def solverExecutionTimePerStep(column,ylabel):
    pylab.subplots_adjust(top=0.95,bottom=0.45)

    for decomposeParDict in decomposeParDictArray:
        title=decomposeParDict
        plotfile=plotfileBase+'-'+title+'-'+column+'.pdf'
        pp = PdfPages(plotfile)
        print plotfile

        for batchFileName in batchFileNameArray:
            idx=np.where(
                (data['decomposeParDict']==decomposeParDict)
                & (data['solveBatch']==batchFileName)
                )

            solver=data['fvSolution'][idx]

            ExecutionTimePerStep=data[column][idx]

            sn = np.unique(solver)
            index0=[]
            for snI in sn:
                index0.append(np.where(solver==snI)[0][0])
            index1=index0[1:]
            index1=np.append(index1,len(ExecutionTimePerStep))
            ExecutionTimeAve=np.zeros(len(sn))
            if nMaxSample>1:
                ExecutionTimeSTD=np.zeros(len(sn))
            for i in range(len(sn)):
                ExecutionTime=ExecutionTimePerStep[index0[i]:index1[i]]
                ExecutionTime=np.sort(ExecutionTime)[0:min(len(ExecutionTime),nMaxSample)]
                ExecutionTimeAve[i]=np.average(ExecutionTime)
                if nMaxSample>1:
                    ExecutionTimeSTD[i]=np.std(ExecutionTime)

            x=np.arange(len(sn))

            offset=(x[len(x)-1]-x[0])*0.05
            xmin=x[0]-offset
            xmax=x[len(x)-1]+offset

            if nMaxSample>1:
                plt.errorbar(x, ExecutionTimeAve, yerr=ExecutionTimeSTD, label=batchFileName\
                             , linewidth=2)
            else:
                plt.plot(x, ExecutionTimeAve, label=batchFileName, linewidth=2)

        plt.title(title)
        plt.xticks(x,sn, rotation=-90)
        plt.grid()
        ymin, ymax = plt.ylim()
        ymin=0
        plt.xlim(xmin, xmax)
        plt.ylim(ymin, ymax)
        plt.legend(loc='best', prop={'size':fontSizeLegend})
        plt.ylabel(ylabel)
        pp.savefig()
        plt.clf()
        pp.close()

def mpiFirstExecutionTimePerStep(column,ylabel,yscalelog=False):
    pylab.subplots_adjust(top=0.95,bottom=0.1)

    for solver in solverArray:
        for method in methodArray:
            title=solver+'-method_'+method
            plotfile=plotfileBase+'-'+title+'-1stTime-'+column
            if yscalelog:
                plotfile=plotfile+'-log'
            else:
                plotfile=plotfile+'-linear'
            plotfile=plotfile+'.pdf'
            pp = PdfPages(plotfile)
            print plotfile
    
            for batchFileName in batchFileNameArray:
                idx=np.where(
                    (data['method']==method)
                    & (data['fvSolution']==solver)
                    & (data['solveBatch']==batchFileName)
                    )
    
                x=data['nProcs'][idx]
    
                ExecutionTimeFirstStep=data[column][idx]
    
                mpi = np.unique(x)
                index0=[]
                for mpiI in mpi:
                    index0.append(np.where(x==mpiI)[0][0])
                index1=index0[1:]
                index1=np.append(index1,len(ExecutionTimeFirstStep))
                ExecutionTimeFirstStepAve=np.zeros(len(mpi))
                ExecutionTimeFirstStepSTD=np.zeros(len(mpi))
                for i in range(len(mpi)):
                    ExecutionTimeFS=ExecutionTimeFirstStep[index0[i]:index1[i]]
                    ExecutionTimeFS=np.sort(ExecutionTimeFS)[0:min(len(ExecutionTimeFS),nMaxSample)]
                    ExecutionTimeFirstStepAve[i]=np.average(ExecutionTimeFS)
                    ExecutionTimeFirstStepSTD[i]=np.std(ExecutionTimeFS)
    
                if nMaxSample>1:
                    plt.errorbar(mpi, ExecutionTimeFirstStepAve, yerr=ExecutionTimeFirstStepSTD, label=batchFileName\
                                 , linewidth=2)
                else:
                    plt.plot(mpi, ExecutionTimeFirstStepAve, label=batchFileName, linewidth=2)
    
            xmin=mpi[0]/1.1
            xmax=mpi[-1]*1.1
    
            plt.legend(loc='best', prop={'size':fontSizeLegend})
            plt.xscale('log')
            plt.title(title)
            plt.xlabel('Number of MPI processes')
            plt.ylabel(ylabel)
            plt.xticks(mpi,mpi)
            plt.grid()
            ymin, ymax = plt.ylim()
            if yscalelog:
                plt.yscale('log')
            else:
                ymin=0
            plt.xlim(xmin, xmax)
            plt.ylim(ymin, ymax)
            pp.savefig()
            plt.clf()
            pp.close()
    
def mpiExecutionTimePerStep(column,ylabel,yscalelog=False):
    pylab.subplots_adjust(top=0.95,bottom=0.1)

    for solver in solverArray:
        for method in methodArray:
            title=solver+'-method_'+method
            plotfile=plotfileBase+'-'+title+'-loopTime-'+column
            if yscalelog:
                plotfile=plotfile+'-log'
            else:
                plotfile=plotfile+'-linear'
            plotfile=plotfile+'.pdf'
            pp = PdfPages(plotfile)
            print plotfile
    
            for batchFileName in batchFileNameArray:
                idx=np.where(
                    (data['method']==method)
                    & (data['fvSolution']==solver)
                    & (data['solveBatch']==batchFileName)
                    )
    
                x=data['nProcs'][idx]
    
                ExecutionTimePerStep=data[column][idx]
    
                mpi = np.unique(x)
                index0=[]
                for mpiI in mpi:
                    index0.append(np.where(x==mpiI)[0][0])
                index1=index0[1:]
                index1=np.append(index1,len(ExecutionTimePerStep))
                ExecutionTimeAve=np.zeros(len(mpi))
                ExecutionTimeSTD=np.zeros(len(mpi))
                for i in range(len(mpi)):
                    ExecutionTime=ExecutionTimePerStep[index0[i]:index1[i]]
                    ExecutionTime=np.sort(ExecutionTime)[0:min(len(ExecutionTime),nMaxSample)]
                    ExecutionTimeAve[i]=np.average(ExecutionTime)
                    ExecutionTimeSTD[i]=np.std(ExecutionTime)
    
                if nMaxSample>1:
                    plt.errorbar(mpi, ExecutionTimeAve, yerr=ExecutionTimeSTD, label=batchFileName\
                                 , linewidth=2)
                else:
                    plt.plot(mpi, ExecutionTimeAve, label=batchFileName,linewidth=2)
    
            xmin=mpi[0]/1.1
            xmax=mpi[-1]*1.1
    
            plt.legend(loc='best', prop={'size':fontSizeLegend})
            plt.xscale('log')
            plt.title(title)
            plt.xlabel('Number of MPI processes')
            plt.ylabel(ylabel)
            plt.xticks(mpi,mpi)
            plt.grid()
            ymin, ymax = plt.ylim()
            if yscalelog:
                plt.yscale('log')
            else:
                ymin=0
            plt.xlim(xmin, xmax)
            plt.ylim(ymin, ymax)
            pp.savefig()
            plt.clf()
            pp.close()
    
def mpiNumberOfStepsPerHour(column,ylabel,yscalelog=False):
    pylab.subplots_adjust(top=0.95,bottom=0.1)

    for solver in solverArray:
        for method in methodArray:
            title=solver+'-method_'+method
            plotfile=plotfileBase+'-'+title+'-sph-'+column
            if yscalelog:
                plotfile=plotfile+'-log'
            else:
                plotfile=plotfile+'-linear'
            plotfile=plotfile+'.pdf'
            pp = PdfPages(plotfile)
            print plotfile
    
            for batchFileName in batchFileNameArray:
                idx=np.where(
                    (data['method']==method)
                    & (data['fvSolution']==solver)
                    & (data['solveBatch']==batchFileName)
                    )
    
                x=data['nProcs'][idx]
    
                ExecutionTimePerStep=data[column][idx]
    
                mpi = np.unique(x)
                index0=[]
                for mpiI in mpi:
                    index0.append(np.where(x==mpiI)[0][0])
                index1=index0[1:]
                index1=np.append(index1,len(ExecutionTimePerStep))
                ExecutionTimeAve=np.zeros(len(mpi))
                ExecutionTimeSTD=np.zeros(len(mpi))
                numberOfStepsPerHourAve=np.zeros(len(mpi))
                numberOfStepsPerHourSTD=np.zeros(len(mpi))
                for i in range(len(mpi)):
                    ExecutionTime=ExecutionTimePerStep[index0[i]:index1[i]]
                    ExecutionTime=np.sort(ExecutionTime)[0:min(len(ExecutionTime),nMaxSample)]
                    ExecutionTimeAve[i]=np.average(ExecutionTime)
                    ExecutionTimeSTD[i]=np.std(ExecutionTime)
                    numberOfStepsPerHourAve[i]=3600.0/ExecutionTimeAve[i]
                    numberOfStepsPerHourSTD[i]=np.std(3600.0/ExecutionTime)

                if nMaxSample>1:
                    plt.errorbar(mpi, numberOfStepsPerHourAve, yerr=numberOfStepsPerHourSTD
                                 , label=batchFileName, linewidth=2)
                else:
                    plt.plot(mpi, numberOfStepsPerHourAve, label=batchFileName, linewidth=2)
    
            xmin=mpi[0]/1.1
            xmax=mpi[-1]*1.1
    
            plt.legend(loc='best', prop={'size':fontSizeLegend})
            plt.xscale('log')
            plt.title(title)
            plt.xlabel('Number of MPI processes')
            plt.ylabel(ylabel)
            plt.xticks(mpi,mpi)
            plt.grid()
            ymin, ymax = plt.ylim()
            if yscalelog:
                plt.yscale('log')
            else:
                ymin=0
            plt.xlim(xmin, xmax)
            plt.ylim(ymin, ymax)
            pp.savefig()
            plt.clf()
            pp.close()
    
def mpiParallelEfficiency(column,ylabel):
    pylab.subplots_adjust(top=0.95,bottom=0.1)

    for solver in solverArray:
        for method in methodArray:
            title=solver+'-method_'+method
            plotfile=plotfileBase+'-'+title+'-pe-'+column+'.pdf'
            pp = PdfPages(plotfile)
            print plotfile
    
            for batchFileName in batchFileNameArray:
                idx=np.where(
                    (data['method']==method)
                    & (data['fvSolution']==solver)
                    & (data['solveBatch']==batchFileName)
                    )
    
                x=data['nProcs'][idx]
    
                ExecutionTimePerStep=data[column][idx]
    
                mpi = np.unique(x)
                index0=[]
                for mpiI in mpi:
                    index0.append(np.where(x==mpiI)[0][0])
                index1=index0[1:]
                index1=np.append(index1,len(ExecutionTimePerStep))
                ExecutionTimeAve=np.zeros(len(mpi))
                ExecutionTimePESTD=np.zeros(len(mpi))
                for i in range(len(mpi)):
                    ExecutionTime=ExecutionTimePerStep[index0[i]:index1[i]]
                    ExecutionTime=np.sort(ExecutionTime)[0:min(len(ExecutionTime),nMaxSample)]
                    ExecutionTimeAve[i]=np.average(ExecutionTime)
    
                    ExecutionTimePE=ExecutionTimeAve[0]/ExecutionTime/(mpi[i]/mpi[0])*100.0
                    ExecutionTimePESTD[i]=np.std(ExecutionTimePE)
    
                ExecutionTimePEAve=ExecutionTimeAve[0]/ExecutionTimeAve/(mpi/mpi[0])*100
    
                if nMaxSample>1:
                    plt.errorbar(mpi, ExecutionTimePEAve, yerr=ExecutionTimePESTD, label=batchFileName\
                                 , linewidth=2)
                else:
                    plt.plot(mpi, ExecutionTimePEAve, label=batchFileName, linewidth=2)
    
            xmin=mpi[0]/1.1
            xmax=mpi[-1]*1.1
    
            plt.plot([xmin, xmax], [100, 100], 'k-', label="Ideal", linewidth=2)
    
            plt.legend(loc='best', prop={'size':fontSizeLegend})
            plt.xscale('log')
            plt.title(title)
            plt.xlabel('Number of MPI processes')
            plt.ylabel(ylabel)
            plt.xticks(mpi,mpi)
            plt.grid()
            ymin, ymax = plt.ylim()
            ymin=0
            plt.xlim(xmin, xmax)
            plt.ylim(ymin, ymax)
            pp.savefig()
            plt.clf()
            pp.close()
    
argvs = sys.argv
argc = len(argvs)

if (argc != 2):
    print 'Usage: %s csv_filename' % argvs[0]
    quit()

csvFileName=argvs[1]

plotfileBase=csvFileName.replace('.','_')

nMaxSample=1
fontSize=14
fontSizeLegend=13

data=np.genfromtxt(csvFileName, names=True, delimiter=',', dtype=None)

decomposeParDictArray=np.unique(data['decomposeParDict'])
methodArray=np.unique(data['method'])
solverArray=np.unique(data['fvSolution'])
nProcsArray=np.unique(data['nProcs'])
batchFileNameArray=np.unique(data['solveBatch'])

mpl.rcParams.update({'font.size': fontSize})

if len(solverArray)>1:
    solverExecutionTimePerStep('ExecutionTimePerStepWOLastStep','Execution time per time step [s]')
    solverExecutionTimePerStep('ClockTimePerStepWOLastStep','Clock time per time step [s]')

if len(nProcsArray)>1:
    mpiParallelEfficiency('ExecutionTimePerStepWOLastStep','Parallel efficiency [%] (Execution time base)')
    mpiParallelEfficiency('ClockTimePerStepWOLastStep','Parallel efficiency [%] (Clock time base)')

    for yscalelog in [True,False]:
        mpiFirstExecutionTimePerStep('ExecutionTimeFirstStep','Execution time to complete 1st time step [s]'
                                     ,yscalelog)
        mpiFirstExecutionTimePerStep('ClockTimeFirstStep','Clock time to complete 1st time step [s]'
                                     ,yscalelog)
        mpiExecutionTimePerStep('ExecutionTimePerStepWOLastStep','Execution time per time step [s]'
                                ,yscalelog)
        mpiExecutionTimePerStep('ClockTimePerStepWOLastStep','Clock time per time step [s]'
                                ,yscalelog)
        mpiNumberOfStepsPerHour('ExecutionTimePerStepWOLastStep','Number of steps per hour (Execution time base)'
                                ,yscalelog)
        mpiNumberOfStepsPerHour('ClockTimePerStepWOLastStep','Number of steps per hour (Clock time base)'
                                ,yscalelog)

