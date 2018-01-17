# TSUBAME_3.0-RapidCFD-CUDA_8.0-openmpi_2.1.1
## 測定者情報
* 山岸 孝輝: (Takateru Yamagishi)

## ハードウェア情報
* ハードウェア名称: TSUBAME 3.0: (SGI ICE XA)
* GPUの種別: NVIDIA Tesla P100 for NVLink-Optimized Servers
* GPU数/ノード: 4
* メモリ量/ノード: 64GB
* メモリ種別: HBM2
* メモリ帯域幅: 732GB/s
* インターフェース種別: Intel Omni-Path
* インターフェース数/ノード: 4基 
* インターフェース・スループット/基: 400Gb/s 
* その他特記事項:

## ソフトウェア情報
* OpenFOAMのバージョン: RapidCFD (rev: 9fc614f4e816c51e5a718a1349cea9d72864042e), RapicdCFD最適化版 [1, 2]
* ビルドに使用したコンパイラ: nvcc (cuda 8.0)
* コンパイラの最適化オプション: -O3
* 使用したMPIライブラリ: openmpi-2.1.1
* その他特記事項:

## References
1. GPU・メニーコアにおけるOpenFOAMの高度化支援紹介, 山岸孝輝、井上義昭、青柳哲雄、浅見曉, 第1回CAEワークショップ, 秋葉原 UDX Gallery NEXT, 2017年12月6日, http://www.hpci-office.jp/invite2/documents2/ws_cae_171206_yamagishi.pdf
2. OpenFOAMのメニーコア・GPUへの対応に向けた取り組みの紹介, 山岸孝輝、井上義昭、青柳哲雄、浅見暁, オープンCAEシンポジウム2017, 名古屋大学, 2017年12月9日

## 謝辞
* 本計測結果は，HPCIシステム利用研究課題「流体・粒子の大規模連成解析を用いた竜巻中飛散物による建物被害の検討（課題番号：hp170055），課題代表者：菊池浩利（清水建設（株）技術研究所）」の高度化支援に基づくものです。
* RapidCFDのビルド及びベンチマークについては青子守歌氏の投稿記事を参考にさせて頂きました。( http://qiita.com/aokomoriuta/items/8a49f64af2e5ab0042d2 )
