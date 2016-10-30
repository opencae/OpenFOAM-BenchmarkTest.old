#!/bin/bash

application=pre.sh

(
env
blockMesh
) >& log.${application}.$1

touch ${application}.done

#------------------------------------------------------------------------------
