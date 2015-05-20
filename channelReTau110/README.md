# OpenFOAM-BenchmarkTest-channelReTau110 "OpenFOAM Benchmark Test for Channel Flow (Re_tau=110)"

## 概要

OpenFOAM-BenchmarkTest-channelReTau110は
オープンCAE学会V&V委員会OpenFOAMベンチマークテストWGで作成した，
チャネル流れ(Re_tau=110)channelReTau110[1]を対象とした
ベンチマークテストである．

* README       このファイル
* bin/         スクリプト
* src/         ソース
* template/    channelReTau110のケースディレクトリ
* FOCUS/       FOCUSでの設定例
* Oakleaf-FX/  Oakleaf-FXでの設定例
* NoBatch/     非バッチジョブシステムでの設定例

## 設定

### ベンチマークケースのパラメータや関数の設定

ベンチマークケースのパラメータや関数は benchmark.conf で設定する．

### nArray(格子数倍率nのベンチマークケース)

格子数倍率nは，格子数374400(nx=120,ny=65,nz=48)をベースにとした格子の倍数である．
ベンチマークケースnArrayの要素にはnを0埋めの5桁の整数値，かつ文字列形式で記述する．

    nArray=( "00001" "00002" "00004"  "00008" )

標準条件: n=00008(格子数2995200=約3M)

### mpiArray(MPI並列数mpiのベンチマークケース)

MPI並列数mpiのベンチマークケースmpiArrayの要素には，
mpiの値を0埋めの5桁の整数かつ文字列形式で記述する．

    mpiArray=( "00008" "00010" "00012" "00016" "00020" "00024" )

標準条件: 無し．
ただし，並列化効率をみるために複数のMPI並列数で計算することを推奨．

### simulationTypesArray(乱流モデルのベンチマークケース)

乱流モデルのベンチマークケースsimulationTypesArrayの要素には，
以下の形式の文字列を羅列する．
"(simulationTypesの値)-LESModel_(LESModelの値)-delta_(deltaの値)"

    simulationTypesArray=(\
      "laminar-LESModel_laminar-delta_cubeRootVol" \
      "LESModel-LESModel_Smagorinsky-delta_vanDriest" \
    )

標準条件: laminar-LESModel_laminar-delta_cubeRootVol
ただし，LESModel-LESModel_Smagorinsky-delta_vanDriest のケースも計算することを強く推奨．

### solversArray(圧力に対する線型ソルバのベンチマークケース)

圧力に対する線型ソルバのベンチマークケースsolversArrayの要素には，
以下の形式の文字列を羅列する．
"PCG-preconditioner_(preconditionerの値)"
"GAMG-smoother_(smootherの値)"

    solversArray=(\
      "PCG-preconditioner_FDIC" \
      "PCG-preconditioner_DIC" \
      "PCG-preconditioner_diagonal" \
      "GAMG-smoother_DIC" \
      "GAMG-smoother_FDIC" \
      "GAMG-smoother_DICGaussSeidel" \
      "GAMG-smoother_GaussSeidel" \
      "GAMG-smoother_nonBlockingGaussSeidel" \
      "GAMG-smoother_symGaussSeidel" \
    )

標準条件: PCG-preconditioner_FDIC

### MAX_NUMBER_OF_LOOP(ベンチマークテストの繰り返し数)

ベンチマークテストの繰り返し数を以下のように整数値で指定する．

    MAX_NUMBER_OF_LOOP=1

標準条件: 1
ただし，計算機負荷にバラつきが大きい場合には，3以上繰り返す．

### MAX_NUMBER_OF_QUEUE(バッチキューの最大値)

ベンチマークテストの実行スクリプトで投入可能なバッチキューの最大値を以下のように指定する．
バッチジョブシステムを使用しない場合には無視される．

    MAX_NUMBER_OF_QUEUE=1

### NumberOfBatchQueue(バッチキュー数を返す関数)

バッチキュー数を返す関数を定義する．

    NumberOfBatchQueue()
    {
    	nq=`squeue | wc -l`
    	expr $nq - 1
    }

バッチジョブシステムを使用しない場合には以下のように定義する．

    NumberOfBatchQueue()
    {
    	# No operation
    	rtn=""
    }

### BatchSubmit(バッチジョブを投入する関数)

バッチジョブを投入する関数を定義する．

    BatchSubmit()
    {
    	local BATCHFILE=$1
    	local MPI=$2
    
    	sbatch -n $MPI $BATCHFILE
    }

バッチジョブシステムを使用しない場合には以下のように定義する．

    BatchSubmit()
    {
    
    	# No operation
    	rtn=""
    }

## バッチジョブスクリプトの設定

バッチジョブシステムを使用する場合には，batchScriptのディレクトリの中に以下の
バッチジョブスクリプトを作成する．

* batchScript/
*   blockMesh.sh     blockMesh実行バッチジョブスクリプト
*   decomposePar.sh  decomposePar実行バッチジョブスクリプト
*   solve.sh         ソルバ実行バッチジョブスクリプト

batchScriptのディレクトリが無い場合には，バッチジョブシステムを使用し
ないで，blockMesh，decomposeParやソルバが実行される．

## ベンチマークケースの実行
### ベンチマークケースの設定

channelReTau110のディレクトリの下に，ベンチマーク実行用のディレクトリ
を作成し，環境に合わせて適切にbenchmark.confを作成する．
また，バッチジョブシステムを使用する場合には，batchScriptのディレクト
リを作成し，適切にバッチジョブスクリプトを作成する．

### ベンチマークケースの実行

ベンチマーク実行用のディレクトリ上で以下を実行する．

    $ nohup ../bin/benchmark.sh >&  log.benchmark.sh &

### ベンチマーク結果の集計

ベンチマーク実行用のディレクトリ上で以下を実行する．

    $ ../bin/table.sh

ベンチマーク結果を集計したファイルtable.csvが作成される．

## ベンチマーク結果のプロット

ベンチマーク実行用のディレクトリ上で以下のPythonスクリプトを実行する．

    $ ../bin/plot.py

ベンチマーク結果をプロットしたファイル*.pdfが作成される．

なお，NumPy,PyLab,matplotlibのライブラリが必要である．

## ベンチマーク結果の提供のお願い
ベンチマークテストを行なった場合には，以下のデータを提供をお願いする．

### ファイル
* ベンチマーク実行用のディレクトリ/
*   benchmark.conf     ベンチマークケースのパラメータや関数の設定
*   table.csv          ベンチマーク結果を集計したファイル
*   batchScript/*.sh   バッチジョブスクリプト(バッチジョブシステムの場合)
*   n_*/mpi_*/simulationType_*/log.*[0-9] 各ベンチマークケースでのソルバーのログ
*   n_*/mpi_*/simulationType_*/log.*[0-9].*.txt 各ベンチマークケースでのプロファイラ結果(もしあれば)

また，以下の情報の提供もお願いする．

測定者: (本名で無くても構いません)

ハードウェア情報
    ハードウェア名称: (例: NEC Express5800/HR120a-1)
    CPUの種別: (例: Intel Xeon CPU E5-2680 v2)
    CPUの周波数: (例: 2.80GHz)
    コア数/CPU: (例: 10)
    CPU数/ノード: (例: 2)
    メモリ量/ノード: (例: 28GB)
    インターフェース種別: (例: FDR-InfiniBand) 
    インターフェース数/ノード: (例: 1基) 
    インターフェース・スループット/基: (例: 56Gbps) 
    その他特記事項:

ソフトウェア情報
    OpenFOAMのバージョン: (例: ###)
    ビルドに使用したコンパイラ: (例: Gcc-###)
    コンパイラの最適化オプション: (例: -O3)
    使用したMPIライブラリ: (例: openmpi-###)
    その他特記事項:

## channelReTau110のケースディレクトリの設定
### 設定ファイル

ケースのパラメータは caseSettings で一括して設定する．

### 格子数の設定

blockMeshDict において X，Y, Z方向の格子数(NX,NY,NZ)を設定する．

    blockMeshDict
    {
      N (240 130 96); // (NX NY NZ)
    }

### 時間刻み，解析時間の設定

controlDict において，時間刻みdt，解析時間Timeを設定する．

    controlDict
    {
      deltaT          0.002; // dt [s]
      endTime         0.022; // Time [s] = 11*dt
    }

格子数を変えても主流方向の最大クーラン数が0.5弱になるように，時間刻みdtは0.480/NXとする．
解析時間Timeはdtの11倍とする．

### 領域分割数の指定

decomposeParDict にてMPI並列に対応する領域分割数をnumberOfSubdomains で指定する．
methodに領域分割手法(simple, scotch等)を指定する．
methodががsimpleの場合には，simpleCoeffsにて，X,Y,Z方向の領域分割数nx,ny,nzを指定する． 
methodがscotchの場合には，simpleCoeffsのnx,ny,nzの指定は無視されるが，
適当な数字を記述しておく必要がある．

    decomposeParDict
    {
      numberOfSubdomains  16;
    
      method scotch;
    
      simpleCoeffs
      {
          nx 4;
          ny 2;
          nz 2;
      }
    }
    
### 圧力線型ソルバ

fvSolution.solvers.pにおけるsolver にて圧力線型ソルバの種類を指定する．
また，ソルバがGAMGの場合には，smootherにてスムーサの種類
(DIC,FDIC,DICGaussSeidel,GaussSeidel,nonBlockingGaussSeidel,symGaussSeidel)
を指定する．
ソルバがPCGの場合には，preconditionerにて前処理の種類(DIC,FDIC,diagonal)を指定する．

    fvSolution
    {
      solvers
      {
          p
          {
              solver           PCG;
              smoother         FDIC;
              preconditioner   FDIC;
          }
      }
    }

### 乱流モデル

turbulencePropertiesのsimulationTypeにて，乱流モデルの種別(laminar, LESModel)
を指定する．
simulationTypeがlaminarの場合には乱流モデルを使用しない．この場合，
LESPropertiesのLESModelはlaminar, deltaはcubeRootVolとしておく．
simulationTypeがLESModelの場合には，LESPropertiesのLESModelにて，
LESモデルの種別(Smagorinsky等)を指定する．また，deltaにはLESファイルタに用いるdeltaの種別
(vanDriest, cubeRootVol)を指定する．

    turbulenceProperties
    {
      simulationType laminar;
    }
    
    LESProperties
    {
      LESModel laminar;
      delta cubeRootVol;
    }

## ケース単体での実行

### 格子生成と領域分割

以下を実行する．

    $ ./Allrun.pre

### 解析実行

以下を実行する．

    $ ./Allrun.solve

### ポスト処理

以下を実行する．

    $ ./Allrun.post

ソルバーのログの解析，領域分割された計算結果の再構築，時間平均鉛直プロファイルの作成が行われる．

### プロット

以下を実行する．

    $ ./Allrun.plot

EPS形式の各種プロット図および，それらを統合したPDFファイルが作成される．
PDFファイルの作成には，ImageMagickのconvertコマンドが必要である．

### 初期化

以下を実行する．

    $ ./Allrun.clean

## References
1. Iwamoto, K., 2002. "Database of Fully Developed ChannelFlow",THTLAB Internal Report, No. ILR-0201.,THTLAB, Dept. of
Mech. Eng., The Univ. of Tokyo. <http://thtlab.jp/DNS/dns_database.html>
