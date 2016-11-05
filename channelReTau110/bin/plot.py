#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import textwrap
import argparse
import numpy as np
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import csv
import math

def parser():
    p = argparse.ArgumentParser()
    p.add_argument('csvFilename')
    p.add_argument('-m','--maxNumberOfSampling', help='Max number of sampling', type=int, default=1)
    p.add_argument('-L','--lineWidth', help='Line width', type=int, default=2)
    p.add_argument('-w','--widthOfXticks'
                   , help='Width of xticks in solver-ExecutionTimePerStep plot', type=int, default=20)
    p.add_argument('-x','--xscaleLinear'
                   , help='x scale Linear', action='store_true')
    p.add_argument('-y','--yscaleLinear'
                   , help='y scale Linear', action='store_true')
    p.add_argument('-r','--rotation'
                   , help='rotation degree of xticks', type=float, default=90)
    p.add_argument('-o','--offset'
                   , help='offset ratio of x range', type=float, default=0.02)
    p.add_argument('-O','--offsetSolver'
                   , help='offset ratio of x range in solver-* plot', type=float, default=0.02)
    p.add_argument('--titleFontSize', help='Title font size', type=int, default=14)
    p.add_argument('--legendFontSize', help='Legend font size', type=int, default=12)
    p.add_argument('--xlabelFontSize', help='X label fontsize', type=int, default=14)
    p.add_argument('--ylabelFontSize', help='Y label fontsize', type=int, default=14)
    p.add_argument('--tickFontSize', help='Tick font size', type=int, default=14)
    p.add_argument('--solverTickFontSize', help='Solver tick font size', type=int, default=14)
    p.add_argument('--topFractionSolver'
                   , help='Top faction in solver-* plot', type=float, default=0.95)
    p.add_argument('--bottomFractionSolver'
                   , help='Bottom faction in solver-* plot', type=float, default=0.2)
    p.add_argument('--topFractionMpi'
                   , help='Top faction in mpi-* plot', type=float, default=0.95)
    p.add_argument('--bottomFractionMpi'
                   , help='Bottom faction in mpi-* plot', type=float, default=0.15)
    p.add_argument('--ExecutionTimePerStep', help='Column of Execution time per step', type=str
                   , default='ExecutionTimePerStepWOLastStep')
    p.add_argument('--ClockTimePerStep', help='Column of clock time per step', type=str
                   , default='ClockTimePerStepWOLastStep')
    p.add_argument('--ExecutionTimeFirstStep', help='Column of execution time 1st step', type=str
                   , default='ExecutionTimeFirstStep')
    p.add_argument('--ClockTimeFirstStep', help='Column of clock time 1st time step', type=str
                   , default='ClockTimeFirstStep')
    return p.parse_args()

def plotMpiInit(title,subfilename):
    plotfile=args.csvFilename.replace('.','_')+'-'+title+subfilename
    if args.xscaleLinear:
        plotfile=plotfile+'-xscalelinear'
    else:
        plotfile=plotfile+'-xscaleLog'
    if args.yscaleLinear:
        plotfile=plotfile+'-yscaleLinear'
    else:
        plotfile=plotfile+'-yscaleLog'
    plotfile=plotfile+'-'+str(args.maxNumberOfSampling)
    plotfile=plotfile+'.pdf'
    print plotfile
    pp=PdfPages(plotfile)
    plt.title(title, fontsize=args.titleFontSize)
    return pp

def plotMpi(args,pp,mpi,ylabel):
    plt.subplots_adjust(top=args.topFractionMpi,bottom=args.bottomFractionMpi)
    plt.grid()
    plt.tick_params(labelsize=args.tickFontSize)
    plt.xlabel('Number of MPI processes', fontsize=args.xlabelFontSize)
    if args.xscaleLinear:
        offset=(mpi[-1]-mpi[0])*args.offset
        xmin=mpi[0]-offset
        xmax=mpi[-1]+offset
    else:
        offset=(math.log10(mpi[-1]-mpi[0]))*args.offset
        xmin=math.pow(10,math.log10(mpi[0])-offset)
        xmax=math.pow(10,math.log10(mpi[-1])+offset)
        plt.xscale('log')
    plt.xlim(xmin, xmax)
    plt.xticks(mpi,mpi,rotation=args.rotation)

    plt.ylabel(ylabel, fontsize=args.ylabelFontSize)
    ymin, ymax = plt.ylim()
    if args.yscaleLinear:
        ymin=0
    else:
        plt.yscale('log')
        ymin, ymax = plt.ylim()
    plt.ylim(ymin, ymax)

    return xmin,xmax,ymin,ymax

def plotEnd(pp):
    plt.legend(loc='best', prop={'size':args.legendFontSize})
    pp.savefig()
    plt.clf()
    pp.close()

def solverExecutionTimePerStep(args,data,column,ylabel):
    for decomposeParDict in np.unique(data['decomposeParDict']):
        title=decomposeParDict
        subfilename='-'+column
        pp=plotMpiInit(title,subfilename)

        for batchFileName in np.unique(data['solveBatch']):
            idx=np.where(
                (data['decomposeParDict']==decomposeParDict)
                & (data['solveBatch']==batchFileName)
                )

            solver=data['fvSolution'][idx]
            sn = np.unique(solver)
            x=np.arange(len(sn))
            if len(x)<=0:
                continue

            ExecutionTimePerStep=data[column][idx]
            index0=[]
            for snI in sn:
                index0.append(np.where(solver==snI)[0][0])
            if len(index0)>1:
                index1=index0[1:]
                index1=np.append(index1,len(ExecutionTimePerStep))
            else:
                index1=[1]
            ExecutionTimeAve=np.zeros(len(sn))
            if args.maxNumberOfSampling>1:
                ExecutionTimeSTD=np.zeros(len(sn))
            for i in range(len(sn)):
                ExecutionTime=ExecutionTimePerStep[index0[i]:index1[i]]
                ExecutionTime=np.sort(ExecutionTime)[0:min(len(ExecutionTime),args.maxNumberOfSampling)]
                ExecutionTimeAve[i]=np.average(ExecutionTime)
                if args.maxNumberOfSampling>1:
                    ExecutionTimeSTD[i]=np.std(ExecutionTime)
            
            if args.maxNumberOfSampling>1:
                plt.errorbar(x, ExecutionTimeAve, yerr=ExecutionTimeSTD, label=batchFileName\
                             , linewidth=args.lineWidth)
            else:
                plt.plot(x, ExecutionTimeAve, label=batchFileName, linewidth=args.lineWidth)

        plt.subplots_adjust(top=args.topFractionSolver,bottom=args.bottomFractionSolver)
        plt.legend(loc='best', prop={'size':args.legendFontSize})
        plt.grid()

        sn=np.unique(data['fvSolution'])
        x=np.arange(len(sn))
        snTicks=[]
        for snI in sn:
            snTicks.append('\n'.join(
                    textwrap.wrap(snI,width=args.widthOfXticks, subsequent_indent="  ")))
        plt.xticks(x,snTicks, rotation=args.rotation)
 
        plt.tick_params(axis='x', labelsize=args.solverTickFontSize)
        offset=(x[len(x)-1]-x[0])*args.offsetSolver
        xmin=x[0]-offset
        xmax=x[len(x)-1]+offset
        plt.xlim(xmin, xmax)

        plt.tick_params(axis='y',labelsize=args.tickFontSize)
        plt.ylabel(ylabel, fontsize=args.ylabelFontSize)
        ymin, ymax = plt.ylim()
        if args.yscaleLinear:
            ymin=0
        else:
            plt.yscale('log')
            ymin, ymax = plt.ylim()
        plt.ylim(ymin, ymax)

        pp.savefig()
        plt.clf()
        pp.close()

def mpiFirstExecutionTimePerStep(args,data,column,ylabel):
    for solver in np.unique(data['fvSolution']):
        for method in np.unique(data['method']):
            title=solver+'-method_'+method
            subfilename='-1stTime-'+column
            pp=plotMpiInit(title,subfilename)
            for batchFileName in np.unique(data['solveBatch']):
                idx=np.where(
                    (data['method']==method)
                    & (data['fvSolution']==solver)
                    & (data['solveBatch']==batchFileName)
                    )

                x=data['nProcs'][idx]
                if len(x)<=0:
                    break

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
                    ExecutionTimeFS=np.sort(ExecutionTimeFS)[0:min(len(ExecutionTimeFS),args.maxNumberOfSampling)]
                    ExecutionTimeFirstStepAve[i]=np.average(ExecutionTimeFS)
                    ExecutionTimeFirstStepSTD[i]=np.std(ExecutionTimeFS)

                if args.maxNumberOfSampling>1:
                    plt.errorbar(mpi, ExecutionTimeFirstStepAve, yerr=ExecutionTimeFirstStepSTD, label=batchFileName\
                                 , linewidth=args.lineWidth)
                else:
                    plt.plot(mpi, ExecutionTimeFirstStepAve, label=batchFileName, linewidth=args.lineWidth)

            xmin,xmax,ymin,ymax=plotMpi(args,pp,mpi,ylabel)
            plotEnd(pp)

def mpiExecutionTimePerStep(args,data,column,ylabel):
    for solver in np.unique(data['fvSolution']):
        for method in np.unique(data['method']):
            title=solver+'-method_'+method
            subfilename='-loopTime-'+column
            pp=plotMpiInit(title,subfilename)
            for batchFileName in np.unique(data['solveBatch']):
                idx=np.where(
                    (data['method']==method)
                    & (data['fvSolution']==solver)
                    & (data['solveBatch']==batchFileName)
                    )

                x=data['nProcs'][idx]
                if len(x)<=0:
                    break

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
                    ExecutionTime=np.sort(ExecutionTime)[0:min(len(ExecutionTime),args.maxNumberOfSampling)]
                    ExecutionTimeAve[i]=np.average(ExecutionTime)
                    ExecutionTimeSTD[i]=np.std(ExecutionTime)

                if args.maxNumberOfSampling>1:
                    plt.errorbar(mpi, ExecutionTimeAve, yerr=ExecutionTimeSTD, label=batchFileName\
                                 , linewidth=args.lineWidth)
                else:
                    plt.plot(mpi, ExecutionTimeAve, label=batchFileName,linewidth=args.lineWidth)

                rBase=ExecutionTimeAve[0]*mpi[0]

            xmin,xmax,ymin,ymax=plotMpi(args,pp,mpi,ylabel)
            if not args.yscaleLinear:
                plt.plot([xmin, xmax], [rBase/xmin, rBase/xmax], 'k-', label="Ideal", linewidth=args.lineWidth)
            plotEnd(pp)

def mpiNumberOfStepsPerHour(args,data,column,ylabel):
    for solver in np.unique(data['fvSolution']):
        for method in np.unique(data['method']):
            title=solver+'-method_'+method
            subfilename='-sph-'+column
            pp=plotMpiInit(title,subfilename)
            for batchFileName in np.unique(data['solveBatch']):
                idx=np.where(
                    (data['method']==method)
                    & (data['fvSolution']==solver)
                    & (data['solveBatch']==batchFileName)
                    )

                x=data['nProcs'][idx]
                if len(x)<=0:
                    break

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
                    ExecutionTime=np.sort(ExecutionTime)[0:min(len(ExecutionTime),args.maxNumberOfSampling)]
                    ExecutionTimeAve[i]=np.average(ExecutionTime)
                    ExecutionTimeSTD[i]=np.std(ExecutionTime)
                    numberOfStepsPerHourAve[i]=3600.0/ExecutionTimeAve[i]
                    numberOfStepsPerHourSTD[i]=np.std(3600.0/ExecutionTime)

                if args.maxNumberOfSampling>1:
                    plt.errorbar(mpi, numberOfStepsPerHourAve, yerr=numberOfStepsPerHourSTD
                                 , label=batchFileName, linewidth=args.lineWidth)
                else:
                    plt.plot(mpi, numberOfStepsPerHourAve, label=batchFileName, linewidth=args.lineWidth)

                rBase=numberOfStepsPerHourAve[0]/mpi[0]

            xmin,xmax,ymin,ymax=plotMpi(args,pp,mpi,ylabel)
            if not args.yscaleLinear:
                plt.plot([xmin, xmax], [xmin*rBase, xmax*rBase], 'k-', label="Ideal", linewidth=args.lineWidth)
            plotEnd(pp)

def mpiParallelEfficiency(args,data,column,ylabel):
    for solver in np.unique(data['fvSolution']):
        for method in np.unique(data['method']):
            title=solver+'-method_'+method
            subfilename='-pe-'+column
            pp=plotMpiInit(title,subfilename)
            for batchFileName in np.unique(data['solveBatch']):
                idx=np.where(
                    (data['method']==method)
                    & (data['fvSolution']==solver)
                    & (data['solveBatch']==batchFileName)
                    )

                x=data['nProcs'][idx]
                if len(x)<=0:
                    break

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
                    ExecutionTime=np.sort(ExecutionTime)[0:min(len(ExecutionTime),args.maxNumberOfSampling)]
                    ExecutionTimeAve[i]=np.average(ExecutionTime)

                    ExecutionTimePE=ExecutionTimeAve[0]/ExecutionTime/(mpi[i]/mpi[0])*100.0
                    ExecutionTimePESTD[i]=np.std(ExecutionTimePE)

                ExecutionTimePEAve=ExecutionTimeAve[0]/ExecutionTimeAve/(mpi/mpi[0])*100.0

                if args.maxNumberOfSampling>1:
                    plt.errorbar(mpi, ExecutionTimePEAve, yerr=ExecutionTimePESTD, label=batchFileName\
                                 , linewidth=args.lineWidth)
                else:
                    plt.plot(mpi, ExecutionTimePEAve, label=batchFileName, linewidth=args.lineWidth)

            xmin,xmax,ymin,ymax=plotMpi(args,pp,mpi,ylabel)
            plt.plot([xmin, xmax], [100, 100], 'k-', label="Ideal", linewidth=args.lineWidth)
            plotEnd(pp)

if __name__ == '__main__':
    args=parser()

    data=np.genfromtxt(args.csvFilename, names=True, delimiter=',', dtype=None)

    if len(np.unique(data['nProcs']))>1:
        mpiExecutionTimePerStep(args, data, args.ExecutionTimePerStep
                                ,'Execution time per time step [s]')
        mpiExecutionTimePerStep(args, data, args.ClockTimePerStep
                                ,'Clock time per time step [s]')
        mpiNumberOfStepsPerHour(args, data, args.ExecutionTimePerStep
                                ,'Number of steps per hour (Execution time base)')
        mpiNumberOfStepsPerHour(args, data, args.ClockTimePerStep
                                ,'Number of steps per hour (Clock time base)')
        mpiParallelEfficiency(args, data, args.ExecutionTimePerStep
                              ,'Parallel efficiency [%] (Execution time base)')
        mpiParallelEfficiency(args, data, args.ClockTimePerStep
                              ,'Parallel efficiency [%] (Clock time base)')
        mpiFirstExecutionTimePerStep(args, data, args.ExecutionTimeFirstStep
                                     ,'Execution time to complete 1st time step [s]')
        mpiFirstExecutionTimePerStep(args, data, args.ClockTimeFirstStep
                                     ,'Clock time to complete 1st time step [s]')


    if len(np.unique(data['fvSolution']))>1:
        solverExecutionTimePerStep(args, data, args.ExecutionTimePerStep
                                   ,'Execution time per time step [s]')
        solverExecutionTimePerStep(args, data, args.ClockTimePerStep
                                   ,'Clock time per time step [s]')

