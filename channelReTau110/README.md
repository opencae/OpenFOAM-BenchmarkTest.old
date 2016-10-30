# OpenFOAM-BenchmarkTest-channelReTau110 "OpenFOAM Benchmark Test for Channel Flow (Re_tau=110)"

## 概要

OpenFOAM-BenchmarkTest-channelReTau110は
オープンCAE学会V&V委員会OpenFOAMベンチマークテストWGで作成した，
チャネル流れ(Re_tau=110)channelReTau110[1]を対象とした
ベンチマークテストである．
52ステップのみ計算を行い，
第1ステップから第51ステップまでの1ステップあたりの平均解析時間を算出し，
計算時間の比較および並列化効率を調べる．

## ファイルの構成

    README.md         このファイル
    bin/              スクリプト
      benchmark.sh      ベンチマーク実行スクリプト
      cleanFailLog.sh   完了しなかったソルバログの消去・移動スクリプト
      plot.py           ベンチマーク結果のプロット用Pythonスクリプト
      table.sh          ベンチマーク結果の集計スクリプト   
    src/              ソース
    template/         channelReTau110のケースディレクトリ
    NoBatch-mesh_3M/  非バッチジョブシステムでの3M格子の設定例
      all               ベンチマークケース設定ファイル(ファイル名任意)
      share/            ベンチマークケース共有設定ファイルのディレクトリ
        batchScript/      バッチスクリプトのディレクトリ
          decomposePar.sh   領域分割バッチスクリプト
          pre.sh            前処理バッチスクリプト
          solve/            ソルバー解析バッチスクリプトのディレクトリ
        decomposeParDict/ 領域分割設定ファイルのディレクトリ
          template          scotch型領域分割設定ファイルのテンプレート
        fvSolution/       解法設定ファイルのディレクトリ

その他のディレクトリはベンチマークのテスト結果である．

## ベンチマークの設定
### 非バッチジョブシステム用ベンチマークケース設定
ベンチマークケースの設定ファイル名は任意のファイルで良いが，
例えばallとすると以下のように設定する．

NoBatch-mesh_3M/all
```
# 領域分割設定検討ケース配列
decomposeParDictArray=(
mpi_0010-method_scotch
mpi_0020-method_scotch
)

# 解法設定の検討ケース配列
fvSolutionArray=(
GAMG-DIC
PCG-DIC
)

# ソルバー解析バッチスクリプトの検討ケース配列
solveBatchArray=(
OpenFOAM
)

MAX_NUMBER_OF_LOOP=1  # ベンチマークテストの繰り返し数

BATCH_PRE=0           # 前処理のバッチジョブでの実行(0=しない)
BATCH_DECOMPOSEPAR=0  # 領域分割のバッチジョブでの実行(0=しない)
BATCH_SOLVE=0         # ソルバ解析のバッチジョブでの実行(0=しない)

# ケースファイルの作成
# 格子分割数(mx,my,mz)，時間刻み(deltaT)，終了時刻(endTime)を設定する．
# なお，格子分割数の比mx:my:mzは120:65:48とする．
# また，時間刻みdeltaTは0.48/mx，endTimeはdeltaT*52の値にする．
makeCases()
{
    local mx=240
    local my=130
    local mz=96
    local deltaT=0.002
    local endTime=0.104

    cp -a ../template cases

    sed -i \
    -e s/"^ *mx .*"/"mx $mx;"/ \
    -e s/"^ *my .*"/"my $my;"/ \
    -e s/"^ *mz .*"/"mz $mz;"/ \
    cases/system/blockMeshDict

    cp cases/system/blockMeshDict cases/constant/polyMesh/

    sed -i \
    -e s/"^ *deltaT .*"/"deltaT $deltaT;"/ \
    -e s/"^ *endTime .*"/"endTime $endTime;"/ \
    cases/system/controlDict
}

# MPIプロセス実行ホストの設定ファイルhostfileを生成する関数
#
# 1ノードでの実行用に設定されているので，多ノードで実行する場合には
# 変更する必要がある．
# ただし，バッチジョブシステムを用いる場合には設定不要．
GenerateHostFile()
{
  local mpi=$1
  (
    i=0
    while [ $i -lt $mpi ]
    do
      echo "localhost" 
      i=`expr $i + 1`
    done
  ) > hostfile

```

decomposeParDictArrayには
領域分割設定ファイルのディレクトリshare/decomposeParDictにあ
る領域分割設定ファイルの中から検討するケースを指定する．
なお，scotch分割の場合には，対応するファイルが
share/decomposeParDictが無い場合，
share/decomposeParDict/templateを元に領域分割数に
応じた設定ファイルが自動的に作成される．

fvSolutionArrayには
解法設定ファイルのディレクトリshare/fvSolutionにあ
る解法設定ファイルの中から検討するケースを指定する．

solveBatchArrayには
ソルバー解析バッチスクリプトのディレクトリ
share/batchScript/solveにある
ソルバー解析バッチスクリプトの中から検討するケースを指定する．
この配列は，OpenFOAMのバージョンやコンパイラ，MPIライブラリの種類，
およびMPIライブラリ等の実行時の設定などを変更した
ケーススタディを自動的に行うために用意されている．

なお，総検討ケースは，
decomposeParDictArray，fvSolutionArray，
solveBatchArrayの配列の積の組み合わせとなる．

### バッチジョブシステム用ベンチマークケース設定

バッチジョブシステムでは，例えば以下のように設定する．

Reedbush_U-mesh_3M-No1/all
```
BATCH_PRE=0            # 前処理のバッチジョブでの実行(0=しない)
BATCH_DECOMPOSEPAR=0   # 領域分割のバッチジョブでの実行(0=しない)
BATCH_SOLVE=1          # ソルバ解析のバッチジョブでの実行(1=する)

MAX_NUMBER_OF_QUEUE=50 # バッチジョブでの最大投入キュー数
NAME=OFBench           # バッチジョブの名前

NPROCS_PER_NODE=36     # ノードあたりのプロセッサ数

# 投入済のバッチキューの数を返す関数
NumberOfBatchQueue()
{
    rbstat -l | grep "^[0-9]" | wc -l
}

# バッチジョブを投入する関数
BatchSubmit()
{
    local BATCHFILE=$1
    local MPI=$2

    local NODE=`echo "($MPI + $NPROCS_PER_NODE - 1)/ $NPROCS_PER_NODE" | bc`
(略)	
    qsub \
	-W group_list=$GROUP \
	-q $QUEUE \
	-l walltime=$WALLTIME \
	-l select=$NODE:ncpus=$NPROCS_PER_NODE:mpiprocs=$NPROCS_PER_NODE:ompthreads=1 \
	$BATCHFILE
}
```

## バッチスクリプトの設定
### 前処理バッチスクリプト

前処理を行うバッチスクリプトをshare/batchScript/pre.shに置く．

BenchmarkTest_3M_NoBatch/share/batchScript/pre.sh
```
#!/bin/bash

application=pre.sh

(
env
blockMesh
) >& log.${application}.$1

touch ${application}.done
```

### 領域分割バッチスクリプト

領域分割を行うバッチスクリプトをshare/batchScript/decomposePar.shに置く．

BenchmarkTest_3M_NoBatch/share/batchScript/pre.sh
```
#!/bin/bash

application=decomposePar.sh

(
    env
    decomposePar -cellDist 
) >& log.${application}.$1

touch ${application}.done
```

### ソルバー解析バッチスクリプト
領域分割を行うバッチスクリプトをshare/batchScript/solve/に置く．
mpirunのオプションが必要であれば追加する．

NoBatch-mesh_3M/share/batchScript/solve/OpenFOAM
```
#!/bin/bash

# Source tutorial run functions
. $WM_PROJECT_DIR/bin/tools/RunFunctions

# Get application name
application=$(getApplication)

log=log.${application}.$2
(
env
mpirun -np $1 -machinefile hostfile \ # 必要に応じてmpirunのオプションを追加
$(getApplication) -parallel
) >& $log

grep "^End" $log >& /dev/null
[ $? -eq 0 ] && touch $log.done
```

## ベンチマークの実行・集計・プロット

### ベンチマークの実行

ベンチマークの実行は以下のようにする．

```bash
../bin/benchmark.sh ベンチマークケース設定ファイル名(all等) >& log &
```

### ベンチマーク結果の集計

ベンチマーク実行用のディレクトリ上で以下を実行する．

```bash
../bin/table.sh ベンチマークケース設定ファイル名(all等)
```

ベンチマーク結果を集計したファイルベンチマークケース設定ファイル名.csv
および，ソルバのログのアーカイブファイル
ファイルベンチマークケース設定ファイル名.tar.bz2
が作成される．
なお，アーカイブファイルに収録されるソルバのログは，
先頭がBuildから始まるヘッダーから，先頭がEndのまでの部分を取り出し，
かつ，プライバシーのため，ヘッダーにおける，HostとCaseの行，および
Slaveの情報を消している．

### ベンチマーク結果のプロット

ベンチマーク実行用のディレクトリ上で以下のPythonスクリプトを実行する．

```bash
../bin/plot.py csvファイル名(all.csv等)
```

ベンチマーク結果をプロットしたファイル*.pdfが作成される．
なお，NumPy,PyLab,matplotlibのライブラリが必要である．

## ベンチマーク結果の提供のお願い

ベンチマークテストを行なった場合には，以下のデータを提供をお願いする．

    README.md
    ベンチマークケース設定ファイル
    ベンチマーク結果を集計したファイル(*.csv)
    ソルバのログのアーカイブファイル(*.tar.bz2)
    ベンチマークケース共有設定ファイルのディレクトリ(share/*)  

### README.md

    # ハードウェア名称-mesh_格子数-NoX

    ## 測定者情報

    * 測定者: [本名で無くても構いません]
    * 測定日: [例: 2016年1月1日-2016年1月2日]

    ## ベンチマーク情報

    * 格子数: [例: 3M(240x130x96)]
    * MPI数[ノード数]: [例: 10(1)，20(2)]

    ## ハードウェア情報
    * ハードウェア名称: [例: NEC Express5800/HR120a-1]
    * CPUの種別: [例: Intel Xeon CPU E5-2680 v2]
    * CPUの周波数: [例: 2.80GHz]
    * コア数/CPU: [例: 10]
    * CPU数/ノード: [例: 2]
    * メモリ量/ノード: [例: 28GB]
    * メモリ種別: [例: SDRAM DDR3-1333 ECC]
    * メモリ帯域幅: [例: 85 GB/s]
    * インターフェース種別: [例: FDR-InfiniBand] 
    * インターフェース数/ノード: [例: 1基] 
    * インターフェース・スループット/基: [例: 56Gbps] 
    * その他特記事項:

    ## ソフトウェア情報
    * OpenFOAMのバージョン: [例: OpenFOAM-4.1]
    * ビルドに使用したコンパイラ: [例: Gcc-4.8.5]
    * コンパイラの最適化オプション: [例: -O3]
    * 使用したMPIライブラリ: [例: OpenMPI-1.8.4]
    * その他特記事項:

## References

1. Iwamoto, K., 2002. "Database of Fully Developed ChannelFlow",THTLAB Internal Report, No. ILR-0201.,THTLAB, Dept. of
Mech. Eng., The Univ. of Tokyo. <http://thtlab.jp/DNS/dns_database.html>
