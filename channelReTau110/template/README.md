channelReTau110/template
"Template Setting for Channel Flow (Re_tau=110)"

Creator: Masashi IMANO <masashi.imano@gmail.com>
Date: 10/May/2015
Supported OpenFOAM version: 2.3.0

1. 概要
================================================================================
channelReTau110/templateはオープンCAE学会V&V委員会OpenFOAMベンチマークテストWGで作成した
チャンネル流れ(Re_tau=110)[1]を対象としたベンチマークテスト問題のテンプレートである．

2. 設定
================================================================================
2.1 設定ファイル

ケースのパラメータは caseSettings で一括して設定する．

2.2 格子数の設定

blockMeshDict において X，Y, Z方向の格子数(NX,NY,NZ)を設定する．

--------------------------------------------------------------------------------
blockMeshDict
{
  N (240 130 96); // (NX NY NZ)
}
--------------------------------------------------------------------------------

2.3 時間刻み，解析時間の設定

controlDict において，時間刻みdt，解析時間Timeを設定する．

--------------------------------------------------------------------------------
controlDict
{
  deltaT          0.002; // dt [s]
  endTime         0.022; // Time [s] = 11*dt
}
--------------------------------------------------------------------------------

格子数を変えても主流方向の最大クーラン数が0.5弱になるように，時間刻みdtは0.480/NXとする．
解析時間Timeはdtの11倍とする．

2.4 領域分割数の指定

decomposeParDict にてMPI並列に対応する領域分割数をnumberOfSubdomains で指定する．
methodに領域分割手法(simple, scotch等)を指定する．
methodががsimpleの場合には，simpleCoeffsにて，X,Y,Z方向の領域分割数nx,ny,nzを指定する． 
methodがscotchの場合には，simpleCoeffsのnx,ny,nzの指定は無視されるが，
適当な数字を記述しておく必要がある．

--------------------------------------------------------------------------------
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
--------------------------------------------------------------------------------

2.5 圧力線型ソルバ

fvSolution.solvers.pにおけるsolver にて圧力線型ソルバの種類を指定する．
また，ソルバがGAMGの場合には，smootherにてスムーサの種類
(DIC,FDIC,DICGaussSeidel,GaussSeidel,nonBlockingGaussSeidel,symGaussSeidel)
を指定する．
ソルバがPCGの場合には，preconditionerにて前処理の種類(DIC,FDIC,diagonal)を指定する．

--------------------------------------------------------------------------------
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
--------------------------------------------------------------------------------

2.6 乱流モデル

turbulencePropertiesのsimulationTypeにて，乱流モデルの種別(laminar, LESModel)
を指定する．
simulationTypeがlaminarの場合には乱流モデルを使用しない．この場合，
LESPropertiesのLESModelはlaminar, deltaはcubeRootVolとしておく．
simulationTypeがLESModelの場合には，LESPropertiesのLESModelにて，
LESモデルの種別(Smagorinsky等)を指定する．また，deltaにはLESファイルタに用いるdeltaの種別
(vanDriest, cubeRootVol)を指定する．

--------------------------------------------------------------------------------
turbulenceProperties
{
  simulationType laminar;
}

LESProperties
{
  LESModel laminar;
  delta cubeRootVol;
}
--------------------------------------------------------------------------------

3. 実行
================================================================================
3.1 格子生成と領域分割

以下を実行する．

$ ./Allrun.pre

3.2 解析実行

以下を実行する．

$ ./Allrun.solve

3.3 ポスト処理(オプション)

以下を実行する．

$ ./Allrun.post

ソルバーのログの解析，領域分割された計算結果の再構築，時間平均鉛直プロファイルの作成が行われる．

3.4 プロット(オプション)

以下を実行する．

$ ./Allrun.plot

EPS形式の各種プロット図および，それらを統合したPDFファイルが作成される．
PDFファイルの作成には，ImageMagickのconvertコマンドが必要である．

3.5 初期化(オプション)

以下を実行する．

$ ./Allrun.clean

4. References
================================================================================
[1] Iwamoto, K., 2002.
    "Database of Fully Developed Channel Flow,"
    THTLAB Internal Report, No. ILR-0201.
    THTLAB, Dept. of Mech. Eng., The Univ. of Tokyo.
    http://thtlab.jp/DNS/dns_database.html
