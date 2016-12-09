#!/bin/bash

# Source tutorial run functions
. $WM_PROJECT_DIR/bin/tools/RunFunctions

application=pre.sh

(
env
blockMesh
) >& log.${application}

touch ${application}.done
