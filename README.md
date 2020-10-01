# rNA

[![GitHub issues](https://img.shields.io/github/issues/skchronicles/rNA)](https://github.com/skchronicles/rNA/issues)  [![GitHub license](https://img.shields.io/github/license/skchronicles/rNA)](https://github.com/skchronicles/rNA/blob/master/LICENSE)

### Table of Contents
1. [Introduction](#1-Introduction)  
2. [Overivew](#2-Overview)  
    2.1 [Primary Analysis](#21-Primary-Analysis)  
    2.2 [Downstream Analysis](#22-Downstream-Analysis)   
3. [Run rRNA](#3-Run-rNA)  
    3.1 [Usage](#31-Usage)  
    3.2 [Required Arguments](#32-Required-Arguments)  
    3.3 [OPTIONS](#33-OPTIONS)  
    3.4 [Example](#34-Example)  
4. [Filtering Critea](#4-Filtering-Critea)
5. [References](#5-References)


### 1. Introduction

report Not Applicable, as known as `rNA`, is an interactive report to allow users to identify problematic samples prior to downstream analysis. rNA has been designed to work with the output from our RNA-seq pipeline.

Before drawing biological conclusions, it is important to assess the quality control of each sample to ensure that there are no signs of sequencing error or systematic biases in your data. Modern high-throughput sequencers generate millions of reads per run, and in the real world, problems can arise. rNA allows a user to interactively filter samples based on different quality-control metrics. This is especially useful when working with large cohorts with hundreds of samples.

### 2. Overview 

rNA has been designed to work with the output from our RNA-seq pipeline. Here is an overview of the pipeline's major data processing and quality control steps.

##### 2.1 Primary Analysis

The quality of each sample is independently assessed using FastQC<sup>2</sup>, Preseq<sup>1</sup>, Picard tools<sup>10</sup>, RSeQC<sup>9</sup>, SAMtools<sup>13</sup>, and QualiMap<sup>16</sup> . FastQ Screen<sup>17</sup> and Kraken<sup>14</sup> + Krona<sup>15</sup> are used to screen for various sources of contamination. Adapter sequences are removed using Cutadapt<sup>3</sup> prior to mapping to hg38 reference genome. STAR<sup>4</sup> is run in _two-pass_ mode where splice-junctions are collected and aggregated across all samples and provided to the second-pass of STAR. Gene expression levels are quantified using RSEM. The expected counts from RSEM<sup>5</sup> are merged across samples to create a counts matrix for downstream analysis. RSeQC<sup>19</sup> `tin.py` is used to calculate transcript integrity numbers (TIN counts matrix) for all canonical protein-coding transcripts. 

##### 2.2 Downstream Analysis 

rNA takes the raw counts matrix, TIN counts matrix, and the QC metadata table generated in the pipeline described above as input. These are a few of the **required** command-line arguments to `rNA.R`. rNA performs the following steps listed below. The expected counts from RSEM are filtered to remove lowly expressed genes with edgeR's<sup>18</sup> `filterByExpr()` function using the following critea: genes must have 10 reads in >= 70% samples. The normalisation factors calculated using edgeR's TMM method  are used as scaling factors for library size. Using the `voom()` function in limma<sup>8</sup>, the counts are converted log2-counts-per-million (logCPM) and quantile normalized.

_voom_<sup>7</sup> is an acronym for mean-variance modelling at the observational level. The key concern is to estimate the mean-variance relationship in the data, then use this to compute appropriate weights for each observation. Count data almost show non-trivial mean-variance relationships. Raw counts show increasing variance with increasing count size, while log-counts typically show a decreasing mean-variance trend. This function estimates the mean-variance trend for log-counts, then assigns a weight to each observation based on its predicted variance. The weights are then used in the linear modelling process to adjust for heteroscedasticity.

### 3. Run rNA

##### 3.1 Usage  

```bash
$ ./rNA.R [OPTIONS] -m RMARKDOWN -r RAW_COUNTS -t TIN_COUNTS -q QC_TABLE -o OUTPUT_DIR
```
##### 3.2 Required Arguments  

| Flag                  | Type       |   Description                   |
| --------------------- | ---------- | ------------------------------- |
| -m, --rmarkdown       | Script     | rNA Rmarkdown file              |
| -r, --raw_counts      | File       | Input Raw counts matrix         |
| -t, --tin_count       | File       | Input TIN counts matrix         |
| -q, --qc_table        | File       | Input QC Metadata Table         |
| -o, --output_dir      | Path       | Path to Output Directory        |

##### 3.3 OPTIONS  
| Flag                  |   Description                       |
| --------------------- | ----------------------------------  |
| -h, --help            | Displays help and usage information |
| -f, --output_filename | Output HTML filename, Default: rNA.html|

##### 3.4 Example
```bash
Rscript rNA.R -m src/rNA.Rmd \
              -r data/TCGA-GBM_Raw_RSEM_Genes.txt \
              -t data/TCGA-GBM_TINs.txt \
              -q data/multiqc_matrix.txt -o "$PWD"
```

### 4. Filtering Critea

**General Recommendations** 

Here is a set of generalized guidelines for filtering based on different QC metrics:

| Metric                      |             Guideline           |
|-----------------------------|:-------------------------------:|
| *medTIN*                    |             > 65                |
| *Trimmed Reads*             |           > 10000000            |
| *% Aligned to Reference*    |             > 65%               |
| *% Duplicates*              |             < 65 %              |
| *% rRNA*                    |             < 10%               |
| *% Coding*                  |          Coding > 35%           |


> **Please note:** Some of these metrics will vary genome-to-genome depending on the quality of the assembly and annotation but that has been taken into consideration for our set of supported reference genomes.

### 5. References

<sup>**1.**	Daley, T. and A.D. Smith, Predicting the molecular complexity of sequencing libraries. Nat Methods, 2013. 10(4): p. 325-7.</sup>  
<sup>**2.** Andrews, S. (2010). FastQC: a quality control tool for high throughput sequence data.</sup>  
<sup>**3.**	Martin, M. (2011). "Cutadapt removes adapter sequences from high-throughput sequencing reads." EMBnet 17(1): 10-12.</sup>  
<sup>**4.**	Dobin, A., et al., STAR: ultrafast universal RNA-seq aligner. Bioinformatics, 2013. 29(1): p. 15-21.</sup>  
<sup>**5.**	Li, B. and C.N. Dewey, RSEM: accurate transcript quantification from RNA-Seq data with or without a reference genome. BMC Bioinformatics, 2011. 12: p. 323.</sup>  
<sup>**6.**	Harrow, J., et al., GENCODE: the reference human genome annotation for The ENCODE Project. Genome Res, 2012. 22(9): p. 1760-74.</sup>  
<sup>**7.**	Law, C.W., et al., voom: Precision weights unlock linear model analysis tools for RNA-seq read counts. Genome Biol, 2014. 15(2): p. R29.</sup>  
<sup>**8.**	Smyth, G.K., Linear models and empirical bayes methods for assessing differential expression in microarray experiments. Stat Appl Genet Mol Biol, 2004. 3: p. Article3.</sup>  
<sup>**9.**    Wang, L., et al. (2012). "RSeQC: quality control of RNA-seq experiments." Bioinformatics 28(16): 2184-2185.</sup>  
<sup>**10.**    The Picard toolkit. https://broadinstitute.github.io/picard/.</sup>  
<sup>**11.**    Ewels, P., et al. (2016). "MultiQC: summarize analysis results for multiple tools and samples in a single report." Bioinformatics 32(19): 3047-3048.</sup>  
<sup>**12.**    R Core Team (2018). R: A Language and Environment for Statistical Computing. Vienna, Austria, R Foundation for Statistical Computing.</sup>  
<sup>**13.**    Li, H., et al. (2009). "The Sequence Alignment/Map format and SAMtools." Bioinformatics 25(16): 2078-2079.</sup>  
<sup>**14.**    Wood, D. E. and S. L. Salzberg (2014). "Kraken: ultrafast metagenomic sequence classification using exact alignments." Genome Biol 15(3): R46.</sup>  
<sup>**15.**    Ondov, B. D., et al. (2011). "Interactive metagenomic visualization in a Web browser." BMC Bioinformatics 12(1): 385.</sup>  
<sup>**16.**    Okonechnikov, K., et al. (2015). "Qualimap 2: advanced multi-sample quality control for high-throughput sequencing data." Bioinformatics 32(2): 292-294.</sup>  
<sup>**17.**    Wingett, S. and S. Andrews (2018). "FastQ Screen: A tool for multi-genome mapping and quality control." F1000Research 7(2): 1338.</sup>  
<sup>**18.**    Robinson, M. D., et al. (2009). "edgeR: a Bioconductor package for differential expression analysis of digital gene expression data." Bioinformatics 26(1): 139-140.</sup>  

<hr>
<p align="center">
	<a href="#rNA">Back to Top</a>
</p>
