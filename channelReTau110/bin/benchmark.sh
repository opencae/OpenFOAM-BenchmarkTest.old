#!/bin/bash

makeCaseSettings()
{
    cat >  caseSettings <<EOF
blockMeshDict
{
  mx $mx;
  my $my;
  mz $mz;
}

controlDict
{
  deltaT          $deltaT;
  endTime         $endTime;
  libs            $libs;
}

decomposeParDict
{
  numberOfSubdomains  $numberOfSubdomains;

  method scotch;

  simpleCoeffs
  {
      nx 4;
      ny 2;
      nz 2;
  }
}

fvSolution
{
  solvers
  {
      p
      {
          solver           $solver;
          smoother         $smoother;
          preconditioner   $preconditioner;
      }
  }
}

turbulenceProperties
{
  simulationType $simulationType;
}

LESProperties
{
  LESModel $LESModel;
  delta $delta;
}
EOF
}

LimitNumberOfBatchQueue()
{
    while : 
    do
	nq=$(NumberOfBatchQueue)
        [ "$nq" -lt "$MAX_NUMBER_OF_QUEUE" ] &&  break
	sleep 1
    done
}
    
# Source configulation file
. benchmark.conf

mpi="00001"
solver="PCG"
preconditioner="DIC"
smoother="DIC"
simulationType="laminar"
LESModel="laminar"
delta="cubeRootVol"
libs=\"\"

templateDir=$PWD/../template
batchScriptDir=$PWD/batchScript

loop=1
while [ "$loop" -le "$MAX_NUMBER_OF_LOOP" ]
do
    echo "loop= $loop"
    loop=`expr $loop + 1`
    for n in ${nArray[@]}
    do
	echo "n= $n"

	mx=`echo $n | awk '{printf("%d", 120*$1^(1./3.) + 0.5)}'`
	my=`echo $n | awk '{printf("%d", 65*$1^(1./3.) + 0.5)}'`
	mz=`echo $n | awk '{printf("%d", 48*$1^(1./3.) + 0.5)}'`

	deltaT=`echo $n | awk '{printf("%f", 0.004/($1^(1./3.)))}'`
	endTime=`echo $deltaT | awk '{printf("%f", $1*11)}'`

	dir=n_$n

	if [ ! -d $dir ];then
	    cp -r $templateDir $dir
	fi

	(cd $dir
	    makeCaseSettings

	    if [ ! -f constant/polyMesh/faces ];then
		batchFile=blockMesh.sh
		if [ -f $batchScriptDir/$batchFile ];then
		    cp $batchScriptDir/$batchFile ./
		    LimitNumberOfBatchQueue
		    BatchSubmit $batchFile 1

		    while [ ! -f constant/polyMesh/faces ];do
			sleep 1
		    done
		else
		    blockMesh >& log.blockMesh
		fi
	    fi

	    for mpi in ${mpiArray[@]}
	    do
		echo "mpi= $mpi"
		dir2=mpi_$mpi
		
		if [ ! -d $dir2 ];then
		    cp -r $templateDir $dir2
		fi
		
		(cd $dir2
		    (cd constant
			rm -rf polyMesh
			ln -s ../../constant/polyMesh .
		    )

		    numberOfSubdomains=`echo "$mpi" | bc` 

		    makeCaseSettings
		    
		    if [ "$mpi" -gt 1 ];then 
			if [ ! -d processor0 ];then
			    batchFile=decomposePar.sh
			    if [ -f $batchScriptDir/$batchFile ];then
				cp $batchScriptDir/$batchFile ./
				LimitNumberOfBatchQueue
				BatchSubmit $batchFile 1

				processorLast=`expr $mpi - 1`
				while [ ! -f processor${processorLast}/0/p ];do
				    sleep 1
				done
			    else
				decomposePar -cellDist >& log.decomposePar
			    fi
			fi
		    fi

		    for simulationTypes in ${simulationTypesArray[@]}
		    do
			simulationType=${simulationTypes%%-*}
			LESModels=${simulationTypes##*LESModel_}
			LESModel=${LESModels%%-*}
			delta=${simulationTypes##*delta_}
			if [ "$LESModel" == "WALE" ];then
			    libs="\"libincompressibleWALE.so\""
			else
			    libs=""
			fi

			for solvers in ${solversArray[@]}
			do
			    solver=${solvers%%-*}
			    preconditioner=${solvers##*preconditioner_}
			    smoother=${solvers##*smoother_}

			    dir3=simulationType_$simulationTypes-solver_$solvers

			    if [ ! -d $dir3 ];then
				cp -r ../../../template $dir3
			    fi

			    (cd $dir3
				echo "dir= $dir/$dir2/$dir3"

				ndone=`ls log.*[0-9] | wc -l`
				if [ "$ndone" -ge "$MAX_NUMBER_OF_LOOP" ];then
				    echo "Allready run in $MAX_NUMBER_OF_LOOP time(s). Skip running" 
				    continue
				fi

				(cd constant
				    rm -rf polyMesh
				    ln -s ../../constant/polyMesh .
				)

				if [ "$mpi" -gt 1 ];then 
				    for p in ../processor*
				    do
					b=`basename $p`
					rm -rf $b
					mkdir $b
					(cd $b
					    ln -s ../../$b/{0,constant} .
					)
				    done
				fi

				makeCaseSettings

				if [ "$solver" == "PCG" -a ${preconditioner%%+*} == "GAMG" ];then
				    smoother=${preconditioner##*+}
				    mv system/fvSolution system/fvSolution.orig
				    sed \
"s/\$:fvSolution.solvers.p.preconditioner;/\
{preconditioner GAMG;\
agglomerator faceAreaPair;\
nCellsInCoarsestLevel 100;\
mergeLevels 1;\
smoother ${smoother};}/"\
 system/fvSolution.orig > system/fvSolution
				fi

				batchFile=solve.sh
				if [ -f $batchScriptDir/$batchFile ];then
				    cp $batchScriptDir/$batchFile ./
				    LimitNumberOfBatchQueue
				    BatchSubmit $batchFile $mpi
				else
				    if [ "$mpi" -gt 1 ];then 
					mpiexec -np $mpi \
					    pimpleFoam -parallel >& log.pimpleFoam.$$
				    else
					pimpleFoam >& log.pimpleFoam.$$
				    fi
				fi
			    )
			done
		    done
		)
	    done
	)
    done
done
