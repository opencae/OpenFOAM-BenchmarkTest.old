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
import argparse
import math

plt.rcParams['ps.useafm'] = True
plt.rcParams['pdf.use14corefonts'] = True
plt.rcParams['text.usetex'] = True
plt.rcParams['text.latex.preamble'] = '\usepackage{sfmath}'

HUGE=1e+30

base="all"
basenameArrayArray=[
    [
        ['n32IAR.csv', "PCG-FDIC", "n32-4.1IAR-system-Icc16_0_4_258-Opt-INTELMPI5_1_3_258",'C1-CG'
         , '--', 2, 'k', '+', 2, 'k', 'none', 10]
        ,['n32IAR.csv', "PPCG-FDIC", "n32-4.1IAR-system-Icc16_0_4_258-Opt-INTELMPI5_1_3_258",'C1-CACG'
          , '-', 2, 'y', '^', 2, 'y', 'none', 10]
     ]
    ,
    [
        ['n32IAR.csv', "PCG-FDIC", "n32-4.1IAR-system-Icc17_0_4_196-Opt-INTELMPI2017_3_196",'C2-CG'
          , '--', 2, 'm', 's', 2, 'm', 'none', 10]
        ,['n32IAR.csv', "PPCG-FDIC", "n32-4.1IAR-system-Icc17_0_4_196-Opt-INTELMPI2017_3_196",'C2-CACG'
          , '-', 2, 'b', 'D', 2, 'b', 'none', 10]
     ]
    ,
    [
        ['n32IAR.csv', "PCG-FDIC", "n32-4.1IAR-system-Icc17_0_2_174-Opt-MPIMVAPICH2_2_2",'C3-CG'
          , '--', 2, 'g', 'x', 2, 'g', 'none', 10]
        ,['n32IAR.csv', "PPCG-FDIC", "n32-4.1IAR-system-Icc17_0_2_174-Opt-MPIMVAPICH2_2_2",'C3-CACG'
          , '-', 2, 'r', 'o', 2, 'r', 'none', 10]
     ]
]
nodeLarge=[32,64,128,256,512,1024,2048,4096]

def parser():
    p = argparse.ArgumentParser()
    p.add_argument('-m','--maxNumberOfSampling', help='Max number of sampling', type=int, default=1)
    p.add_argument('-L','--lineWidth', help='Line width', type=int, default=2)
    p.add_argument('-x','--xscaleLog'
                   , help='x scale Log', action='store_true')
    p.add_argument('-y','--yscaleLog'
                   , help='y scale Log', action='store_true')
    p.add_argument('-o','--offset'
                   , help='offset ratio of x range', type=float, default=0.05)
    p.add_argument('-r','--rotation'
                   , help='rotation degree of xticks', type=float, default=0)
    p.add_argument('--titleFontSize', help='Title font size', type=float, default=13)
    p.add_argument('--legendFontSize', help='Legend font size', type=float, default=11)
    p.add_argument('--xlabelFontSize', help='X label fontsize', type=int, default=13)
    p.add_argument('--ylabelFontSize', help='Y label fontsize', type=int, default=13)
    p.add_argument('--tickFontSize', help='Tick font size', type=float, default=13)
    p.add_argument('--topFraction'
                   , help='Top faction', type=float, default=0.9)
    p.add_argument('--bottomFraction'
                   , help='Bottom faction', type=float, default=0.12)
    p.add_argument('--rightFraction'
                   , help='Right faction', type=float, default=0.99)
    p.add_argument('--leftFraction'
                   , help='Left faction', type=float, default=0.14)
    p.add_argument('--xgridColor', help='Grid color', type=str, default='black')
    p.add_argument('--xgridLineWidth', help='Grid line width', type=float, default=1.0)
    p.add_argument('--xgridLineStyle', help='Grid line style', type=str, default='dotted')
    p.add_argument('--ygridColor', help='Grid color', type=str, default='black')
    p.add_argument('--ygridLineWidth', help='Grid line width', type=float, default=1.0)
    p.add_argument('--ygridLineStyle', help='Grid line style', type=str, default='dotted')
    return p.parse_args()


def result(basename):
    data=np.genfromtxt(basename[0], names=True, delimiter=',', dtype=None)

    idx=np.where(
        (data['fvSolution']==basename[1])
        & (data['solveBatch']==basename[2])
        )

    x=data['nProcs'][idx]
    y=data['ExecutionTimePerStepWOLastStep'][idx]
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

def plotNumberOfTimeStepPerHour(args,base,basenameArray,xticksNode):
    subfilename="node-NumberOfTimeStepPerHour-"+basenameArray[0][2]
    pp=plotInit(subfilename)

    nTimeStepPerHourAveMin=HUGE
    nTimeStepPerHourAveMax=-HUGE
    for basename in basenameArray:
        (node,clockTimeAve,nTimeStepPerHourAve,srAve,peAve,clockTimeFSAve)=result(basename)
        nTimeStepPerHourAveMin=min(min(nTimeStepPerHourAve),nTimeStepPerHourAveMin)
        nTimeStepPerHourAveMax=max(max(nTimeStepPerHourAve),nTimeStepPerHourAveMax)
        plt.plot(
            node
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

    ylabel='Speed [Step/h]'
    xmin,xmax,ymin,ymax=plotNode(args,pp,xticksNode,ylabel)
    ax = plt.gca()
    plotEnd(pp)    
            
def plotRelativeSpeed(args,base,basenameArray,xticksNode):
    subfilename="node-Relative"
    pp=plotInit(subfilename)

    nTimeStepPerHourAveMin=HUGE
    nTimeStepPerHourAveMax=-HUGE
    for basename in basenameArray:
        (node,clockTimeAve,nTimeStepPerHourAve,srAve,peAve,clockTimeFSAve)=result(basename)
        if (basename[1]=='PCG-FDIC'):
            spAveBase=nTimeStepPerHourAve
            continue
        relativeSpeed=nTimeStepPerHourAve/spAveBase*100.0
        print basename[2]
        print "relativeSpeed=",relativeSpeed
        plt.plot(
            node
            ,relativeSpeed
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

    ylabel='Relative speed [\%]'
    xmin,xmax,ymin,ymax=plotNode(args,pp,xticksNode,ylabel)
    ax = plt.gca()
    plt.plot([xmin, xmax], [100, 100], 'k-', label="", linewidth=args.lineWidth)
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
        plt.plot(
            node
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
    plt.plot([xmin, xmax], [100, 100], 'k-', label="", linewidth=args.lineWidth)
    plotEnd(pp)    

def plotInit(subfilename):
    plotfile=subfilename
    if args.xscaleLog:
        plotfile=plotfile+'-xscaleLog'
    else:
        plotfile=plotfile+'-xscalelinear'

    if args.yscaleLog:
        plotfile=plotfile+'-yscaleLog'
    else:
        plotfile=plotfile+'-yscaleLinear'

    plotfile=plotfile+'-maxNumberOfSampling_'+str(args.maxNumberOfSampling)
    plotfile=plotfile+'.pdf'
    print plotfile
    pp=PdfPages(plotfile)
    return pp
    
def plotNode(args,pp,node,ylabel):
    plt.subplots_adjust(
        top=args.topFraction
        ,bottom=args.bottomFraction
        ,left=args.leftFraction
        ,right=args.rightFraction
    )
    plt.grid(True
             , which='both'
             , axis='y'
             , color=args.ygridColor
             , linestyle=args.ygridLineStyle
             , linewidth=args.ygridLineWidth)
    plt.grid(True
             , which='major'
             , axis='x'
             , color=args.xgridColor
             , linestyle=args.xgridLineStyle
             , linewidth=args.xgridLineWidth)
    plt.tick_params(
        labelsize=args.tickFontSize
    )
    plt.tick_params(
        axis='x',
        which='minor',
        bottom='off',
        top='off'
    )
    
    plt.xlabel('Number of MPI processes', fontsize=args.xlabelFontSize)
    if args.xscaleLog:
        offset=(math.log10(node[-1])-math.log10(node[0]))*args.offset
        xmin=math.pow(10,math.log10(node[0])-offset)
        xmax=math.pow(10,math.log10(node[-1])+offset)
        plt.xscale('log')
    else:
        offset=(node[-1]-node[0])*args.offset
        xmin=0
        xmax=node[-1]+1

    plt.xlim(xmin, xmax)
    plt.xticks(node,node,rotation=args.rotation)

    plt.ylabel(ylabel, fontsize=args.ylabelFontSize)
    ymin, ymax = plt.ylim()
    if args.yscaleLog:
        plt.yscale('log')

    return xmin,xmax,ymin,ymax

def plotEnd(pp):
    plt.legend(loc='best', prop={'size':args.legendFontSize})
    pp.savefig( bbox_inches="tight", pad_inches=0.03)
    plt.clf()
    pp.close()

#
# main
#
if __name__ == '__main__':
    args=parser()

    args.xscaleLog=True
    args.yscaleLog=True
    for basenameArray in basenameArrayArray:
        plotNumberOfTimeStepPerHour(args,base,basenameArray,nodeLarge)

    args.xscaleLog=True
    args.yscaleLog=False
    basenameArray=[flatten for inner in basenameArrayArray for flatten in inner]
    print basenameArray
    plotRelativeSpeed(args,base,basenameArray,nodeLarge)
