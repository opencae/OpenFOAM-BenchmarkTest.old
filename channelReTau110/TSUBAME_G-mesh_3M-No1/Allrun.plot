#!/bin/sh

rm -f *.{eps,pdf}

CSV=PCG-DIC.csv

../bin/plot.py \
    $CSV \
    --ExecutionTimePerStep ExecutionTimePerStepWOLastStep \
    --loop \
    --sph

../bin/plot.py \
    $CSV \
    --ExecutionTimePerStep ExecutionTimePerStepWOLastStep \
    -y \
    --pe

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
