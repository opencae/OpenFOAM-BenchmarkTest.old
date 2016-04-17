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

def result(basedir):
    nMaxSample=5
    data=np.genfromtxt("../"+basedir+"/table.csv", names=True, delimiter=',', dtype=None)
    nCellsArray=np.unique(data['nCells'])
    LESModelArray=np.unique(data['LESModel'])
    solverArray=np.unique(data['solver'])
    nProcsArray=np.unique(data['nProcs'])
    
    for nCells in nCellsArray:
        if nCells != 5992888:
            continue
        for LESModel in LESModelArray:
            if LESModel != "laminar":
                continue
            for solver in solverArray:
                if solver != "PCG":
                    continue
                idxSolver=np.where(data['solver']==solver)
                preArray=np.unique(data['preconditioner'][idxSolver])
                for pre in preArray:
                    if pre != "DIC" and pre != "AINV":
                        continue
                    idx=np.where(
                        (data['nCells']==nCells)
                        & (data['LESModel']==LESModel)
                        & (data['solver']==solver)
                        & (data['preconditioner']==pre)
                        )
                    x=data['nProcs'][idx]
                    y=(data['ClockTimeNextToLastStep'][idx]-data['ClockTimeFirstStep'][idx])\
                        /(data['Steps'][idx]-2.0)
    
                    mpi,index0 = np.unique(x, return_index=True)
                    index1=index0[1:]
                    index1=np.append(index1,len(y))
                    clockTimeAve=np.zeros(len(mpi))
                    for i in range(len(mpi)):
                        clockTime=y[index0[i]:index1[i]]
                        clockTime=np.sort(clockTime)[0:min(len(clockTime),nMaxSample)]
                        clockTimeAve[i]=np.average(clockTime)
                        sr=clockTimeAve[0]/clockTime
                        pe=sr/(mpi[i]/mpi[0])*100.0

                    nTimeStepPerHourAve=3600.0/clockTimeAve
                    srAve=clockTimeAve[0]/clockTimeAve
                    peAve=srAve/(mpi/mpi[0])*100

                    return mpi,clockTimeAve,nTimeStepPerHourAve,srAve,peAve
                            
def charge(basename,mpi,report,year):
    chargeCoef=np.ones(len(mpi))
    label=[basename[1]]
    if basename[1] == "FOCUS A":
        chargePerTime=[0]
        chargePerNodeTime=[100*1.08]
        if year=='FYH27':
            for i in range(len(mpi)):
                if mpi[i]/mpi[0]<=8:
                    chargeCoef[i]=1.0
                elif mpi[i]/mpi[0]<=16:
                    chargeCoef[i]=90./100.
                elif mpi[i]/mpi[0]<=24:
                    chargeCoef[i]=80./100.
                elif mpi[i]/mpi[0]<=32:
                    chargeCoef[i]=70./100.
                elif mpi[i]/mpi[0]<=40:
                    chargeCoef[i]=60./100.
                else:
                    chargeCoef[i]=50./100.
        elif year=='FYH28':
            for i in range(len(mpi)):
                if mpi[i]/mpi[0]<=16:
                    chargeCoef[i]=1.0
                elif mpi[i]/mpi[0]<=32:
                    chargeCoef[i]=90./100.
                elif mpi[i]/mpi[0]<=48:
                    chargeCoef[i]=80./100.
                elif mpi[i]/mpi[0]<=64:
                    chargeCoef[i]=70./100.
                elif mpi[i]/mpi[0]<=80:
                    chargeCoef[i]=60./100.
                else:
                    chargeCoef[i]=50./100.

    elif basename[1] == "FOCUS D":
        chargePerTime=[0]
        chargePerNodeTime=[300*1.08]
        if year=='FYH27':
            for i in range(len(mpi)):
                if mpi[i]/mpi[0]<=32:
                    chargeCoef[i]=1.0
                elif mpi[i]/mpi[0]<=40:
                    chargeCoef[i]=285./300.
                elif mpi[i]/mpi[0]<=48:
                    chargeCoef[i]=270./300.
                elif mpi[i]/mpi[0]<=64:
                    chargeCoef[i]=255./300.
                else:
                    chargeCoef[i]=240./300.
        elif year=='FYH28':
            for i in range(len(mpi)):
                if mpi[i]/mpi[0]<=8:
                    chargeCoef[i]=1.0
                elif mpi[i]/mpi[0]<=16:
                    chargeCoef[i]=285./300.
                elif mpi[i]/mpi[0]<=24:
                    chargeCoef[i]=270./300.
                elif mpi[i]/mpi[0]<=32:
                    chargeCoef[i]=255./300.
                elif mpi[i]/mpi[0]<=40:
                    chargeCoef[i]=240./300.
                elif mpi[i]/mpi[0]<=48:
                    chargeCoef[i]=225./300.
                elif mpi[i]/mpi[0]<=56:
                    chargeCoef[i]=210./300.
                elif mpi[i]/mpi[0]<=64:
                    chargeCoef[i]=195./300.
                elif mpi[i]/mpi[0]<=72:
                    chargeCoef[i]=180./300.
                else:
                    chargeCoef[i]=165./300.

    elif basename[1] == "Azure A9":
        chargePerTime=[31.42*1.08]
        chargePerNodeTime=[198.90*1.08]
    elif basename[1] == "EC2 c4.8xlarge":
        chargePerNodeTime=[295.8]
        chargePerTime=[132.8]
    elif basename[1] == "Oakleaf-FX":
        chargePerTime=[0,0]
        if year=='FYH27':
            chargePerNodeTime=[180800/8640]
        elif year=='FYH28':
            chargePerNodeTime=[77500/8640]
            
#        for i in range(len(mpi)):
#            if mpi[i]/mpi[0]<=12:
#                chargeCoef[i]=1.0
#            else:
#                chargeCoef[i]=2.0

    elif basename[1] == "TSUBAME S" or "TSUBAME G(GPU)":
        if basename[1] == "TSUBAME G(GPU)":
            for i in range(len(mpi)):
                chargeCoef[i]=0.5
        chargePerTime=[0]
        if report == "close":
            chargePerNodeTime=[10*4*4*1.08]
        else:
            chargePerNodeTime=[10*4*1.08]

    return label,chargeCoef,chargePerTime,chargePerNodeTime

def plotCPUChargePerHourVsNumberOfTimesStepPerHour(base,basenameArray,xmin,xmax,ymin,ymax,report,year):
    plt.figure()
    pylab.subplots_adjust(bottom=0.125,top=0.975,left=0.15,right=0.95)
    mpl.rcParams.update({'font.size': 18})
    plt.ylabel('Number of time step per hour [Step/h]')
    plt.xlabel('CPU Charge per hour [JPY/h]')
    if xmin<xmax:
        plt.xlim(xmin, xmax)
    if ymin<ymax:
        plt.ylim(ymin, ymax)
    plt.xticks()
    plt.yticks()
    plt.grid(True)

    for basename in basenameArray:
        if basename[1]=="Xeon Phi":
                continue
        if report=="close":
            if basename[1]=='Oakleaf-FX':
                continue
        else:
            if basename[1] == 'FOCUS A' or basename[1] == 'FOCUS D' \
            or basename[1] == 'EC2 c4.8xlarge' or basename[1] == 'Azure A9':
                continue

        (mpi,clockTimeAve,nTimeStepPerHourAve,srAve,peAve)=result(basename[0])
        (label,chargeCoef,chargePerTime,chargePerNodeTime)=charge(basename,mpi,report,year)
        for i in range(len(label)):
            plt.plot(chargeCoef*(chargePerNodeTime[i]*mpi/mpi[0]+chargePerTime[i])
                     ,nTimeStepPerHourAve
                     , label=label[i], linewidth=2, color=basename[2], linestyle=basename[3], marker=basename[4], markersize=10)
                      
    plt.legend(loc='best', prop={'size':13})
    plt.savefig(base+"-ChargePerHour-NumerOfTimeStepPerHour-"+str(report)+"-"+str(year)\
                +"-"+str(xmin)+"-"+str(xmax)+"-"+str(ymin)+"-"+str(ymax)+".pdf")
    plt.clf()
    plt.close()

def plotParallelEfficiency(base,basenameArray,xmin,xmax,ymin,ymax,node):
    plt.figure()
    pylab.subplots_adjust(bottom=0.125,top=0.975,left=0.15,right=0.95)
    mpl.rcParams.update({'font.size': 18})
    plt.xlabel('Number of node')
#    plt.ylabel('Parallel efficiency (Strong scaling) [\%]')
    plt.ylabel('Parallel efficiency (Strong scaling) [%]')
    plt.xlim(xmin, xmax)
    plt.ylim(ymin, ymax)
    plt.xticks(node)
    plt.yticks()
    plt.grid()

    for basename in basenameArray:
        (mpi,clockTimeAve,nTimeStepPerHourAve,srAve,peAve)=result(basename[0])
        plt.plot(mpi/mpi[0],peAve, label=basename[1], linewidth=2, color=basename[2], linestyle=basename[3], marker=basename[4], markersize=10)    
        
    plt.legend(loc='best', prop={'size':13})
    plt.savefig(base+"-node-pe"\
                +"-"+str(xmin)+"-"+str(xmax)+"-"+str(ymin)+"-"+str(ymax)+".pdf")
    plt.clf()
    plt.close()

def plotNumberOfTimeStepPerHour(base,basenameArray,xmin,xmax,ymin,ymax,node):
    plt.figure()
    pylab.subplots_adjust(bottom=0.125,top=0.975,left=0.15,right=0.95)
    mpl.rcParams.update({'font.size': 18})
    plt.xlabel('Number of node [-]')
    plt.ylabel('Number of time step per hour [Step/h]')
    if xmin<xmax:
        plt.xlim(xmin, xmax)
    if ymin<ymax:
        plt.ylim(ymin, ymax)
    plt.xticks(node)
    plt.yticks()
    plt.grid()

    for basename in basenameArray:
        (mpi,clockTimeAve,nTimeStepPerHourAve,srAve,peAve)=result(basename[0])
        plt.plot(mpi/mpi[0],nTimeStepPerHourAve, label=basename[1], linewidth=2, color=basename[2], linestyle=basename[3], marker=basename[4], markersize=10)    
        
    plt.legend(loc='best', prop={'size':13})
    plt.savefig(base+"-node-NumberOfTimeStepPerHour"\
                +"-"+str(xmin)+"-"+str(xmax)+"-"+str(ymin)+"-"+str(ymax)+".pdf")
    plt.clf()
    plt.close()

def plotCPUChargePerTimeStep(base,basenameArray,xmin,xmax,ymin,ymax,node,report,year):
    plt.figure()
    pylab.subplots_adjust(bottom=0.125,top=0.975,left=0.15,right=0.95)
    mpl.rcParams.update({'font.size': 18})
    plt.xlabel('Number of node [-]')
    plt.ylabel('CPU Charge per time step [JPY]')
    if xmin<xmax:
        plt.xlim(xmin, xmax)
    if ymin<ymax:
        plt.ylim(ymin, ymax)
    plt.xticks(node)
    plt.yticks()
    plt.grid(True)

    for basename in basenameArray:
        if basename[1]=="Xeon Phi":
                continue
        if report=="close":
            if basename[1]=='Oakleaf-FX':
                continue
        else:
            if basename[1] == 'FOCUS A' or basename[1] == 'FOCUS D'\
            or basename[1] == 'EC2 c4.8xlarge' or basename[1] == 'Azure A9':
                continue

        (mpi,clockTimeAve,nTimeStepPerHourAve,srAve,peAve)=result(basename[0])
        (label,chargeCoef,chargePerTime,chargePerNodeTime)=charge(basename,mpi,report,year)
        for i in range(len(label)):
            plt.plot(mpi/mpi[0],chargeCoef*(chargePerNodeTime[i]*mpi/mpi[0]+chargePerTime[i])*clockTimeAve/3600.0
                     , label=label[i], linewidth=2, color=basename[2], linestyle=basename[3], marker=basename[4], markersize=10)
                      
    plt.legend(loc='best', prop={'size':13})
    plt.savefig(base+"-node-charge-"+str(report)+"-"+str(year)\
                +"-"+str(xmin)+"-"+str(xmax)+"-"+str(ymin)+"-"+str(ymax)+".pdf")
    plt.clf()
    plt.close()

        
#
# main
#

# use Type 1 font
#plt.rcParams['ps.useafm'] = True
#plt.rcParams['pdf.use14corefonts'] = True
#plt.rcParams['text.usetex'] = True
#plt.rcParams['font.family'] = 'Times New Roman'

base="all"
basenameArray=[
    ['Oakleaf_FX-2.3.0-n_00016-No1','Oakleaf-FX', 'r', '-', 'o']
    ,['TSUBAME_S-OF230-gcc_4.8.4-openmpi_1.6.5-ncpus_10-n_00016-No1','TSUBAME S', 'k', '-', 'v']
    ,['TSUBAME_G-RCdev-cuda_6.5-openmpi_1.8.4-gpus_3-n_00016-No1','TSUBAME G(GPU)', 'g', '-', '^']
    ]

nodeSmall=[1,2,3,4,5,6,7,8]
nodeLarge=[1,4,6,8,12,16,20,24,48]

plotParallelEfficiency(base,basenameArray,0,50,0,200,nodeLarge)


plotNumberOfTimeStepPerHour(base,basenameArray,0,50,0,8000,nodeLarge)
plotNumberOfTimeStepPerHour(base,basenameArray,0,9,0,1200,nodeSmall)

plotCPUChargePerTimeStep(base,basenameArray,0,50,0,0.8,nodeLarge,"open",'FYH27')
plotCPUChargePerHourVsNumberOfTimesStepPerHour(base,basenameArray,0,360,0,1200,"open",'FYH27')
plotCPUChargePerHourVsNumberOfTimesStepPerHour(base,basenameArray,0,2400,0,8000,"open",'FYH27')

plotCPUChargePerTimeStep(base,basenameArray,0,50,0,0.8,nodeLarge,"open",'FYH28')
plotCPUChargePerHourVsNumberOfTimesStepPerHour(base,basenameArray,0,360,0,1200,"open",'FYH28')
plotCPUChargePerHourVsNumberOfTimesStepPerHour(base,basenameArray,0,2400,0,8000,"open",'FYH28')
