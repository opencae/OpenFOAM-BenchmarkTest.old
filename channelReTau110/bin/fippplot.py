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

dataorig=np.genfromtxt("fipptable.csv", names=True, delimiter=',', dtype=None)

data=np.sort(dataorig)

if options.standard:
    plotfile='fipp-standard.pdf'
else:
    plotfile='fipp.pdf'

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
	
	            y=data['MFLOPSPEAK'][idx]
	
                    sn = np.unique(solvers)
                    index0=[]
                    for snI in sn:
                        index0.append(np.where(solvers==snI)[0][0])
	            index1=index0[1:]
	            index1=np.append(index1,len(y))
	            MFLOPSPerPeakAve=np.zeros(len(sn))
	            MFLOPSPerPeakSTD=np.zeros(len(sn))
	            for i in range(len(sn)):
	                MFLOPSPerPeak=y[index0[i]:index1[i]]
	                MFLOPSPerPeakAve[i]=np.average(MFLOPSPerPeak)
	                MFLOPSPerPeakSTD[i]=np.std(MFLOPSPerPeak)

                    LESModels=LESModel
                    if LESModel != "laminar":
                        LESModels+=",delta="+delta
                        if delta == "vanDriest":
                            LESModels+=",calcInterval="+str(calcInterval)
	
	            base=str(nCells)+"cells-"+LESModels+"-"+str(nProcs)+"MPI-performance"
	            print base
	
	            x=np.arange(len(sn))
	
	            offset=(x[len(x)-1]-x[0])*0.05
	            xmin=x[0]-offset
	            xmax=x[len(x)-1]+offset
	
                    title=basename+"\n"+str(nCells/1e+6)+"M cells\n"+LESModels+"\n"+str(nProcs)+"MPI"
                    plt.title(title)
	            plt.plot(x,MFLOPSPerPeakAve, label="MFLOPS per peak [%]", linewidth=1)
	            plt.errorbar(x, MFLOPSPerPeakAve, yerr=MFLOPSPerPeakSTD, fmt='.', linewidth=2)
	            plt.xlabel('Matrix solver for pressure equation')
	            plt.xticks(x,sn, rotation=-90)
	            plt.ylabel('MFLOPS per peak [%]')
	            ymin, ymax = plt.ylim()
	            ymin=0
	            plt.xlim(xmin, xmax)
	            plt.ylim(ymin,ymax*1.1)
#	            plt.legend(loc='lower left')
	            plt.grid()
	            pp.savefig()
	            plt.clf()
	
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
	                y=data['MFLOPSPEAK'][idx]
	
                        mpi = np.unique(x)
                        index0=[]
                        for mpiI in mpi:
                            index0.append(np.where(x==mpiI)[0][0])
	                index1=index0[1:]
	                index1=np.append(index1,len(y))
	                MFLOPSPerPeakAve=np.zeros(len(mpi))
	                MFLOPSPerPeakSTD=np.zeros(len(mpi))
	                for i in range(len(mpi)):
	                    MFLOPSPerPeak=y[index0[i]:index1[i]]
	                    MFLOPSPerPeakAve[i]=np.average(MFLOPSPerPeak)
	                    MFLOPSPerPeakSTD[i]=np.std(MFLOPSPerPeak)

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
	                plt.plot(mpi,MFLOPSPerPeakAve, label="MFLOPS per peak [%]", linewidth=1)
	                plt.errorbar(mpi, MFLOPSPerPeakAve, yerr=MFLOPSPerPeakSTD, fmt='.', linewidth=2)
	                plt.ylabel('MFLOPS per peak [%]')
	                ymin, ymax = plt.ylim()
	                ymin=0
	                plt.xlim(xmin, xmax)
	                plt.ylim(ymin,ymax*1.1)
#	                plt.legend(loc='upper right')
	                pp.savefig()
	                plt.clf()
	
pp.close()
