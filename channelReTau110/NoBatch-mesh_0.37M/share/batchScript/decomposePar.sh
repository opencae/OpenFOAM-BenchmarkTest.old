#!/bin/bash

application=decomposePar.sh

(
    env
    decomposePar -cellDist 
) >& log.${application}.$1

touch ${application}.done
