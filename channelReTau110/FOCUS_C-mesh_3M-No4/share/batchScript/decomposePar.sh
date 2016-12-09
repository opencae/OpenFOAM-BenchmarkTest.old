#!/bin/bash

# Source tutorial run functions
. $WM_PROJECT_DIR/bin/tools/RunFunctions

application=decomposePar.sh

log=log.${application}
(
    env
    decomposePar -cellDist
) >& $log

grep "^End" $log >& /dev/null
[ $? -eq 0 ] && touch ${application}.done
