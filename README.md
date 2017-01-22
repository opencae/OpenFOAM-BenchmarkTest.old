# OpenFOAM-BenchmarkTest

## English version (Translated from Japanese version by Gooogle translate)

### Overview

OpenFOAM - BenchmarkTest is a benchmark test conducted by The Open CAE Society of Japan V&V Committee OpenFOAM Benchmark Test WG.

### background

In recent years clouds for Amazon's EC 2 and HP's Azure such as Azure can be easily used and there are cases where it is desired to execute HPC analysis such as large scale CFD calculation of OpenFOAM spotally as difficult with hand computer resources etc. It is said to be suitable. In addition, as with Oakleaf-FX of the University of Tokyo and TSUBAME of Tokyo Institute of Technology, universities and research institutes are increasingly using supercomputers to open up the door to education / public institutions such as corporate use. Normally, however, there is a task review for the use of supercomputers in education / public institutions like this, and the unit of use is usually at least monthly, and unlike the cloud, it is not spot usage or billing. On the other hand, in the Foundation for Computational Science Promotion FOCUS, in the case of a corporation, it can be used without examination of tasks, and spot usage and billing are also possible. As mentioned above, the number of remote computer resources that can perform HPC calculation has increased recently, but in each system there are differences in CPU performance as well as interconnect etc., the usage fee naturally differs. Based on the above background, we made a common OpenFOAM benchmark to compare the computing performance and cost of various systems so that it can be a reference for system selection to use for OpenFOAM users.

## Japanese version (Original)

### 概要

OpenFOAM-BenchmarkTest は オープンCAE学会 V&V委員会 OpenFOAMベンチマークテストWG で行っているベンチマークテストである．

### 背景

近年AmazonのEC2やMicrosoftのAzure等のHPC向けのクラウドが気軽に利用できるようになっており，手持ちの計算機リソースでは難しいOpenFOAMの大規模CFD計算のようなHPC解析をスポット的に実行したい場合などに適すると言われている．
また，東京大学のOakleaf-FXや東京工業大学のTSUBAMEのように，大学や研究機関でも企業利用など教育・公共機関以外に門戸を開放するのスパコン利用サービスが増えてきている．
ただし，通常このような教育・公共機関でのスパコンの利用には課題審査があり，利用単位は通常最低でも月単位となり，クラウドと異なりスポット的な利用や課金ではない．
一方，計算科学振興財団FOCUSでは，法人の場合課題の審査無く利用可能であり，スポット的な利用や課金も可能である．
以上のように，昨今ではHPC計算を行えるリモートの計算機リソースが増えてきたが，各システムでは，CPU性能はもちろん，インターコネクト等にも違いがあり，利用料金も当然異なる．
以上の背景から，OpenFOAMのユーザに対して使用するシステム選択の参考となるよう，共通OpenFOAMベンチマークを作成し各種システムの計算性能と費用を比較した．
