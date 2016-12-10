#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import matplotlib as mpl
mpl.use('Agg')
import numpy as np
import pylab
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.ticker import ScalarFormatter
import argparse
import math

HUGE=1e+30

base="all"
basenameArray=[
     ['Reedbush_U-mesh_24M-No1','Reedbush-U', 'y', '-', 's', 32, "open", "OF230_Icc_SGIMPI"]
#    ,['FOCUS_D-mesh_24M-No1','FOCUS D', "r", '-', 'D', -1, "close", "OF230_Icc_IntelMPI"]
    ,['FOCUS_F-mesh_24M-No1','FOCUS F', "b", '-', '>', -1, "close", "OF230_Icc_IntelMPI"]
    ,['FOCUS_H-mesh_24M-No1','FOCUS H', "g", '-', 'H', 8, "close", "OF230_Icc_IntelMPI"]
    ]

nodeLarge=[1,2,4,8,10,16,24,32]

def parser():
    p = argparse.ArgumentParser()
    p.add_argument('csvFilename')
    p.add_argument('-a','--all', help='plot all data', action='store_true')
    p.add_argument('-m','--maxNumberOfSampling', help='Max number of sampling', type=int, default=1)
    p.add_argument('-L','--lineWidth', help='Line width', type=int, default=2)
    p.add_argument('-M','--markersize', help='Marker size', type=int, default=8)
    p.add_argument('-x','--xscaleLinear'
                   , help='x scale Linear', action='store_true')
    p.add_argument('-y','--yscaleLinear'
                   , help='y scale Linear', action='store_true')
    p.add_argument('-o','--offset'
                   , help='offset ratio of x range', type=float, default=0.05)
    p.add_argument('-r','--rotation'
                   , help='rotation degree of xticks', type=float, default=90)
    p.add_argument('--titleFontSize', help='Title font size', type=int, default=14)
    p.add_argument('--legendFontSize', help='Legend font size', type=int, default=10)
    p.add_argument('--xlabelFontSize', help='X label fontsize', type=int, default=14)
    p.add_argument('--ylabelFontSize', help='Y label fontsize', type=int, default=14)
    p.add_argument('--tickFontSize', help='Tick font size', type=int, default=14)
    p.add_argument('--topFraction'
                   , help='Top faction', type=float, default=0.95)
    p.add_argument('--bottomFraction'
                   , help='Bottom faction', type=float, default=0.1)
    return p.parse_args()


def result(basename):
    data=np.genfromtxt("../"+basename[0]+"/"+args.csvFilename, names=True, delimiter=',', dtype=None)

    nNodesMax=10e+30
    if args.all==False and basename[5]>0:
        nNodesMax=basename[5]
    
    idx=np.where(
        (data['fvSolution']=='PCG-DIC')
        & (data['solveBatch']==basename[7])
        & (data['nNodes']<=nNodesMax)
        )

    x=data['nNodes'][idx]
    if data['Steps'][idx][0]==51:
        y=data['ExecutionTimePerStep'][idx]
    elif data['Steps'][idx][0]==52:
        y=data['ExecutionTimePerStepWOLastStep'][idx]
    else:
        print "Illegal Steps: "+str(data['Steps'][idx][0])
        exit(0)
        
    t=data['ExecutionTimeFirstStep'][idx]

    node,index0 = np.unique(x, return_index=True)
    index1=index0[1:]
    index1=np.append(index1,len(y))
    clockTimeAve=np.zeros(len(node))
    clockTimeFSAve=np.zeros(len(node))

    for i in range(len(node)):
        clockTime=y[index0[i]:index1[i]]
        clockTime=np.sort(clockTime)[0:min(len(clockTime),args.maxNumberOfSampling)]
        clockTimeAve[i]=np.average(clockTime)
        sr=clockTimeAve[0]/clockTime
        pe=sr/(node[i]/node[0])*100.0
        clockTimeFS=t[index0[i]:index1[i]]
        clockTimeFS=np.sort(clockTimeFS)[0:min(len(clockTimeFS),args.maxNumberOfSampling)]
        clockTimeFSAve[i]=np.average(clockTimeFS)
    
    nTimeStepPerHourAve=3600.0/clockTimeAve
    srAve=clockTimeAve[0]/clockTimeAve
    peAve=srAve/(node/node[0])*100
    
    return node,clockTimeAve,nTimeStepPerHourAve,srAve,peAve,clockTimeFSAve
                            
def charge(basename,node,report,year):
    chargeCoef=np.ones(len(node))
    label=[basename[1]+","+basename[7]]
    if basename[1] == "FOCUS A":
        chargePerTime=[0]
        chargePerNodeTime=[100*1.08]
        if year=='FYH27':
            for i in range(len(node)):
                if node[i]<=8:
                    chargeCoef[i]=1.0
                elif node[i]<=16:
                    chargeCoef[i]=90./100.
                elif node[i]<=24:
                    chargeCoef[i]=80./100.
                elif node[i]<=32:
                    chargeCoef[i]=70./100.
                elif node[i]<=40:
                    chargeCoef[i]=60./100.
                else:
                    chargeCoef[i]=50./100.
        elif year=='FYH28':
            for i in range(len(node)):
                if node[i]<=16:
                    chargeCoef[i]=1.0
                elif node[i]<=32:
                    chargeCoef[i]=90./100.
                elif node[i]<=48:
                    chargeCoef[i]=80./100.
                elif node[i]<=64:
                    chargeCoef[i]=70./100.
                elif node[i]<=80:
                    chargeCoef[i]=60./100.
                else:
                    chargeCoef[i]=50./100.
        elif year=='FYH29':
            for i in range(len(node)):
                if node[i]<=8:
                    chargeCoef[i]=1.0
                elif node[i]<=16:
                    chargeCoef[i]=95./100.
                elif node[i]<=24:
                    chargeCoef[i]=90./100.
                elif node[i]<=32:
                    chargeCoef[i]=85./100.
                elif node[i]<=40:
                    chargeCoef[i]=80./100.
                elif node[i]<=48:
                    chargeCoef[i]=75./100.
                elif node[i]<=56:
                    chargeCoef[i]=70./100.
                elif node[i]<=64:
                    chargeCoef[i]=65./100.
                elif node[i]<=72:
                    chargeCoef[i]=60./100.
                elif node[i]<=80:
                    chargeCoef[i]=55./100.
                else:
                    chargeCoef[i]=50./100.

    elif basename[1] == "FOCUS D":
        chargePerTime=[0]
        chargePerNodeTime=[300*1.08]
        if year=='FYH27':
            for i in range(len(node)):
                if node[i]<=32:
                    chargeCoef[i]=1.0
                elif node[i]<=40:
                    chargeCoef[i]=285./300.
                elif node[i]<=48:
                    chargeCoef[i]=270./300.
                elif node[i]<=64:
                    chargeCoef[i]=255./300.
                else:
                    chargeCoef[i]=240./300.
        elif year=='FYH28':
            for i in range(len(node)):
                if node[i]<=8:
                    chargeCoef[i]=1.0
                elif node[i]<=16:
                    chargeCoef[i]=285./300.
                elif node[i]<=24:
                    chargeCoef[i]=270./300.
                elif node[i]<=32:
                    chargeCoef[i]=255./300.
                elif node[i]<=40:
                    chargeCoef[i]=240./300.
                elif node[i]<=48:
                    chargeCoef[i]=225./300.
                elif node[i]<=56:
                    chargeCoef[i]=210./300.
                elif node[i]<=64:
                    chargeCoef[i]=195./300.
                elif node[i]<=72:
                    chargeCoef[i]=180./300.
                else:
                    chargeCoef[i]=165./300.
        elif year=='FYH29':
            for i in range(len(node)):
                if node[i]<=8:
                    chargeCoef[i]=1.0
                elif node[i]<=16:
                    chargeCoef[i]=280./300.
                elif node[i]<=24:
                    chargeCoef[i]=260./300.
                elif node[i]<=32:
                    chargeCoef[i]=240./300.
                elif node[i]<=40:
                    chargeCoef[i]=220./300.
                elif node[i]<=48:
                    chargeCoef[i]=200./300.
                elif node[i]<=56:
                    chargeCoef[i]=180./300.
                elif node[i]<=64:
                    chargeCoef[i]=160./300.
                else:
                    chargeCoef[i]=140./300.

    elif basename[1] == "FOCUS F":
        chargePerTime=[0]
        chargePerNodeTime=[500*1.08]
        if year=='FYH29':
            for i in range(len(node)):
                if node[i]<=1:
                    chargeCoef[i]=1.0
                elif node[i]<=4:
                    chargeCoef[i]=475./500.
                elif node[i]<=6:
                    chargeCoef[i]=450./500.
                elif node[i]<=8:
                    chargeCoef[i]=425./300.
                elif node[i]<=10:
                    chargeCoef[i]=400./500.
                else:
                    chargeCoef[i]=375./500.

    elif basename[1] == "FOCUS H":
        chargePerTime=[0]
        chargePerNodeTime=[100*1.08]
        if year=='FYH29':
            for i in range(len(node)):
                if node[i]<=8:
                    chargeCoef[i]=1.0
                elif node[i]<=16:
                    chargeCoef[i]=95./100.
                elif node[i]<=24:
                    chargeCoef[i]=90./100.
                elif node[i]<=32:
                    chargeCoef[i]=85./100.
                elif node[i]<=40:
                    chargeCoef[i]=80./100.
                elif node[i]<=48:
                    chargeCoef[i]=75./100.
                elif node[i]<=56:
                    chargeCoef[i]=70./100.
                elif node[i]<=64:
                    chargeCoef[i]=65./100.
                else:
                    chargeCoef[i]=60./100.

    elif basename[1] == "Azure A9":
        chargePerTime=[31.42*1.08]
        chargePerNodeTime=[198.90*1.08]
    elif basename[1] == "EC2 c4.8xlarge":
        chargePerNodeTime=[295.8]
        chargePerTime=[132.8]
    elif basename[1] == "Oakleaf-FX":
        chargePerTime=[0,0]
        chargePerNodeTime=[77500/8640]
        if year=='FYH27':
            chargePerNodeTime=[180800/8640]

    elif basename[1] == "Reedbush-U":
        chargePerTime=[0,0]
        chargePerNodeTime=[62000/2880]

    elif basename[1] == "TSUBAME S" or basename[1] =="TSUBAME G":
        if basename[1] == "TSUBAME G":
            for i in range(len(node)):
                chargeCoef[i]=0.5
        chargePerTime=[0]
        if report == "close":
            chargePerNodeTime=[10*4*4*1.08]
        else:
            chargePerNodeTime=[10*4*1.08]

    if  basename[1] == "Oakleaf-FX" or basename[1] == "Reedbush-U":
        if  basename[1] == "Oakleaf-FX":
            normalChargeNodeMax=12
        else:
            normalChargeNodeMax=4

        for i in range(len(node)):
            if node[i]<=normalChargeNodeMax:
                chargeCoef[i]=1.0
            else:
                chargeCoef[i]=(normalChargeNodeMax+(node[i]-normalChargeNodeMax)*2.0)/node[i]

    return label,chargeCoef,chargePerTime,chargePerNodeTime

def plotCPUChargePerHourVsNumberOfTimesStepPerHour(args,base,basenameArray,report,year):

    subfilename="ChargePerHour-NumerOfTimeStepPerHour-"+str(report)+"-"+str(year)
    pp=plotInit(subfilename)

    chargeMin=HUGE
    chargeMax=-HUGE
    nTimeStepPerHourAveMin=HUGE
    nTimeStepPerHourAveMax=-HUGE
    for basename in basenameArray:
        if report != "both" and basename[6] != "both" and basename[6] != report:
            continue
        (node,clockTimeAve,nTimeStepPerHourAve,srAve,peAve,clockTimeFSAve)=result(basename)
        (label,chargeCoef,chargePerTime,chargePerNodeTime)=charge(basename,node,report,year)
        for i in range(len(label)):
            chargeArray=chargeCoef*(chargePerNodeTime[i]*node+chargePerTime[i])
            chargeMin=min(min(chargeArray),chargeMin)
            chargeMax=max(max(chargeArray),chargeMax)
            nTimeStepPerHourAveMin=min(min(nTimeStepPerHourAve),nTimeStepPerHourAveMin)
            nTimeStepPerHourAveMax=max(max(nTimeStepPerHourAve),nTimeStepPerHourAveMax)
            plt.plot(chargeArray
                     ,nTimeStepPerHourAve
                     , label=label[i]
                     , linewidth=args.lineWidth
                     , color=basename[2]
                     , linestyle=basename[3]
                     , marker=basename[4]
                     , markersize=args.markersize)

    xlabel='CPU Charge per hour [JPY/h]'
    plt.subplots_adjust(top=args.topFraction,bottom=args.bottomFraction)
    plt.grid(which='major')
    plt.grid(which='minor')
    plt.tick_params(labelsize=args.tickFontSize)

    plt.xlabel(xlabel, fontsize=args.xlabelFontSize)
    if args.xscaleLinear:
        xmin, xmax = plt.xlim()
        xmin=0
    else:
        plt.xscale('log')
        offset=(math.log10(chargeMax)-math.log10(chargeMin))*args.offset
        xmin=math.pow(10,math.log10(chargeMin)-offset)
        xmax=math.pow(10,math.log10(chargeMax)+offset)
    plt.xlim(xmin, xmax)

    ylabel='Number of time step per hour [Step/h]'
    plt.ylabel(ylabel, fontsize=args.ylabelFontSize)
    if args.yscaleLinear:
        ymin, ymax = plt.ylim()
        ymin=0
    else:
        plt.yscale('log')
        offset=(math.log10(nTimeStepPerHourAveMax)-math.log10(nTimeStepPerHourAveMin))*args.offset
        ymin=math.pow(10,math.log10(nTimeStepPerHourAveMin)-offset)
        ymax=math.pow(10,math.log10(nTimeStepPerHourAveMax)+offset)
    plt.ylim(ymin, ymax)
    
    plotEnd(pp)    
            
def plotParallelEfficiency(args,base,basenameArray,xticksNode):
    subfilename="node-pe"
    pp=plotInit(subfilename)

    peMin=HUGE
    peMax=-HUGE
    for basename in basenameArray:
        (node,clockTimeAve,nTimeStepPerHourAve,srAve,peAve,clockTimeFSAve)=result(basename)
        peMin=min(min(peAve),peMin)
        peMax=max(max(peAve),peMax)
        plt.plot(node
                 ,peAve
                 , label=basename[1]+","+basename[7]
                 , linewidth=args.lineWidth
                 , color=basename[2]
                 , linestyle=basename[3]
                 , marker=basename[4]
                 , markersize=args.markersize)    
        
    ylabel='Parallel efficiency (Strong scaling) [%]'
    xmin,xmax,ymin,ymax=plotNode(args,pp,xticksNode,ylabel,peMin,peMax)
    plt.plot([xmin, xmax], [100, 100], 'k-', label="", linewidth=args.lineWidth)
    plotEnd(pp)    

def plotInit(subfilename):
    plotfile=args.csvFilename.replace('.','_')+'-'+subfilename
    if args.xscaleLinear:
        plotfile=plotfile+'-xscalelinear'
    else:
        plotfile=plotfile+'-xscaleLog'
    if args.yscaleLinear:
        plotfile=plotfile+'-yscaleLinear'
    else:
        plotfile=plotfile+'-yscaleLog'
    plotfile=plotfile+'-maxNumberOfSampling_'+str(args.maxNumberOfSampling)
    if args.all==True:
        plotfile+="-all"
    plotfile=plotfile+'.pdf'
    print plotfile
    pp=PdfPages(plotfile)
    return pp
    
def plotNode(args,pp,node,ylabel,yMin,yMax):
    plt.subplots_adjust(top=args.topFraction,bottom=args.bottomFraction)
    plt.grid(which='major')
    plt.grid(which='minor')
    plt.tick_params(labelsize=args.tickFontSize)
    
    plt.xlabel('Number of node [-]', fontsize=args.xlabelFontSize)
    if args.xscaleLinear:
        offset=(node[-1]-node[0])*args.offset
        xmin=node[0]-offset
        xmax=node[-1]+offset
    else:
        offset=(math.log10(node[-1])-math.log10(node[0]))*args.offset
        xmin=math.pow(10,math.log10(node[0])-offset)
        xmax=math.pow(10,math.log10(node[-1])+offset)
        plt.xscale('log')
    plt.xlim(xmin, xmax)
    plt.xticks(node,node,rotation=args.rotation)

    plt.ylabel(ylabel, fontsize=args.ylabelFontSize)
    ymin, ymax = plt.ylim()
    if args.yscaleLinear:
        ymin=0
    else:
        offset=(math.log10(yMax)-math.log10(yMin))*args.offset
        ymin=math.pow(10,math.log10(yMin)-offset)
        ymax=math.pow(10,math.log10(yMax)+offset)
        plt.yscale('log')
    plt.ylim(ymin, ymax)

    return xmin,xmax,ymin,ymax

def plotEnd(pp):
    plt.legend(loc='best', prop={'size':args.legendFontSize})
    pp.savefig()
    plt.clf()
    pp.close()

def plotNumberOfTimeStepPerHour(args,base,basenameArray,xticksNode):
    subfilename="node-NumberOfTimeStepPerHour"
    pp=plotInit(subfilename)

    nTimeStepPerHourAveMin=HUGE
    nTimeStepPerHourAveMax=-HUGE
    for basename in basenameArray:
        (node,clockTimeAve,nTimeStepPerHourAve,srAve,peAve,clockTimeFSAve)=result(basename)
        nTimeStepPerHourAveMin=min(min(nTimeStepPerHourAve),nTimeStepPerHourAveMin)
        nTimeStepPerHourAveMax=max(max(nTimeStepPerHourAve),nTimeStepPerHourAveMax)
        plt.plot(node
                 ,nTimeStepPerHourAve
                 , label=basename[1]+","+basename[7]
                 , linewidth=args.lineWidth
                 , color=basename[2]
                 , linestyle=basename[3]
                 , marker=basename[4]
                 , markersize=args.markersize
        )    

    ylabel='Number of time step per hour [Step/h]'
    xmin,xmax,ymin,ymax=plotNode(args,pp,xticksNode,ylabel,nTimeStepPerHourAveMin,nTimeStepPerHourAveMax)
    plotEnd(pp)    

def plotCPUChargePerTimeStep(args,base,basenameArray,xticksNode,report,year):
    subfilename="node-charge-"+str(report)+"-"+str(year)
    pp=plotInit(subfilename)

    chargeMin=HUGE
    chargeMax=-HUGE
    for basename in basenameArray:
        if report != "both" and basename[6] != "both" and basename[6] != report:
            continue

        (node,clockTimeAve,nTimeStepPerHourAve,srAve,peAve,clockTimeFSAve)=result(basename)
        (label,chargeCoef,chargePerTime,chargePerNodeTime)=charge(basename,node,report,year)
        for i in range(len(label)):
            chargeArray=chargeCoef*(chargePerNodeTime[i]*node+chargePerTime[i])*clockTimeAve/3600.0
            chargeMin=min(min(chargeArray),chargeMin)
            chargeMax=max(max(chargeArray),chargeMax)
            plt.plot(node
                     , chargeArray
                     , label=label[i]
                     , linewidth=args.lineWidth
                     , color=basename[2]
                     , linestyle=basename[3]
                     , marker=basename[4]
                     , markersize=args.markersize)

    ylabel='CPU Charge per time step [JPY]'
    xmin,xmax,ymin,ymax=plotNode(args,pp,xticksNode,ylabel,chargeMin,chargeMax)
    plotEnd(pp)    

#
# main
#
if __name__ == '__main__':
    args=parser()

    if args.all:
        nodeLarge=[1,2,4,8,10,16,24,32,64,96]
    
    for xscaleLinear in [ False,True ]:
        args.xscaleLinear=xscaleLinear
        for yscaleLinear in [ False,True ]:
            args.yscaleLinear=yscaleLinear
            plotNumberOfTimeStepPerHour(args,base,basenameArray,nodeLarge)
            plotParallelEfficiency(args,base,basenameArray,nodeLarge)
            for year in ['FYH28','FYH29']:
                for report in ['both' ]:
                    plotCPUChargePerTimeStep(args, base,basenameArray,nodeLarge,report,year)
                    plotCPUChargePerHourVsNumberOfTimesStepPerHour(args,base,basenameArray,report,year)

