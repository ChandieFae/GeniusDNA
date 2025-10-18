#!/usr/bin/env python3
"""
Test suite for GeniusDNA AI Longevity Engine
"""

import unittest
import os
import tempfile
from genius_dna import (
    SNP, SNPInfo, SNPDatabase, DNAParser, LongevityEngine, Genotype
)


class TestSNPDatabase(unittest.TestCase):
    """Test SNP Database functionality"""
    
    def setUp(self):
        self.db = SNPDatabase()
    
    def test_database_initialization(self):
        """Test that database initializes with SNPs"""
        snps = self.db.get_all_snps()
        self.assertGreaterEqual(len(snps), 20, "Should have at least 20 SNPs")
    
    def test_detox_snps_present(self):
        """Test that detox-related SNPs are in database"""
        detox_snps = ['rs1695', 'rs762551', 'rs1065852', 'rs4646436']
        for rsid in detox_snps:
            snp_info = self.db.get_snp_info(rsid)
            self.assertIsNotNone(snp_info, f"{rsid} should be in database")
            # Check if categorized as detox (some may be related but categorized differently)
            trait_lower = snp_info.trait.lower()
            self.assertTrue(
                any(term in trait_lower for term in ['detox', 'metabolism', 'drug', 'caffeine']),
                f"{rsid} should be detox-related"
            )
    
    def test_mitochondrial_snps_present(self):
        """Test that mitochondrial SNPs are in database"""
        mito_snps = ['rs8192678', 'rs659366']  # PGC-1α and UCP2
        for rsid in mito_snps:
            snp_info = self.db.get_snp_info(rsid)
            self.assertIsNotNone(snp_info, f"{rsid} should be in database")
    
    def test_cognitive_snps_present(self):
        """Test that cognitive SNPs are in database"""
        cognitive_snps = ['rs4680', 'rs6265', 'rs429358']  # COMT, BDNF, APOE
        for rsid in cognitive_snps:
            snp_info = self.db.get_snp_info(rsid)
            self.assertIsNotNone(snp_info, f"{rsid} should be in database")
    
    def test_snp_info_structure(self):
        """Test that SNP info has all required fields"""
        snp_info = self.db.get_snp_info('rs1801133')
        self.assertIsNotNone(snp_info)
        self.assertEqual(snp_info.rsid, 'rs1801133')
        self.assertEqual(snp_info.gene, 'MTHFR')
        self.assertTrue(len(snp_info.recommendations) > 0)
        self.assertTrue(len(snp_info.description) > 0)
    
    def test_methylation_snps(self):
        """Test MTHFR and other methylation SNPs"""
        methylation_snps = ['rs1801133', 'rs1801131', 'rs1801394']
        for rsid in methylation_snps:
            snp_info = self.db.get_snp_info(rsid)
            self.assertIsNotNone(snp_info)
            self.assertIn('methylation', snp_info.trait.lower())


class TestDNAParser(unittest.TestCase):
    """Test DNA file parsing"""
    
    def test_parse_23andme_format(self):
        """Test parsing 23andMe format"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write("# Comment line\n")
            f.write("# rsid\tchromosome\tposition\tgenotype\n")
            f.write("rs1695\t11\t67352689\tAG\n")
            f.write("rs1801133\t1\t11856378\tCT\n")
            temp_file = f.name
        
        try:
            snps = DNAParser.parse_23andme(temp_file)
            self.assertEqual(len(snps), 2)
            self.assertIn('rs1695', snps)
            self.assertEqual(snps['rs1695'].genotype, 'AG')
            self.assertEqual(snps['rs1801133'].genotype, 'CT')
        finally:
            os.unlink(temp_file)
    
    def test_parse_csv_format(self):
        """Test parsing CSV format"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            f.write("rsid,chromosome,position,genotype\n")
            f.write("rs1695,11,67352689,AG\n")
            f.write("rs1801133,1,11856378,TT\n")
            temp_file = f.name
        
        try:
            snps = DNAParser.parse_csv(temp_file)
            self.assertEqual(len(snps), 2)
            self.assertIn('rs1695', snps)
            self.assertEqual(snps['rs1695'].genotype, 'AG')
            self.assertEqual(snps['rs1801133'].genotype, 'TT')
        finally:
            os.unlink(temp_file)
    
    def test_parse_vcf_format(self):
        """Test parsing VCF format"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.vcf', delete=False) as f:
            f.write("##fileformat=VCFv4.2\n")
            f.write("#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\tSAMPLE1\n")
            f.write("11\t67352689\trs1695\tA\tG\t.\tPASS\t.\tGT\t0/1\n")
            f.write("1\t11856378\trs1801133\tC\tT\t.\tPASS\t.\tGT\t1/1\n")
            temp_file = f.name
        
        try:
            snps = DNAParser.parse_vcf(temp_file)
            self.assertEqual(len(snps), 2)
            self.assertIn('rs1695', snps)
            self.assertEqual(snps['rs1695'].genotype, 'AG')
            self.assertEqual(snps['rs1801133'].genotype, 'TT')
        finally:
            os.unlink(temp_file)
    
    def test_vcf_genotype_conversion(self):
        """Test VCF genotype to allele conversion"""
        # Test homozygous reference
        result = DNAParser._vcf_genotype_to_alleles('0/0', 'A', 'G')
        self.assertEqual(result, 'AA')
        
        # Test heterozygous
        result = DNAParser._vcf_genotype_to_alleles('0/1', 'C', 'T')
        self.assertEqual(result, 'CT')
        
        # Test homozygous alternate
        result = DNAParser._vcf_genotype_to_alleles('1/1', 'C', 'T')
        self.assertEqual(result, 'TT')


class TestLongevityEngine(unittest.TestCase):
    """Test Longevity Engine analysis"""
    
    def setUp(self):
        self.engine = LongevityEngine()
        
        # Create sample DNA data
        self.sample_dna = {
            'rs1695': SNP('rs1695', '11', '67352689', 'AG'),
            'rs1801133': SNP('rs1801133', '1', '11856378', 'TT'),
            'rs762551': SNP('rs762551', '15', '74749576', 'CC'),
            'rs8192678': SNP('rs8192678', '4', '23815662', 'CT'),
            'rs4680': SNP('rs4680', '22', '19951271', 'AG'),
            'rs6265': SNP('rs6265', '11', '27679916', 'AA'),
        }
    
    def test_analyze_dna_basic(self):
        """Test basic DNA analysis"""
        results = self.engine.analyze_dna(self.sample_dna)
        
        # Check that all categories exist
        self.assertIn('detox', results)
        self.assertIn('methylation', results)
        self.assertIn('mitochondrial', results)
        self.assertIn('cognitive', results)
        self.assertIn('summary', results)
        self.assertIn('priority_recommendations', results)
    
    def test_analyze_genotype_normal(self):
        """Test normal genotype analysis"""
        snp = SNP('rs1695', '11', '67352689', 'AA')
        snp_info = self.engine.snp_database.get_snp_info('rs1695')
        result = self.engine._analyze_genotype(snp, snp_info)
        
        self.assertEqual(result['status'], 'normal')
        self.assertEqual(result['risk_level'], 0)
    
    def test_analyze_genotype_carrier(self):
        """Test carrier genotype analysis"""
        snp = SNP('rs1695', '11', '67352689', 'AG')
        snp_info = self.engine.snp_database.get_snp_info('rs1695')
        result = self.engine._analyze_genotype(snp, snp_info)
        
        self.assertEqual(result['status'], 'carrier')
        self.assertEqual(result['risk_level'], 1)
    
    def test_analyze_genotype_at_risk(self):
        """Test at-risk genotype analysis"""
        snp = SNP('rs1801133', '1', '11856378', 'TT')
        snp_info = self.engine.snp_database.get_snp_info('rs1801133')
        result = self.engine._analyze_genotype(snp, snp_info)
        
        self.assertEqual(result['status'], 'at_risk')
        self.assertEqual(result['risk_level'], 2)
    
    def test_categorize_traits(self):
        """Test trait categorization"""
        self.assertEqual(self.engine._categorize_trait('Detoxification'), 'detox')
        self.assertEqual(self.engine._categorize_trait('Methylation'), 'methylation')
        self.assertEqual(self.engine._categorize_trait('Mitochondrial Biogenesis'), 'mitochondrial')
        self.assertEqual(self.engine._categorize_trait('Dopamine Metabolism'), 'cognitive')
        self.assertEqual(self.engine._categorize_trait('Longevity'), 'aging')
    
    def test_generate_report(self):
        """Test report generation"""
        results = self.engine.analyze_dna(self.sample_dna)
        report = self.engine.generate_report(results)
        
        self.assertIn('GENIUSDNA AI LONGEVITY ENGINE', report)
        self.assertIn('RISK SUMMARY', report)
        self.assertIn('PRIORITY RECOMMENDATIONS', report)
        self.assertTrue(len(report) > 100)
    
    def test_high_risk_detection(self):
        """Test detection of high-risk variants"""
        # Create DNA with at-risk variants
        high_risk_dna = {
            'rs1801133': SNP('rs1801133', '1', '11856378', 'TT'),  # MTHFR homozygous
            'rs762551': SNP('rs762551', '15', '74749576', 'CC'),   # CYP1A2 slow
        }
        
        results = self.engine.analyze_dna(high_risk_dna)
        
        # Should have priority recommendations for at-risk variants
        priority = '\n'.join(results['priority_recommendations'])
        self.assertIn('HIGH PRIORITY', priority)
    
    def test_recommendations_present(self):
        """Test that recommendations are generated"""
        results = self.engine.analyze_dna(self.sample_dna)
        
        # Check methylation category (should have rs1801133 with TT genotype)
        if results['methylation']:
            mthfr_result = next((r for r in results['methylation'] 
                               if r['rsid'] == 'rs1801133'), None)
            self.assertIsNotNone(mthfr_result)
            self.assertTrue(len(mthfr_result['recommendations']) > 0)
            self.assertIn('methylfolate', 
                         ' '.join(mthfr_result['recommendations']).lower())


class TestIntegration(unittest.TestCase):
    """Integration tests"""
    
    def test_full_workflow_23andme(self):
        """Test complete workflow with 23andMe file"""
        # Create temporary test file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write("# Test 23andMe file\n")
            f.write("# rsid\tchromosome\tposition\tgenotype\n")
            f.write("rs1695\t11\t67352689\tGG\n")
            f.write("rs1801133\t1\t11856378\tTT\n")
            f.write("rs762551\t15\t74749576\tCC\n")
            f.write("rs8192678\t4\t23815662\tTT\n")
            temp_file = f.name
        
        try:
            # Parse DNA
            dna_data = DNAParser.parse_23andme(temp_file)
            self.assertEqual(len(dna_data), 4)
            
            # Analyze
            engine = LongevityEngine()
            results = engine.analyze_dna(dna_data)
            
            # Verify analysis
            self.assertIsNotNone(results['summary'])
            self.assertTrue(len(results['summary']) > 0)
            
            # Generate report
            report = engine.generate_report(results)
            self.assertIn('GENIUSDNA', report)
            
        finally:
            os.unlink(temp_file)
    
    def test_full_workflow_vcf(self):
        """Test complete workflow with VCF file"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.vcf', delete=False) as f:
            f.write("##fileformat=VCFv4.2\n")
            f.write("#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\tSAMPLE\n")
            f.write("1\t11856378\trs1801133\tC\tT\t.\tPASS\t.\tGT\t0/1\n")
            f.write("15\t74749576\trs762551\tA\tC\t.\tPASS\t.\tGT\t1/1\n")
            temp_file = f.name
        
        try:
            # Parse and analyze
            dna_data = DNAParser.parse_vcf(temp_file)
            engine = LongevityEngine()
            results = engine.analyze_dna(dna_data)
            
            # Should have methylation results for MTHFR
            self.assertTrue(len(results['methylation']) > 0)
            
        finally:
            os.unlink(temp_file)


class TestSNPCoverage(unittest.TestCase):
    """Test coverage of required SNPs from problem statement"""
    
    def setUp(self):
        self.db = SNPDatabase()
    
    def test_detox_snps_coverage(self):
        """Test that requested detox SNPs are included"""
        required_genes = ['CYP1A2', 'GSTM1', 'GSTP1', 'CYP2D6', 'CYP1A1', 'GSTT1']
        
        all_snps = self.db.get_all_snps()
        found_genes = set()
        
        for snp_info in all_snps.values():
            if snp_info.gene in required_genes:
                found_genes.add(snp_info.gene)
        
        for gene in required_genes:
            self.assertIn(gene, found_genes, 
                         f"Detox gene {gene} should be in database")
    
    def test_mitochondrial_snps_coverage(self):
        """Test that mitochondrial SNPs are included"""
        required_genes = ['PPARGC1A', 'UCP2']
        
        all_snps = self.db.get_all_snps()
        found_genes = set()
        
        for snp_info in all_snps.values():
            if 'PPARGC1A' in snp_info.gene or snp_info.gene in required_genes:
                found_genes.add(snp_info.gene)
        
        self.assertIn('PPARGC1A', found_genes, "PGC-1α should be in database")
        self.assertIn('UCP2', found_genes, "UCP2 should be in database")
    
    def test_cognitive_snps_coverage(self):
        """Test that cognitive SNPs are included"""
        required_genes = ['COMT', 'BDNF', 'APOE']
        
        all_snps = self.db.get_all_snps()
        found_genes = set()
        
        for snp_info in all_snps.values():
            if snp_info.gene in required_genes:
                found_genes.add(snp_info.gene)
        
        for gene in required_genes:
            self.assertIn(gene, found_genes, 
                         f"Cognitive gene {gene} should be in database")


if __name__ == '__main__':
    unittest.main()
