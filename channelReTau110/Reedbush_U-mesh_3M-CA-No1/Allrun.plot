#!/bin/sh

rm -f *.{eps,pdf}

../bin/plot.py \
    n32IAR.csv \
    --ExecutionTimePerStep ExecutionTimePerStepWOLastStep \
    --sph \
    -l "Intel MPI 5.1.3.258" "MVAPICH2 2.2" "Intel MPI 2017.3.196"

../bin/plot.py \
    n32IAR.csv \
    --ExecutionTimePerStep ExecutionTimePerStepWOLastStep \
    -y \
    --pe \
    --solution \
    -l "Intel MPI 5.1.3.258" "MVAPICH2 2.2" "Intel MPI 2017.3.196"

caseName=${PWD##*/}
convert -density 150 -resize 900x900 *.eps ${caseName}.pdf

gs \
-dNOPAUSE \
-dBATCH \
-dQUIET \
-sDEVICE=pdfwrite \
-dCompatibilityLevel=1.4 \
-dAutoFilterGrayImages=true \
-dGrayImageFilter=/DCTEncode \
-dEncodeGrayImages=true \
-dDownsampleGrayImages=true \
-dGrayImageDownsampleThreshold=1.5 \
-dGrayImageDownsampleType=/Bicubic \
-dGrayImageResolution=150 \
-dMonoImageFilter=/CCITTFaxEncode \
-dEncodeMonoImages=true \
-dDownsampleMonoImages=true \
-dMonoImageDownsampleThreshold=1.5 \
-dMonoImageDownsampleType=/Bicubic \
-dMonoImageResolution=300 \
-dAutoFilterColorImages=true \
-dColorImageFilter=/DCTEncode \
-dEncodeColorImages=true \
-dColorImageResolution=150 \
-dColorImageDownsampleThreshold=1.5 \
-dColorImageDownsampleType=/Bicubic \
-sOutputFile=${caseName}-compressed.pdf \
${caseName}.pdf

rm ${caseName}.pdf

../Reedbush_U-mesh_0.37M-CA-No1/comparison.py

