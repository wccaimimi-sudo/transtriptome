## 🧬 RNA-seq 分析流程（HISAT2 + StringTie + featureCounts）

 RNA-seq 分析流程
### 📦 流程概览


<img width="1201" height="225" alt="image" src="https://github.com/user-attachments/assets/89296ae4-5a60-484c-8ee4-6726b74ab92a" />



### 🔧 模块详解

模块

脚本

输入

核心工具

输出

说明

**1. 质量控制**

`fp.sh`

`0.rawdata/*.fq.gz`

`fastp`

`1.fastp/results/1_qc/*.clean.fq.gz`

自动去接头、质控、过滤低质量 reads

**2. 基因组索引**

`his.sh`

`reference/*.fasta`

`hisat2-build`

`results/0_reference/hisat2_index/*.ht21`

一次性构建，后续比对复用

**3. 序列比对**

`map.sh`

Clean FASTQ + 索引

`hisat2`,  `samtools`

`3.map/results/*.sorted.bam`

并行比对 + 实时排序

**4.1 转录本组装**

`stringtie.sh`

`*.sorted.bam`

`stringtie`,  `parallel`

`4.stringtie/4.1results/*.gtf`

每样本独立组装转录本结构

**4.2 注释合并**

`merge.sh`

所有 sample.gtf

`stringtie --merge`

`4.stringtie/4.2results/merged_transcripts.gtf`

生成统一非冗余基因/转录本注释

**4.3 表达定量**

`abd.sh`

BAM + merged.gtf

`featureCounts`,  `Python`

`5.counts/{raw_counts.tsv, tpm_counts.tsv}`

**基因水平 counts → TPM**

----------


-   **双输出**：
    -   `raw_counts.tsv`  
    -   `tpm_counts.tsv`  
