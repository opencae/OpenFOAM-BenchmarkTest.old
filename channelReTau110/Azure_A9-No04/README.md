# Azure_A9-No04

## 測定者情報

* 測定者: 佐々木 邦暢 ([@ksasakims](https://twitter.com/ksasakims) )
* 測定日: 2015年11月25日 - 2015年11月26日

## ベンチマーク情報

* 格子数(格子数倍率)：2995200(8)
* MPI数(ノード数)：16(1), 32(2), 48(3), 64(4), 80(5), 96(6), 112(7), 128(8)

## ハードウェア情報

* ハードウェア名称: [Azure A9 インスタンス](https://azure.microsoft.com/ja-jp/documentation/articles/virtual-machines-a8-a9-a10-a11-specs/)
* CPUの種別: Intel Xeon E5-2670
* CPUの周波数: 2.66GHz
* コア数/CPU: 8
* CPU数/ノード: 2
* メモリ量/ノード: 112GB
* インターフェース種別: Infiniband-QDR
* インターフェース数/ノード: 1基 
* インターフェース・スループット/基: 40Gbps

## ソフトウェア情報

* OS: SUSE Linux Enterprise Server 12 (x86_64)
* OpenFOAMのバージョン: 2.3.0
* ビルドに使用したコンパイラ: gcc version 4.8.3 20140627 [gcc-4_8-branch revision 212064] (SUSE Linux)
* コンパイラの最適化オプション: -O3
* 使用したMPIライブラリ: Intel MPI 5.1.1.109
