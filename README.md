# GeniusDNA AI Longevity Engine

A comprehensive Python tool for analyzing raw DNA data and generating personalized longevity protocols based on genetic variants (SNPs).

## Features

- **Multi-format Support**: Parse 23andMe, CSV, and VCF format DNA files
- **Comprehensive SNP Database**: Analyzes 30+ genetic variants across multiple health categories:
  - **Detoxification**: GSTP1, CYP2D6, CYP1A2, GSTM1, CYP1A1
  - **Methylation**: MTHFR (C677T, A1298C), MTRR
  - **Vitamin D Metabolism**: GC, CYP2R1
  - **Fat Metabolism**: FTO, PPARG
  - **Mitochondrial Function**: PPARGC1A (PGC-1α), UCP2
  - **Cognitive Traits**: COMT, BDNF, APOE (ε2, ε3, ε4)
  - **Aging & Longevity**: FOXO3, CFH, SIRT1

- **Personalized Recommendations**: Get specific, actionable recommendations based on your genetic profile
- **Risk Assessment**: Understand your genetic predispositions with clear risk scoring
- **Detailed Reports**: Comprehensive reports with explanations and prioritized actions

## Installation

No external dependencies required! Uses Python 3 standard library only.

```bash
git clone https://github.com/ChandieFae/GeniusDNA.git
cd GeniusDNA
```

## Usage

### Basic Usage

```bash
python3 genius_dna.py <dna_file>
```

Supported file formats:
- `.txt` - 23andMe format
- `.csv` - CSV format with columns: rsid, chromosome, position, genotype
- `.vcf` - Standard VCF format

### Example

```bash
# Analyze 23andMe data
python3 genius_dna.py sample_23andme.txt

# Analyze CSV data
python3 genius_dna.py sample.csv

# Analyze VCF data
python3 genius_dna.py sample.vcf
```

## File Formats

### 23andMe Format (.txt)
```
# rsid	chromosome	position	genotype
rs1695	11	67352689	AG
rs1801133	1	11856378	CT
```

### CSV Format (.csv)
```
rsid,chromosome,position,genotype
rs1695,11,67352689,AG
rs1801133,1,11856378,CT
```

### VCF Format (.vcf)
Standard VCF 4.2 format with GT (genotype) field.

## Understanding Your Results

### Risk Levels
- **Low risk**: Optimal or normal genotype
- **Moderate risk (carrier)**: One copy of risk variant
- **Higher risk (at_risk)**: Two copies of risk variant

### Categories

#### Detoxification Genes
Affects your ability to process toxins, medications, and environmental chemicals.
- Key genes: GSTP1, CYP2D6, CYP1A2, GSTM1, CYP1A1

#### Methylation Genes
Critical for DNA synthesis, neurotransmitter production, and detoxification.
- Key genes: MTHFR, MTRR

#### Vitamin D Metabolism
Impacts vitamin D synthesis and utilization.
- Key genes: GC, CYP2R1

#### Fat Metabolism
Affects weight management, insulin sensitivity, and metabolic health.
- Key genes: FTO, PPARG

#### Mitochondrial Function
Impacts energy production, endurance, and cellular aging.
- Key genes: PPARGC1A (PGC-1α), UCP2

#### Cognitive Function
Affects memory, learning, stress response, and Alzheimer's risk.
- Key genes: COMT, BDNF, APOE

#### Aging & Longevity
Influences cellular aging, inflammation, and lifespan.
- Key genes: FOXO3, CFH, SIRT1

## Example Output

```
================================================================================
GENIUSDNA AI LONGEVITY ENGINE - GENETIC ANALYSIS REPORT
================================================================================

RISK SUMMARY
--------------------------------------------------------------------------------
Detox: Higher risk (score: 6)
Methylation: Moderate risk (score: 3)
...

PRIORITY RECOMMENDATIONS
--------------------------------------------------------------------------------
=== HIGH PRIORITY GENETIC VARIANTS DETECTED ===

MTHFR (rs1801133): TT
Status: AT_RISK
Description: C677T variant reduces MTHFR enzyme activity by 30-70%...

Recommended Actions:
  • Take methylfolate (5-MTHF) instead of folic acid
  • Supplement with methylcobalamin (B12) 1000mcg daily
  ...
```

## SNP Database

The engine includes detailed information for 30+ SNPs:

### Detox SNPs
- **rs1695** (GSTP1): Glutathione conjugation
- **rs1065852** (CYP2D6): Drug metabolism
- **rs762551** (CYP1A2): Caffeine metabolism
- **rs4680** (GSTM1): Glutathione detox
- **rs4646436** (CYP1A1): Phase I detoxification

### Methylation SNPs
- **rs1801133** (MTHFR C677T): Folate metabolism
- **rs1801131** (MTHFR A1298C): Methylation support
- **rs1801394** (MTRR): B12 recycling

### Mitochondrial SNPs
- **rs8192678** (PPARGC1A/PGC-1α): Mitochondrial biogenesis
- **rs659366** (UCP2): Mitochondrial uncoupling

### Cognitive SNPs
- **rs4680** (COMT): Dopamine metabolism
- **rs6265** (BDNF): Neuroplasticity
- **rs429358** (APOE ε4): Alzheimer's risk
- **rs7412** (APOE ε2): Alzheimer's protection

### And many more...

## Disclaimer

This tool is for informational and educational purposes only. It is not intended to diagnose, treat, cure, or prevent any disease. Always consult with qualified healthcare professionals before making any health decisions or implementing recommendations based on genetic information.

Genetic data is just one factor in health outcomes. Lifestyle, environment, and other factors play crucial roles in health and longevity.

## Contributing

Contributions are welcome! Please feel free to submit pull requests to expand the SNP database or improve functionality.

## License

See LICENSE file for details.

## References

- dbSNP Database: https://www.ncbi.nlm.nih.gov/snp/
- ClinVar: https://www.ncbi.nlm.nih.gov/clinvar/
- SNPedia: https://www.snpedia.com/
- Published scientific literature on genetic variants and health outcomes