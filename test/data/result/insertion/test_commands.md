# General Test Cases

## Test Case 1 - Insertion smaller than 50 bp

Test command containing an insertion smaller than 50 bp.

-   **PacBio data:** Insertions are not displayed in the long-read plot.
-   **Illumina data:** Smaller insertions are also displayed in the
    paired-end read plot.

### PacBio commands

**chr1: 4520723 - SVLEN=48**

``` bash
samplot plot -b HG002_PacBio_Insertion.bam -s 4520400 -e 4521000 -c chr1 -o ./result/insertion/TC001_LR_INS_chr1_4520723.png -t INS
```

**chr2: 235536158 - SVLEN=48**

``` bash
samplot plot -b HG002_PacBio_Insertion.bam -s 235536000 -e 235536350 -c chr2 -o ./result/insertion/TC001_LR_INS_chr2_235536158.png -t INS
```

**chr7: 51899408 - SVLEN=48**

``` bash
samplot plot -b HG002_PacBio_Insertion.bam -s 51899200 -e 51899600 -c chr7 -o ./result/insertion/TC001_LR_INS_chr7_51899408.png -t INS
```

### Illumina commands

**chr1: 4520723 - SVLEN=48**

``` bash
samplot plot -b HG002_Illumina_Insertion.bam -s 4520400 -e 4521000 -c chr1 -o ./result/insertion/TC001_PER_INS_chr1_4520723.png -t INS
```

**chr2: 235536158 - SVLEN=48**

``` bash
samplot plot -b HG002_Illumina_Insertion.bam -s 235536000 -e 235536350 -c chr2 -o ./result/insertion/TC001_PER_INS_chr2_235536158.png -t INS
```

**chr7: 51899408 - SVLEN=48**

``` bash
samplot plot -b HG002_Illumina_Insertion.bam -s 51899200 -e 51899600 -c chr7 -o ./result/insertion/TC001_PER_INS_chr7_51899408.png -t INS
```

**Additional test command for chr7:**

A cyan read was also visible with this test command. Interestingly, the
insertion is located between two magenta bars.

``` bash
samplot plot -b HG002_Illumina_Insertion.bam -s 51899200 -e 51902200 -c chr7 -o ./result/insertion/TC001_PER_INS_chr7_51899408.png -t INS
```

------------------------------------------------------------------------

## Test Case 2 - Insertion larger than 50 bp

Test command containing an insertion larger than 50 bp.

**Expected result:** Both data types should display the same insertion.

### PacBio commands

**chr10: 27296289 - SVLEN=450**

``` bash
samplot plot -b HG002_PacBio_Insertion.bam -s 27296000 -e 27296840 -c chr10 -o ./result/insertion/TC002_LR_INS_chr10_27296289.png -t INS
```

**chr10: 27312248 - SVLEN=1294**

``` bash
samplot plot -b HG002_PacBio_Insertion.bam -s 27312100 -e 27313600 -c chr10 -o ./result/insertion/TC002_LR_INS_chr10_27312248.png -t INS
```

**chr13: 65440375 - SVLEN=335**

``` bash
samplot plot -b HG002_PacBio_Insertion.bam -s 65440275 -e 65440900 -c chr13 -o ./result/insertion/TC002_LR_INS_chr13_65440375.png -t INS
```

**chr13: 65449105 - SVLEN=494**

``` bash
samplot plot -b HG002_PacBio_Insertion.bam -s 65448900 -e 65449800 -c chr13 -o ./result/insertion/TC002_LR_INS_chr13_65449105.png -t INS
```

**chr13: 66146710 - SVLEN=1230**

``` bash
samplot plot -b HG002_PacBio_Insertion.bam -s 66146600 -e 66148100 -c chr13 -o ./result/insertion/TC002_LR_INS_chr13_66146710.png -t INS
```

**chr19: 23753136 - SVLEN=464**

``` bash
samplot plot -b HG002_PacBio_Insertion.bam -s 23753100 -e 23753700 -c chr19 -o ./result/insertion/TC002_LR_INS_chr19_23753136.png -t INS
```

### Illumina commands

**chr10: 27296289 - SVLEN=450**

``` bash
samplot plot -b HG002_Illumina_Insertion.bam -s 27296000 -e 27296840 -c chr10 -o ./result/insertion/TC002_PER_INS_chr10_27296289.png -t INS
```

**chr10: 27312248 - SVLEN=1294**

``` bash
samplot plot -b HG002_Illumina_Insertion.bam -s 27312100 -e 27313600 -c chr10 -o ./result/insertion/TC002_PER_INS_chr10_27312248.png -t INS
```

**chr13: 65440375 - SVLEN=335**

``` bash
samplot plot -b HG002_Illumina_Insertion.bam -s 65440275 -e 65440900 -c chr13 -o ./result/insertion/TC002_PER_INS_chr13_65440375.png -t INS
```

**chr13: 65449105 - SVLEN=494**

``` bash
samplot plot -b HG002_Illumina_Insertion.bam -s 65448900 -e 65449800 -c chr13 -o ./result/insertion/TC002_PER_INS_chr13_65449105.png -t INS
```

**chr13: 66146710 - SVLEN=1230**

``` bash
samplot plot -b HG002_Illumina_Insertion.bam -s 66146600 -e 66148100 -c chr13 -o ./result/insertion/TC002_PER_INS_chr13_66146710.png -t INS
```

**chr19: 23753136 - SVLEN=464**

``` bash
samplot plot -b HG002_Illumina_Insertion.bam -s 23753100 -e 23753700 -c chr19 -o ./result/insertion/TC002_PER_INS_chr19_23753136.png -t INS
```

------------------------------------------------------------------------

## Test Case 3 - Negative test without insertions

Regions in which no insertions are expected are plotted. Neither data
type should show insertions. Therefore, the Illumina data should only
show noise and no actual evidence of an insertion.

### PacBio commands

**Chromosome 4**

``` bash
samplot plot -b HG002_PacBio_Insertion.bam -s 35785000 -e 35790000 -c chr4 -o ./result/insertion/TC003_LR_INS_chr4_35785000.png -t INS
```

**Chromosome 9**

``` bash
samplot plot -b HG002_PacBio_Insertion.bam -s 73295364 -e 73300000 -c chr9 -o ./result/insertion/TC003_LR_INS_chr9_73314626.png -t INS
```

### Illumina commands

**Chromosome 4**

``` bash
samplot plot -b HG002_Illumina_Insertion.bam -s 35785000 -e 35802843 -c chr4 -o ./result/insertion/TC003_PER_INS_chr4_35785000.png -t INS
```

**Chromosome 9**

``` bash
samplot plot -b HG002_Illumina_Insertion.bam -s 73295364 -e 73314626 -c chr9 -o ./result/insertion/TC003_PER_INS_chr9_73314626.png -t INS
```

------------------------------------------------------------------------

## Test Case 4 - Negative test without alignments

A region without any alignments is plotted. There should be no evidence
of structural variants (SVs), and no reads should be displayed.

### PacBio command

``` bash
samplot plot -b HG002_PacBio_Insertion.bam -s 73295364 -e 73314626 -c chr11 -o ./result/insertion/TC004_LR_INS_chr11_73295364.png -t INS
```

### Illumina command

``` bash
samplot plot -b HG002_Illumina_Insertion.bam -s 73295364 -e 73314626 -c chr11 -o ./result/insertion/TC004_PER_INS_chr11_73295364.png -t INS
```

------------------------------------------------------------------------

## Test Case 5 - Comparison of different coverage levels

Comparison of similarly sized insertions in two regions with different
coverage levels. One insertion should be supported or covered by
significantly more reads than the other.

-   **PacBio data:** The arrows representing the insertion supported by
    multiple reads should be significantly thicker than the arrows
    representing the insertion supported by fewer reads.
-   **Illumina data:** If a region is covered by more reads, the slope
    in that region should be less steep than in a region with fewer
    reads.

------------------------------------------------------------------------

## Test Case 6 - Illustrative example / typical use case

First, a larger region containing an insertion is plotted. The region is
then narrowed to make the insertion easier to see.

This test case is only suitable for Illumina data (paired-end reads).
With long-read data, narrowing the region may cause relevant reads to be
excluded, meaning that the insertion may no longer be displayed
sufficiently.

### Illumina commands

**Larger region**

``` bash
samplot plot -b HG002_Illumina_Insertion.bam -s 24730000 -e 24731300 -c chr1 -o ./result/insertion/TC006_PER_INS_chr1_24730337.png -t INS
```

**Narrowed region (zoom)**

``` bash
samplot plot -b HG002_Illumina_Insertion.bam -s 24730300 -e 24730500 -c chr1 -o ./result/insertion/TC006_PER_INS_chr1_24730337_zoom.png -t INS
```

------------------------------------------------------------------------

## Test Case 7 - Preservation of existing functionality

Existing functionality should be preserved. To verify this, plots are
generated using both the original Samplot code and the extended code,
and then checked to ensure that they still work correctly.

### Options to be tested

-   `--zoom`
-   `--coverage_only`
-   `--max_coverage`

### PacBio commands

**Option `--zoom`**

``` bash
samplot plot -b HG002_PacBio_Insertion.bam -s 23753100 -e 23753700 -c chr19 -o ./result/insertion/TC007_LR_INS_chr19_23753136_zoom.png -t INS --zoom 500
```

**Option `--coverage_only`**

``` bash
samplot plot -b HG002_PacBio_Insertion.bam -s 23753100 -e 23753700 -c chr19 -o ./result/insertion/TC007_LR_INS_chr19_23753136_coverage_only.png -t INS --coverage_only
```

**Option `--max_coverage`**

``` bash
samplot plot -b HG002_PacBio_Insertion.bam -s 23753100 -e 23753700 -c chr19 -o ./result/insertion/TC007_LR_INS_chr19_23753136_max_coverage.png -t INS --max_coverage 80
```

### Illumina commands

**Option `--zoom`**

``` bash
samplot plot -b HG002_Illumina_Insertion.bam -s 23753100 -e 23753700 -c chr19 -o ./result/insertion/TC007_PER_INS_chr19_23753136_zoom.png -t INS --zoom 500
```

**Option `--coverage_only`**

``` bash
samplot plot -b HG002_Illumina_Insertion.bam -s 23753100 -e 23753700 -c chr19 -o ./result/insertion/TC007_PER_INS_chr19_23753136_coverage_only.png -t INS --coverage_only
```

**Option `--max_coverage`**

``` bash
samplot plot -b HG002_Illumina_Insertion.bam -s 23753100 -e 23753700 -c chr19 -o ./result/insertion/TC007_PER_INS_chr19_23753136_max_coverage.png -t INS --max_coverage 80
```

------------------------------------------------------------------------

# Functionality Tests for Other SV Types

*Test commands were created using `samplot/test` on the `master` branch
of the Samplot repository.*

## Test Case 8 - Duplication

Testing the visualization of a duplication.

### Command

``` bash
samplot plot -b HG004_Illumina.bam -s 99813786 -e 99817098 -c chr4 -o ./result/insertion/TC008_PER_DUP_chr4_99813786.png -t DUP
```

------------------------------------------------------------------------

## Test Case 9 - Deletion

Testing the visualization of a deletion.

### Command

``` bash
samplot plot -b HG002_Illumina.bam -s 24804398 -e 24807302 -c chr1 -o ./result/insertion/TC009_PER_DEL_chr1_24804398.png -t DEL
```

**Plot:** A plot was intended to be included at this point in the
original text.

------------------------------------------------------------------------

## Test Case 10 - Inversion

Testing the visualization of an inversion.

### Command

``` bash
samplot plot -b HG004_Illumina.bam -s 12544867 -e 12546613 -c chr12 -o ./result/insertion/TC010_PER_INV_chr12_12544867.png -t INV
```

------------------------------------------------------------------------

## Test Case 12 - Translocation

Testing the visualization of a translocation.

**Note:** No translocation test data could be found.
