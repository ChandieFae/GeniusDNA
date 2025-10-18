"""
Test VCF multi-sample support and phased genotype parsing.

Tests cover:
- Parsing phased genotypes (|)
- Parsing unphased genotypes (/)
- Multi-sample VCF file handling
- Sample-aware analysis
"""

import pytest
from pathlib import Path


class MockVCFParser:
    """Mock VCF parser for testing multi-sample and phased genotype handling."""
    
    def __init__(self, vcf_content):
        """Initialize with VCF content."""
        self.lines = vcf_content.strip().split('\n')
        self.samples = []
        self.variants = []
        self._parse()
    
    def _parse(self):
        """Parse VCF content."""
        for line in self.lines:
            if line.startswith('##'):
                continue  # Skip meta-information lines
            elif line.startswith('#CHROM'):
                # Header line with sample names
                parts = line.split('\t')
                if len(parts) > 9:
                    self.samples = parts[9:]  # Sample names start at column 10
            elif line and not line.startswith('#'):
                # Variant line
                self._parse_variant(line)
    
    def _parse_variant(self, line):
        """Parse a single variant line."""
        parts = line.split('\t')
        if len(parts) < 8:
            return
        
        chrom = parts[0]
        pos = int(parts[1])
        rsid = parts[2]
        ref = parts[3]
        alt = parts[4]
        format_field = parts[8] if len(parts) > 8 else ''
        
        # Parse genotypes for each sample
        genotypes = {}
        if len(parts) > 9:
            format_keys = format_field.split(':')
            for i, sample_name in enumerate(self.samples):
                sample_data = parts[9 + i]
                genotypes[sample_name] = self._parse_genotype(sample_data, format_keys)
        
        variant = {
            'chrom': chrom,
            'pos': pos,
            'rsid': rsid,
            'ref': ref,
            'alt': alt.split(','),
            'genotypes': genotypes
        }
        self.variants.append(variant)
    
    def _parse_genotype(self, sample_data, format_keys):
        """Parse genotype data for a sample."""
        values = sample_data.split(':')
        result = {}
        
        for key, value in zip(format_keys, values):
            if key == 'GT':
                # Parse genotype: can be phased (|) or unphased (/)
                result['GT'] = value
                result['phased'] = '|' in value
                
                # Extract alleles
                if '|' in value:
                    alleles = value.split('|')
                elif '/' in value:
                    alleles = value.split('/')
                else:
                    alleles = [value]
                
                result['alleles'] = [int(a) if a.isdigit() else None for a in alleles]
            else:
                result[key] = value
        
        return result
    
    def get_sample_genotype(self, rsid, sample_name):
        """Get genotype for a specific sample at a specific variant."""
        for variant in self.variants:
            if variant['rsid'] == rsid:
                return variant['genotypes'].get(sample_name)
        return None
    
    def get_all_samples(self):
        """Get list of all sample names."""
        return self.samples
    
    def is_phased(self, rsid, sample_name):
        """Check if a genotype is phased."""
        gt = self.get_sample_genotype(rsid, sample_name)
        return gt.get('phased', False) if gt else False


def test_parse_phased_genotype():
    """Test parsing of phased genotypes (using | separator)."""
    vcf_content = """##fileformat=VCFv4.2
#CHROM	POS	ID	REF	ALT	QUAL	FILTER	INFO	FORMAT	Sample1
1	100	rs123	A	T	.	PASS	.	GT	0|1"""
    
    parser = MockVCFParser(vcf_content)
    
    assert len(parser.samples) == 1
    assert parser.samples[0] == 'Sample1'
    
    assert len(parser.variants) == 1
    variant = parser.variants[0]
    assert variant['rsid'] == 'rs123'
    
    gt = parser.get_sample_genotype('rs123', 'Sample1')
    assert gt is not None
    assert gt['GT'] == '0|1'
    assert gt['phased'] is True
    assert gt['alleles'] == [0, 1]


def test_parse_unphased_genotype():
    """Test parsing of unphased genotypes (using / separator)."""
    vcf_content = """##fileformat=VCFv4.2
#CHROM	POS	ID	REF	ALT	QUAL	FILTER	INFO	FORMAT	Sample1
1	200	rs456	G	C	.	PASS	.	GT	0/1"""
    
    parser = MockVCFParser(vcf_content)
    
    gt = parser.get_sample_genotype('rs456', 'Sample1')
    assert gt is not None
    assert gt['GT'] == '0/1'
    assert gt['phased'] is False
    assert gt['alleles'] == [0, 1]


def test_parse_multi_sample_vcf():
    """Test parsing VCF with multiple samples."""
    vcf_content = """##fileformat=VCFv4.2
#CHROM	POS	ID	REF	ALT	QUAL	FILTER	INFO	FORMAT	Sample1	Sample2	Sample3
1	300	rs789	T	C	.	PASS	.	GT	0|1	1|1	0|0"""
    
    parser = MockVCFParser(vcf_content)
    
    assert len(parser.samples) == 3
    assert parser.samples == ['Sample1', 'Sample2', 'Sample3']
    
    # Check each sample's genotype
    gt1 = parser.get_sample_genotype('rs789', 'Sample1')
    assert gt1['GT'] == '0|1'
    assert gt1['alleles'] == [0, 1]
    
    gt2 = parser.get_sample_genotype('rs789', 'Sample2')
    assert gt2['GT'] == '1|1'
    assert gt2['alleles'] == [1, 1]
    
    gt3 = parser.get_sample_genotype('rs789', 'Sample3')
    assert gt3['GT'] == '0|0'
    assert gt3['alleles'] == [0, 0]


def test_mixed_phasing():
    """Test VCF with mix of phased and unphased genotypes."""
    vcf_content = """##fileformat=VCFv4.2
#CHROM	POS	ID	REF	ALT	QUAL	FILTER	INFO	FORMAT	Sample1	Sample2
1	400	rs111	A	G	.	PASS	.	GT	0|1	0/1"""
    
    parser = MockVCFParser(vcf_content)
    
    # Sample1 is phased
    assert parser.is_phased('rs111', 'Sample1') is True
    
    # Sample2 is unphased
    assert parser.is_phased('rs111', 'Sample2') is False


def test_multiple_variants_multi_sample():
    """Test multiple variants across multiple samples."""
    vcf_content = """##fileformat=VCFv4.2
#CHROM	POS	ID	REF	ALT	QUAL	FILTER	INFO	FORMAT	Alice	Bob
1	1000	rs1801133	C	T	.	PASS	.	GT	0|1	1|1
1	2000	rs4680	G	A	.	PASS	.	GT	1|0	0|0"""
    
    parser = MockVCFParser(vcf_content)
    
    assert len(parser.variants) == 2
    assert parser.samples == ['Alice', 'Bob']
    
    # Check MTHFR variant
    alice_mthfr = parser.get_sample_genotype('rs1801133', 'Alice')
    assert alice_mthfr['alleles'] == [0, 1]  # Heterozygous
    
    bob_mthfr = parser.get_sample_genotype('rs1801133', 'Bob')
    assert bob_mthfr['alleles'] == [1, 1]  # Homozygous risk
    
    # Check COMT variant
    alice_comt = parser.get_sample_genotype('rs4680', 'Alice')
    assert alice_comt['alleles'] == [1, 0]
    
    bob_comt = parser.get_sample_genotype('rs4680', 'Bob')
    assert bob_comt['alleles'] == [0, 0]  # Homozygous normal


def test_homozygous_genotypes():
    """Test parsing of homozygous genotypes."""
    vcf_content = """##fileformat=VCFv4.2
#CHROM	POS	ID	REF	ALT	QUAL	FILTER	INFO	FORMAT	Sample1
1	500	rs222	A	T	.	PASS	.	GT	1|1"""
    
    parser = MockVCFParser(vcf_content)
    
    gt = parser.get_sample_genotype('rs222', 'Sample1')
    assert gt['alleles'] == [1, 1]  # Homozygous alternate


def test_reference_genotypes():
    """Test parsing of reference (wild-type) genotypes."""
    vcf_content = """##fileformat=VCFv4.2
#CHROM	POS	ID	REF	ALT	QUAL	FILTER	INFO	FORMAT	Sample1
1	600	rs333	G	A	.	PASS	.	GT	0|0"""
    
    parser = MockVCFParser(vcf_content)
    
    gt = parser.get_sample_genotype('rs333', 'Sample1')
    assert gt['alleles'] == [0, 0]  # Homozygous reference


def test_sample_aware_analysis():
    """Test that analysis can distinguish between different samples."""
    vcf_content = """##fileformat=VCFv4.2
#CHROM	POS	ID	REF	ALT	QUAL	FILTER	INFO	FORMAT	HighRisk	LowRisk
1	700	rs444	C	T	.	PASS	.	GT	1|1	0|0"""
    
    parser = MockVCFParser(vcf_content)
    
    high_risk_gt = parser.get_sample_genotype('rs444', 'HighRisk')
    low_risk_gt = parser.get_sample_genotype('rs444', 'LowRisk')
    
    # High risk sample has risk alleles
    assert high_risk_gt['alleles'] == [1, 1]
    
    # Low risk sample has no risk alleles
    assert low_risk_gt['alleles'] == [0, 0]
    
    # Ensure they are different
    assert high_risk_gt['alleles'] != low_risk_gt['alleles']


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
