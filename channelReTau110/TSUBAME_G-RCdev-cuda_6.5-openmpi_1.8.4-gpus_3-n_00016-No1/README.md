# TSUBAME_G-RCdev-cuda_6.5-openmpi_1.8.4-gpus_3-n_00016-No1

## 測定者情報

* 測定者: 今野 雅 ( Masashi Imano )
* 測定日: 2015年12月28日〜29日

## ベンチマーク情報

* 格子数(格子数倍率)：5992888(16)
* MPI数(ノード数)：3(1),6(2),12(4),24(8),36(12),48(16),60(20),72(24),144(48),288(96)
* その他特記事項:
  * 使用キュー: Gキュー (Sキューの半額)
  * blockMesh や decompoPar は rapidCFD ではなく，通常の OpenFOAM で実行する．
  * 288MPI数のデータはプロットしないよう table.csv から取り除いた．
オリジナルの table.csv  は orig-table.csv である．

## ハードウェア情報

* ハードウェア名称: TSUBAME 2.5 Thinノード(HP Proliant SL390s G7)
* GPUの種別: NVIDIA Tesla K20X
* GPU数/ノード: 3
* メモリ量/ノード: 54GB
* インターフェース種別: Infiniband-QDR
* インターフェース数/ノード: 2基 
* インターフェース・スループット/基: 40Gbps
* その他特記事項:
  
## ソフトウェア情報

* OpenFOAMのバージョン: RapidCFD (rev: d3733257dee5fb9999b918f5c26a1493cebb603c)
* ビルドに使用したコンパイラ: nvcc (cuda-6.5)
* コンパイラの最適化オプション: -O3
* 使用したMPIライブラリ: openmpi-1.8.4
* その他特記事項:
  * mpirunオプション: --bind-to core -mca btl openib,sm,self

## 謝辞

東京工業大学学術国際情報センター共同利用推進室の
佐々木淳様から，OpenFOAMとRapidCFDの評価用として，
TSUBAME 2.5の計算機リソースを提供して頂きました．

青子守歌様には，RapidCFDのビルド及びベンチマークについてご協力頂きました．
( http://qiita.com/aokomoriuta/items/8a49f64af2e5ab0042d2 )

ここに深く感謝致します．
