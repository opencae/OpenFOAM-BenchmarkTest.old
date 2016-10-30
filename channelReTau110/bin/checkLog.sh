#/bin/bash

atexit()
 {
      [[ -n $tmpdir ]] && rm -rf "$tmpdir"
}

separateLog()
{
    local log=$1

    grep "^Courant Number" $log | cut -d ' ' -f 4,6  > $log.Co
    grep "Solving for Ux," $log | awk -F ' ' '{print $8,$12,$15}' | $SED "s/, */ /g" > $log.Ux
    grep "Solving for Uy," $log | awk -F ' ' '{print $8,$12,$15}' | $SED "s/, */ /g" > $log.Uy
    grep "Solving for Uz," $log | awk -F ' ' '{print $8,$12,$15}' | $SED "s/, */ /g" > $log.Uz
    grep "Solving for p," $log | awk -F ' ' '(NR%2==1) {print $8,$12,$15}' | $SED "s/, */ /g" > $log.p0
    grep "Solving for p," $log | awk -F ' ' '(NR%2==0) {print $8,$12,$15}' | $SED "s/, */ /g" > $log.p1
    grep "ExecutionTime =" $log | awk -F ' ' '{print $3,$7}' > $log.time
}

calcRMSEandMaxErr()
{
    local file1=$1
    local column1=$2
    local file2=$3
    local column2=$4
    local nStepMin=$5

    cut -d ' ' -f $column1 $file1 | head -n $nStepMin > $tmpdir/file1
    cut -d ' ' -f $column2 $file2 | head -n $nStepMin > $tmpdir/file2
    paste -d ' ' $tmpdir/file1 $tmpdir/file2 \
    |  awk -F ' ' \
'BEGIN {n=0;Mean;RMSE=0;ErrMax=0;} \
{\
Mean+=$1;\
Err=sqrt(($2-$1)^2);\
RMSE=RMSE+Err^2;\
if (ErrMax<Err) {ErrMax=Err};\
n++;\
} \
END {Mean/=n;RMSE=sqrt(RMSE/n);\
printf("%g,%g,%g,%g,%g",Mean,RMSE,RMSE/Mean*100,ErrMax,ErrMax/Mean*100);}'

}

tmpdir=`mktemp -d`
echo $tmpdir
#trap atexit EXIT
#trap 'trap - EXIT; atexit; exit -1' SIGHUP SIGINT SIGTERM

if [ "$#" -ne 2 ];then
        cat<<USAGE
Usage: ${0##*/} basedir basename
USAGE
    exit 1
fi

basedir=$1
basename=$2

# Source configuration file
. benchmark.conf

caseDir=cases
csvFile=${basedir##*/}.$basename.csv


if [ "$(uname)" == "Darwin" ]
then
    SED=gsed
else
    SED=sed
fi

application=`$SED -ne 's/^ *application\s*\([^\s]*\)\s*;.*$/\1/p' cases/system/controlDict`

echo $application

line="#decomposeParDict,fvSolution,solveBatch"
line="$line,Filename"
line="$line,nStepBase,nStep"
line="$line,UxMean,UxRMSE,UxRMSE/UxMean[%],UxErrMax,UxErrMax/UxMean[%]"
line="$line,UyMean,UyRMSE,UyRMSE/UyMean[%],UyErrMax,UyErrMax/UyMean[%]"
line="$line,UzMean,UzRMSE,UzRMSE/UzMean[%],UzErrMax,UzErrMax/UzMean[%]"
line="$line,p0Mean,p0RMSE,p0RMSE/p0Mean[%],p0ErrMax,p0ErrMax/p0Mean[%]"
line="$line,p1Mean,p1RMSE,p1RMSE/p1Mean[%],p1ErrMax,p1ErrMax/p1Mean[%]"
line="$line,CoMean,CoMeanRMSE,CoMeanRMSE/CoMean[%],CoMeanErrMax,CoMeanErrMax/CoMean[%]"
line="$line,CoMax,CoMaxRMSE,CoMaxRMSE/CoMax[%],CoMaxErrMax,CoMaxErrMax/CoMax[%]"
line="$line,ExecutionTimePerStepBase,ExecutionTimePerStep,ExecutionTimePerStep/Base[%]"

echo $line > $csvFile

for decomposeParDict in ${decomposeParDictArray[@]}
do
    for fvSolution in ${fvSolutionArray[@]}
    do
	
	basenameFile=`ls $basedir/cases/$decomposeParDict/$fvSolution/$basename/log.${application}.[0-9]* | head -n 1`
	echo $basenameFile

	separateLog $basenameFile
    
	nStepBase=`wc -l < $basenameFile.Co`
	echo "nStepBase=$nStepBase"

	for solveBatch in ${solveBatchArray[@]}
	do
	    Dir=$caseDir/$decomposeParDict/$fvSolution/$solveBatch
	    for log in $Dir/log.${application}.*[0-9]
	    do
		[ "${log##*/}" == "log.pimpleFoam.*[0-9]" ] && continue
		[ -f $log ] || continue
		[ -f $log.done ] || continue

		echo $log

		separateLog $log

		nStep=`wc -l < $log.Co`
		nStepMin=$nStepBase
		[ "$nStepMin" -gt "$nStep" ] && nStepMin=$nStep
		echo "nStepMin= $nStepMin"

		CoMeanErr=`calcRMSEandMaxErr $basenameFile.Co 1 $log.Co 1 $nStepMin`
		CoMaxErr=`calcRMSEandMaxErr $basenameFile.Co 2 $log.Co 2 $nStepMin`
		UxErr=`calcRMSEandMaxErr $basenameFile.Ux 3 $log.Ux 3 $nStepMin`
		UyErr=`calcRMSEandMaxErr $basenameFile.Uy 3 $log.Uy 3 $nStepMin`
		UzErr=`calcRMSEandMaxErr $basenameFile.Uz 3 $log.Uz 3 $nStepMin`
		p0Err=`calcRMSEandMaxErr $basenameFile.p0 3 $log.p0 3 $nStepMin`
		p1Err=`calcRMSEandMaxErr $basenameFile.p1 3 $log.p1 3 $nStepMin`

		ExecutionTimePerStepBase=`head -n $nStepMin $basenameFile.time | \
awk -F ' ' 'BEGIN {t0=$1} {t1old=t1;t1=$1;} END {printf "%g",(t1old-t0)/(NR-1)}'`
		ExecutionTimePerStep=`head -n $nStepMin $log.time | \
awk -v ExecutionTimePerStepBase=$ExecutionTimePerStepBase \
-F ' ' 'BEGIN {t0=$1} {t1old=t1;t1=$1} \
END {t=(t1old-t0)/(NR-1);printf "%g,%g",t,t/ExecutionTimePerStepBase*100}'`


		diff=$log.diff.${basedir##*/}.$basename
		diff -u $basenameFile $log > $diff 2>/dev/null

		line="$decomposeParDict,$fvSolution,$solveBatch"
		line="$line,${log##*/},$nStepBase,$nStep"
		line="$line,$UxErr,$UyErr,$UzErr,$p0Err,$p1Err,$CoMeanErr,$CoMaxErr"
		line="$line,$ExecutionTimePerStepBase,$ExecutionTimePerStep"
		echo $line >> $csvFile
	    done
	done
    done
done
