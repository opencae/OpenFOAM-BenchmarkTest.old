#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import os
import matplotlib as mpl
mpl.use('Agg')
import numpy as np
import pylab
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.ticker import ScalarFormatter
from matplotlib.ticker import AutoMinorLocator
import argparse
import math
import re

HUGE=1e+30

base="all"
basenameArray=[
    ['../Oakforest-PACS-mesh_3M-No4/all.csv', "PCG-DIC", "n64-f-9-v1612+-system-Icc2017_4_196KNL-Opt-INTELMPI2017_3_196",'Oakforest-PACS'
     , '-', 2, 'k', 'o', 2, 'k', 'none', 8, 32, 'open']
    ,['../Reedbush_U-mesh_3M-No0/all.csv', "PCG-DIC", 'OF230_Gcc_SGIMPI','Reedbush-U'
     , '-', 2, 'y', 's', 2, 'y', 'none', 8, -1, 'open']
    ,['../Oakleaf_FX-mesh_3M-No1/all.csv', "PCG-DIC", 'OF230_Gcc_OpenMPI','Oakleaf-FX'
      , '-', 2, 'r', 'o', 2, 'r', 'none', 8, 48, 'open']
    ,['../TSUBAME_S-mesh_3M-No1/all.csv', "PCG-DIC", 'OF230_Gcc_OpenMPI','TSUBAME S'
    , '-', 2, 'c', 'v', 2, 'c', 'none', 8, -1, 'both']
    ,['../TSUBAME_G-mesh_3M-No1/all.csv', "PCG-DIC", 'OF230_Gcc_OpenMPI','TSUBAME G'
     , '-', 2, 'g', '^', 2, 'g', 'none', 8, -1, 'both']
    ,['../FOCUS_A-mesh_3M-No4/all.csv', "PCG-DIC", 'OF230_Gcc_OpenMPI','FOCUS A'
     , '-', 2, '0.0', '<', 2, '0.0', 'none', 8, -1, 'close']
    ,['../FOCUS_D-mesh_3M-No4/all.csv', "PCG-DIC", 'OF230_Gcc_OpenMPI','FOCUS D'
     , '-', 2, '0.2', 'D', 2, '0.2', 'none', 8, -1, 'close']
    ,['../FOCUS_F-mesh_3M-No1/all.csv', "PCG-DIC", 'OF230_Gcc_OpenMPI','FOCUS F'
     , '-', 2, '0.4', '>', 2, '0.4', 'none', 8, -1, 'close']
    ,['../FOCUS_H-mesh_3M-No1/all.csv', "PCG-DIC", 'OF230_Gcc_OpenMPI','FOCUS H'
     , '-', 2, '0.6', 'H', 2, '0.6', 'none', 8, 32, 'close']
    ,['../AWS_c4.8xlarge-mesh_3M-No3/all.csv', "PCG-DIC", 'OF230_Gcc_OpenMPI','EC2 c4.8xlarge'
     , '-', 2, 'm', 'x', 2, 'm', 'none', 8, -1, 'close']
    ,['../Azure_A9-mesh_3M-No04/all.csv', "PCG-DIC", 'OF230_Gcc_OpenMPI','Azure A9'
     , '-', 2, 'b', '+', 2, 'b', 'none', 8, -1, 'close']
    ]

def parser():
    p = argparse.ArgumentParser()
    p.add_argument('-a','--all', help='plot all data', action='store_true')
    p.add_argument('-m','--maxNumberOfSampling', help='Max number of sampling', type=int, default=1)
    p.add_argument('-L','--lineWidth', help='Line width', type=int, default=2)
    p.add_argument('-x','--xscaleLinear'
                   , help='x scale Linear', action='store_true')
    p.add_argument('-y','--yscaleLinear'
                   , help='y scale Linear', action='store_true')
    p.add_argument('-o','--offset'
                   , help='offset ratio of x range', type=float, default=0.03)
    p.add_argument('-r','--rotation'
                   , help='rotation degree of xticks', type=float, default=0)
    p.add_argument('--titleFontSize', help='Title font size', type=int, default=16)
    p.add_argument('--legendFontSize', help='Legend font size', type=int, default=9.5)
    p.add_argument('--xlabelFontSize', help='X label fontsize', type=int, default=16)
    p.add_argument('--ylabelFontSize', help='Y label fontsize', type=int, default=16)
    p.add_argument('--tickFontSize', help='Tick font size', type=int, default=16)
    p.add_argument('--topFraction'
                   , help='Top faction', type=float, default=0.98)
    p.add_argument('--bottomFraction'
                   , help='Bottom faction', type=float, default=0.10)
    p.add_argument('--leftFraction'
                   , help='Left faction', type=float, default=0.15)
    p.add_argument('--rightFraction'
                   , help='Right faction', type=float, default=0.95)
    return p.parse_args()


def result(basename):
    data=np.genfromtxt(basename[0], names=True, delimiter=',', dtype=None)

    nNodesMax=10e+30
    if basename[12]>0:
        nNodesMax=basename[12]

    idx=np.where(
        (data['fvSolution']==basename[1])
        & (data['solveBatch']==basename[2])
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

def plotInit(subfilename):
    plotfile=subfilename
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
    plt.subplots_adjust(
        top=args.topFraction
        ,bottom=args.bottomFraction
        ,left=args.leftFraction
        ,right=args.rightFraction
        )
    plt.grid(which='major',axis='x')
    plt.grid(which='major',axis='y',linestyle='-')
    plt.grid(which='minor',axis='y',linestyle=':')
    plt.tick_params(labelsize=args.tickFontSize)
    
    plt.xlabel('Number of nodes', fontsize=args.xlabelFontSize)
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
        plt.grid(which='minor',axis='y',linestyle=':')
    else:
        offset=(math.log10(yMax)-math.log10(yMin))*args.offset
#        ymin=math.pow(10,math.log10(yMin)-offset)
        ymin=math.pow(10,math.floor(math.log10(yMin)))
#        ymax=math.pow(10,math.log10(yMax)+offset)
        ymax=math.pow(10,math.ceil(math.log10(yMax)))
        ymax=5e+4
#        ymax=1e+5
        plt.yscale('log')
        plt.yticks([100,1000,10000,50000],[100,1000,10000,50000])
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
        , label=basename[3]
        , linestyle=basename[4]
        , linewidth=basename[5]
        , color=basename[6]
        , marker=basename[7]
        , markeredgewidth = basename[8]
        , markeredgecolor = basename[9]
        , markerfacecolor=basename[10]
        , markersize=basename[11]
        )    

    ylabel='Speed [Steps/h]'
    xmin,xmax,ymin,ymax=plotNode(args,pp,xticksNode,ylabel,nTimeStepPerHourAveMin,nTimeStepPerHourAveMax)
    linearY=0.5*1e+4
    plt.plot([xmin, xmax], [linearY*xmin, linearY*xmax/xmin], 'k--', label="", linewidth=2)
    plt.annotate("Linear"
                 , rotation=30
                 , ha="center", va="center"
                 , xy=(3, (3+1)*linearY)
                 , annotation_clip=False
                 , fontsize=16)
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
        , label=basename[3]
        , linestyle=basename[4]
        , linewidth=basename[5]
        , color=basename[6]
        , marker=basename[7]
        , markeredgewidth = basename[8]
        , markeredgecolor = basename[9]
        , markerfacecolor=basename[10]
        , markersize=basename[11]
        )
        
    ylabel='Parallel efficiency (Strong scaling) [%]'
    xmin,xmax,ymin,ymax=plotNode(args,pp,xticksNode,ylabel,peMin,peMax)
    ax = plt.gca()
    if args.yscaleLinear==True:
        ax.yaxis.set_minor_locator(AutoMinorLocator(5))
    plt.plot([xmin, xmax], [100, 100], 'k-', label="", linewidth=args.lineWidth)
    plotEnd(pp)    

def charge(basename,node,report,year):
    chargePerTime=[]
    chargePerNodeTime=[]
    chargeCoef=np.ones(len(node))
    label=[basename[3]]
    if basename[3] == "FOCUS A":
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

    elif basename[3] == "FOCUS D":
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

    elif basename[3] == "FOCUS F":
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
                    chargeCoef[i]=425./500.
                elif node[i]<=10:
                    chargeCoef[i]=400./500.
                else:
                    chargeCoef[i]=375./500.

    elif basename[3] == "FOCUS H":
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

    elif basename[3] == "Azure A9":
        chargePerTime=[31.42*1.08]
        chargePerNodeTime=[198.90*1.08]
    elif basename[3] == "EC2 c4.8xlarge":
        chargePerNodeTime=[295.8]
        chargePerTime=[132.8]
    elif basename[3] == "Oakleaf-FX":
        chargePerTime=[0,0]
        if year=='FYH27':
            chargePerNodeTime=[180800/8640]
        elif year=='FYH28':
            chargePerNodeTime=[77500/8640]
        elif year=='FYH29':
            chargePerNodeTime=[55800/8640]
        else:
            print "Unknown year"
            exit(1)
    elif basename[3] == "Reedbush-U":
        chargePerTime=[0,0]
        if year=='FYH28':
            chargePerNodeTime=[62000/2880]
        elif year=='FYH29':
            chargePerNodeTime=[46500/2880]
        else:
            print "Unknown year"
            exit(1)
            
    elif basename[3] == "Oakforest-PACS":
        chargePerTime=[0,0]
        chargePerNodeTime=[62000/5760]

    elif basename[3] == "TSUBAME S" or basename[3] =="TSUBAME G":
        if basename[3] == "TSUBAME G":
            for i in range(len(node)):
                chargeCoef[i]=0.5
        chargePerTime=[0]
        if report == "close":
            chargePerNodeTime=[10*4*4*1.08]
        else:
            chargePerNodeTime=[10*4*1.08]

    if  basename[3] == "Oakleaf-FX" or basename[3] == "Reedbush-U" or basename[3] == "Oakforest-PACS":
        if  basename[3] == "Oakleaf-FX":
            normalChargeNodeMax=12
        elif  basename[3] == "Reedbush-U":
            normalChargeNodeMax=4
        elif  basename[3] == "Oakforest-PACS":
            normalChargeNodeMax=8
        else:
            print "Unknown system"
            exit(1)

        for i in range(len(node)):
            if node[i]<=normalChargeNodeMax:
                chargeCoef[i]=1.0
            else:
                chargeCoef[i]=(normalChargeNodeMax+(node[i]-normalChargeNodeMax)*2.0)/node[i]

    return label,chargeCoef,chargePerTime,chargePerNodeTime

def plotCPUChargePerTimeStep(args,base,basenameArray,xticksNode,report,year):
    subfilename="node-charge-"+str(report)+"-"+str(year)
    pp=plotInit(subfilename)

    chargeMin=HUGE
    chargeMax=-HUGE
    for basename in basenameArray:
        if report != "both" and basename[13] != "both" and basename[13] != report:
            continue

        (node,clockTimeAve,nTimeStepPerHourAve,srAve,peAve,clockTimeFSAve)=result(basename)
        (label,chargeCoef,chargePerTime,chargePerNodeTime)=charge(basename,node,report,year)
        for i in range(len(label)):
            chargeArray=chargeCoef*(chargePerNodeTime[i]*node+chargePerTime[i])*clockTimeAve/3600.0
            chargeMin=min(min(chargeArray),chargeMin)
            chargeMax=max(max(chargeArray),chargeMax)
            plt.plot(node
                     , chargeArray
                     , label=basename[3]
                     , linestyle=basename[4]
                     , linewidth=basename[5]
                     , color=basename[6]
                     , marker=basename[7]
                     , markeredgewidth = basename[8]
                     , markeredgecolor = basename[9]
                     , markerfacecolor=basename[10]
                     , markersize=basename[11]
                     )

    ylabel='CPU Charge per time step [JPY]'
    xmin,xmax,ymin,ymax=plotNode(args,pp,xticksNode,ylabel,chargeMin,chargeMax)
    plotEnd(pp)    

def plotCPUChargePerHourVsNumberOfTimesStepPerHour(args,base,basenameArray,report,year):

    subfilename="ChargePerHour-NumerOfTimeStepPerHour-"+str(report)+"-"+str(year)
    pp=plotInit(subfilename)

    chargeMin=HUGE
    chargeMax=-HUGE
    nTimeStepPerHourAveMin=HUGE
    nTimeStepPerHourAveMax=-HUGE
    for basename in basenameArray:
        if report != "both" and basename[13] != "both" and basename[13] != report:
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
                     , label=basename[3]
                     , linestyle=basename[4]
                     , linewidth=basename[5]
                     , color=basename[6]
                     , marker=basename[7]
                     , markeredgewidth = basename[8]
                     , markeredgecolor = basename[9]
                     , markerfacecolor=basename[10]
                     , markersize=basename[11]
                     )

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

    ylabel='Speed [Steps/h]'
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

#
# main
#
if __name__ == '__main__':
    args=parser()

    nodeLarge=[1,2,4,8,12,16,24,32,48]
    
    args.xscaleLinear=False
    args.yscaleLinear=True
    plotParallelEfficiency(args,base,basenameArray,nodeLarge)
    args.yscaleLinear=False
    plotNumberOfTimeStepPerHour(args,base,basenameArray,nodeLarge)

    year='FYH29'
    for report in ['close', 'open', 'both']:
        args.xscaleLinear=False
        args.yscaleLinear=True
        plotCPUChargePerTimeStep(args, base,basenameArray,nodeLarge,report,year)

        for flag in [ True, False ]:
            args.xscaleLinear=flag
            args.yscaleLinear=flag
            plotCPUChargePerHourVsNumberOfTimesStepPerHour(args,base,basenameArray,report,year)
