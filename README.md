# ICML-2020 论文统计信息

## 声明
本工作基于Paper Digest对ICML-2020接收论文的整理([链接](https://www.paperdigest.org/2020/07/icml-2020-highlights/))，将ICML-2020的论文按照关键词、主题、作者信息进行分类整理，
方便大家更好的查阅自己偏好的研究方向和作者的论文。

## 对作者信息统计生成author_cloud

Top 10 authors:

|author|num_papers|University|
|:----|:----|:----|
|Masashi Sugiyama|11|University of Tokyo|
|Michael Jordan|8|UC Berkeley|
|Michal Valko|8|DeepMind & Inria & ENS|
|Dale Schuurmans|8|Google Brain & U of Alberta|
|Zhaoran Wang|7|Northwestern U|
|Gang Niu|7|RIKEN AIP|
|Mihaela van der Schaar|7|University of Cambridge|
|Percy Liang| 7|Stanford|
|Tommi Jaakkola|7|MIT|
|Steven Wu|6|U of Minnesota|

![avatar](/pic/author.png)
## 对关键词信息统计生成word_cloud
problem: 
- 很多专业名词(e.g., Adversarial Network, neural network)被分开成为两个词语
，不符合实际情况；<br>
- 大小写，单复数应该要不敏感;<br>
![avatar](/pic/keyword.png)

## 对论文按照主题进行统计分类

problem：
- 自动找出一堆标题、摘要中出现次数很多的主题：主题发现；（手工定义容易遗漏，需要领域知识）
- 自动将类似主题聚类合并；


To be finished...


|topic|num_papers|
|:----|:----|
|graph|58|
|GAN|17|
|private|14|
|unsupervised|11|
|uncertainty|11|
|multi-task|8|
|GANs|7|
|online learning|7|
|semi-supervised|7|
|Differential Privacy|6|
|few-shot|6|
|transfer learning|5|
|convolutional neural networks|4|
|Q-learning|4|
|time series|4|
|CNN|4|
|generative adversarial|4|
|interpretability|2|
|Knowledge Distillation|1|
|real time|1|
|GNN|1|
|real-time|1|

![avatar](/pic/topic.png)