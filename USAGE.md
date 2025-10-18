# GeniusDNA Usage Guide

## Quick Start

1. Get your raw DNA data from 23andMe, Ancestry, or another provider
2. Run the analysis:

```bash
python3 genius_dna.py your_dna_file.txt
```

## Supported File Formats

### 23andMe Format

The most common format from 23andMe downloads:

```
# rsid	chromosome	position	genotype
rs1695	11	67352689	AG
rs1801133	1	11856378	CT
rs762551	15	74749576	AC
```

Usage:
```bash
python3 genius_dna.py my_23andme_data.txt
```

### CSV Format

Standard comma-separated values with header:

```
rsid,chromosome,position,genotype
rs1695,11,67352689,AG
rs1801133,1,11856378,CT
rs762551,15,74749576,AC
```

Usage:
```bash
python3 genius_dna.py my_dna_data.csv
```

### VCF Format

Standard Variant Call Format (VCF 4.0+):

```
##fileformat=VCFv4.2
#CHROM	POS	ID	REF	ALT	QUAL	FILTER	INFO	FORMAT	SAMPLE1
11	67352689	rs1695	A	G	.	PASS	.	GT	0/1
```

Usage:
```bash
python3 genius_dna.py my_dna_data.vcf
```

## Understanding Your Report

### Risk Summary

The report starts with an overall risk summary for each category:

```
RISK SUMMARY
--------------------------------------------------------------------------------
Detox: Higher risk (score: 6)
Methylation: Moderate risk (score: 3)
Vitamin D: Low risk (score: 0)
```

- **Low risk (0)**: No risk variants detected
- **Moderate risk (1-3)**: One or more carrier variants
- **Higher risk (4+)**: Multiple carrier variants or homozygous risk variants

### Priority Recommendations

High-priority genetic variants are highlighted first:

```
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

### Detailed Results

Each category includes detailed information:

```
DETOXIFICATION GENES
--------------------------------------------------------------------------------

GSTP1 (rs1695)
  Genotype: AG
  Status: carrier
  Description: Affects phase II detoxification...
  Recommendations:
    • Increase glutathione precursors (NAC, glycine, glutamine)
    • Support with cruciferous vegetables
    ...
```

## Real-World Examples

### Example 1: Methylation Support

If you have MTHFR variants (rs1801133 or rs1801131):

**Genotype Found:** rs1801133 = CT or TT

**What It Means:**
- Reduced MTHFR enzyme activity
- Impaired folate metabolism
- Higher homocysteine risk

**Action Steps:**
1. Switch from folic acid to methylfolate (5-MTHF)
2. Take methylcobalamin B12 (1000mcg daily)
3. Add B6 (P5P form, 50mg daily)
4. Monitor homocysteine levels (keep <8 µmol/L)
5. Eat folate-rich foods daily

### Example 2: Caffeine Metabolism

If you have CYP1A2 variant (rs762551):

**Genotype Found:** rs762551 = CC

**What It Means:**
- Slow caffeine metabolizer
- Caffeine stays in system longer
- Higher cardiovascular risk with high intake

**Action Steps:**
1. Limit caffeine to <200mg/day
2. No caffeine after 2pm
3. Consider switching to green tea
4. Monitor blood pressure

### Example 3: Alzheimer's Risk

If you have APOE ε4 variant (rs429358):

**Genotype Found:** rs429358 = CC or TC

**What It Means:**
- One or two copies of APOE ε4
- Higher risk for Alzheimer's disease
- Important to be proactive

**Action Steps:**
1. Follow Mediterranean or ketogenic diet
2. Take high-dose omega-3 (2-3g EPA/DHA daily)
3. Regular exercise and cognitive stimulation
4. Optimize sleep (treat sleep apnea if present)
5. Control inflammation
6. Consider MCT oil supplementation
7. Regular cardiovascular health monitoring

### Example 4: Mitochondrial Support

If you have PPARGC1A variant (rs8192678):

**Genotype Found:** rs8192678 = TT or CT

**What It Means:**
- Reduced PGC-1α activity
- Lower mitochondrial biogenesis
- May affect endurance and energy

**Action Steps:**
1. High-intensity interval training (HIIT) 3x/week
2. CoQ10 supplementation (100-200mg ubiquinol)
3. PQQ 20mg daily
4. Alpha-lipoic acid 300-600mg daily
5. Ensure adequate B-vitamins

## Categories Explained

### 1. Detoxification (5 genes)
**Purpose:** Process toxins, medications, environmental chemicals

**Key Genes:**
- GSTP1, GSTM1, GSTT1: Glutathione conjugation
- CYP1A2: Caffeine and drug metabolism
- CYP2D6: Drug metabolism
- CYP1A1: Phase I detoxification

**If At Risk:** Focus on liver support, antioxidants, minimize toxin exposure

### 2. Methylation (3 genes)
**Purpose:** DNA synthesis, neurotransmitters, detoxification

**Key Genes:**
- MTHFR (C677T, A1298C): Folate metabolism
- MTRR: B12 recycling

**If At Risk:** Use methylated B vitamins, monitor homocysteine

### 3. Vitamin D (2 genes)
**Purpose:** Vitamin D synthesis and binding

**Key Genes:**
- GC: Vitamin D binding protein
- CYP2R1: Vitamin D conversion

**If At Risk:** Higher supplementation needs, regular monitoring

### 4. Fat Metabolism (2 genes)
**Purpose:** Weight management, insulin sensitivity

**Key Genes:**
- FTO: Appetite regulation
- PPARG: Insulin sensitivity

**If At Risk:** High-protein diet, exercise, monitor insulin

### 5. Mitochondrial Function (2 genes)
**Purpose:** Energy production, endurance

**Key Genes:**
- PPARGC1A (PGC-1α): Mitochondrial biogenesis
- UCP2: Mitochondrial uncoupling

**If At Risk:** HIIT training, CoQ10, NAD+ support

### 6. Cognitive Function (4 genes)
**Purpose:** Memory, learning, Alzheimer's risk

**Key Genes:**
- COMT: Dopamine metabolism
- BDNF: Neuroplasticity
- APOE: Alzheimer's risk/protection

**If At Risk:** Omega-3s, exercise, cognitive stimulation

### 7. Aging & Longevity (3 genes)
**Purpose:** Cellular aging, inflammation, lifespan

**Key Genes:**
- FOXO3: Longevity pathway
- CFH: Inflammation
- SIRT1: DNA repair

**If At Risk:** Fasting, resveratrol, NAD+ support

## Supplement Guidelines

Based on your genetic report, you might consider:

### High Priority (if variants present)
- **Methylfolate (5-MTHF)**: For MTHFR variants
- **Methylcobalamin B12**: For MTHFR/MTRR variants
- **NAC**: For glutathione support (GSTP1, GSTM1)
- **Omega-3 (EPA/DHA)**: For APOE, BDNF variants
- **Vitamin D3**: For GC, CYP2R1 variants

### Moderate Priority
- **CoQ10 (ubiquinol)**: For mitochondrial support
- **Magnesium**: General support, especially COMT
- **B-Complex**: Methylated forms if methylation variants
- **Alpha-lipoic acid**: Antioxidant and mitochondrial

### Optional/Advanced
- **NMN or NR**: NAD+ support for aging
- **Resveratrol**: SIRT1 activation
- **PQQ**: Mitochondrial biogenesis
- **Curcumin**: Anti-inflammatory, brain health

**Important:** Always consult healthcare providers before starting supplements, especially if you have medical conditions or take medications.

## Lifestyle Recommendations

### If You Have Detox Variants
- Eat cruciferous vegetables daily
- Minimize processed foods
- Avoid unnecessary medications
- Regular sauna use
- Filter drinking water

### If You Have Methylation Variants
- Avoid folic acid fortification
- Eat leafy greens daily
- Monitor homocysteine annually
- Manage stress
- Ensure B-vitamin intake

### If You Have Mitochondrial Variants
- HIIT training 3x/week
- Fasting or time-restricted eating
- Cold exposure therapy
- Adequate sleep (7-9 hours)
- Manage oxidative stress

### If You Have Cognitive Variants
- Regular aerobic exercise
- Mediterranean diet
- Lifelong learning
- Social engagement
- Quality sleep hygiene
- Stress management

### If You Have APOE ε4
- **Critical:** Aggressive prevention
- Mediterranean or ketogenic diet
- Regular exercise (cardio + strength)
- Cognitive training
- Treat sleep apnea
- Control cardiovascular risk
- Monitor inflammation
- Avoid head trauma

## Testing and Monitoring

Based on your variants, consider regular testing:

### Blood Tests
- **Homocysteine**: If MTHFR variants (keep <8 µmol/L)
- **Vitamin D**: If GC/CYP2R1 variants (target 50-80 ng/mL)
- **B12**: If methylation variants (>500 pg/mL)
- **hsCRP**: If inflammation/aging variants (<1 mg/L)
- **Lipid panel**: If APOE or PPARG variants
- **Fasting glucose/insulin**: If FTO or PPARG variants

### Annual Assessments
- Comprehensive metabolic panel
- Complete blood count
- Thyroid function
- Liver function (if detox variants)
- Cognitive assessment (if APOE ε4)

## Privacy and Security

**Important Notes:**
- Keep your genetic data private and secure
- Be cautious about sharing results
- Understand genetic discrimination laws in your area
- This tool runs locally - your data is not uploaded anywhere
- Consider implications for family members (genetic data is shared)

## Limitations

This tool:
- ✅ Provides educational information
- ✅ Suggests areas for discussion with healthcare providers
- ✅ Identifies genetic predispositions

But does NOT:
- ❌ Diagnose diseases
- ❌ Replace medical advice
- ❌ Predict definite outcomes
- ❌ Consider all genetic variants
- ❌ Account for environment and lifestyle

**Remember:** Genetics is just one factor. Lifestyle, environment, and choices matter more than genes alone.

## Getting Help

If you need assistance:
1. Review this guide thoroughly
2. Check the main README.md
3. Run test files to verify functionality
4. Consult with qualified healthcare providers about results

## Further Reading

- **Methylation:** Dr. Ben Lynch - "Dirty Genes"
- **APOE4:** Dr. Dale Bredesen - "The End of Alzheimer's"
- **Longevity:** Dr. David Sinclair - "Lifespan"
- **SNPedia:** https://www.snpedia.com/
- **Genetic Lifehacks:** https://www.geneticlifehacks.com/
