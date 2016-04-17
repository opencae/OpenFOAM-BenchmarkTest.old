#channelReTau110-Oakleaf-FX-No1

## 測定者情報

* 測定者: 今野 雅 ( Masashi Imano )
* 測定日: 2015年12月28日

## ベンチマーク情報

* 格子数(格子数倍率)：5992888(16)
* MPI数(ノード数)：16(1),32(2),64(4),128(8),192(12),384(24),768(48)

## ハードウェア情報

* ハードウェア名称: Oakleaf-FX
* CPUの種別: Fujitsu SPARC64(TM) IXfx
* CPUの周波数: 1.848GHz
* コア数/CPU: 16
* CPU数/ノード: 1
* メモリ量/ノード: 32GB
* インターフェース種別: Tofu(6次元メッシュ / トーラス)
* インターフェース数/ノード: 10ポート(4方向同時通信可能)
* インターフェース・スループット/基: 5 GByte/sec × 双方向
* その他特記事項:
    * メモリ: SDRAM DDR3-1333 ECC
    * メモリ帯域幅: 85 GB/s (SDRAM DDR3-1333 ECC)
    * インターフェース: RDMA通信

## ソフトウェア情報

* OpenFOAMのバージョン: 2.3.0
* ビルドに使用したコンパイラ: FCC (Technical Computing Suite GM-1.2.1-08)
* コンパイラの最適化オプション: -O3 -Xg -D__INTEL_COMPILER
* 使用したMPIライブラリ: FJMPI
* その他特記事項:
