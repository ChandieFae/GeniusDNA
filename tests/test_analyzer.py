"""Tests for SNP analyzer"""
import pytest
from app.analyzers import SNPAnalyzer, ProtocolGenerator
from app.models import DNAFile, FileFormat, HealthCategory
from datetime import datetime


class TestSNPAnalyzer:
    """Test SNP analysis functionality"""
    
    def test_analyze_snps_with_known_markers(self):
        """Test analysis of known health markers"""
        parsed_snps = [
            ('rs7412', '19', 45411941, 'CC'),  # APOE protective
            ('rs429358', '19', 45412079, 'CT'),  # APOE moderate risk
            ('rs9939609', '16', 53820527, 'AA')  # FTO high risk
        ]
        
        dna_file = DNAFile(
            filename="test.txt",
            format=FileFormat.TWENTYTHREEANDME,
            total_snps=len(parsed_snps)
        )
        
        analyzer = SNPAnalyzer()
        result = analyzer.analyze_snps(parsed_snps, dna_file)
        
        assert result.analysis_id is not None
        assert len(result.analyzed_snps) == 3
        assert HealthCategory.LONGEVITY in result.category_summary
        assert HealthCategory.METABOLISM in result.category_summary
    
    def test_analyze_snps_filters_unknown(self):
        """Test that unknown SNPs are filtered out"""
        parsed_snps = [
            ('rs7412', '19', 45411941, 'CC'),  # Known
            ('rs999999999', '1', 12345, 'AG')  # Unknown
        ]
        
        dna_file = DNAFile(
            filename="test.txt",
            format=FileFormat.TWENTYTHREEANDME,
            total_snps=len(parsed_snps)
        )
        
        analyzer = SNPAnalyzer()
        result = analyzer.analyze_snps(parsed_snps, dna_file)
        
        # Only known SNP should be in results
        assert len(result.analyzed_snps) == 1
        assert result.analyzed_snps[0].rsid == 'rs7412'
    
    def test_get_snps_by_category(self):
        """Test filtering SNPs by category"""
        parsed_snps = [
            ('rs7412', '19', 45411941, 'CC'),  # Longevity
            ('rs9939609', '16', 53820527, 'AA')  # Metabolism
        ]
        
        dna_file = DNAFile(
            filename="test.txt",
            format=FileFormat.TWENTYTHREEANDME,
            total_snps=len(parsed_snps)
        )
        
        analyzer = SNPAnalyzer()
        result = analyzer.analyze_snps(parsed_snps, dna_file)
        
        longevity_snps = analyzer.get_snps_by_category(result, HealthCategory.LONGEVITY)
        assert len(longevity_snps) == 1
        assert longevity_snps[0].gene == 'APOE'


class TestProtocolGenerator:
    """Test health protocol generation"""
    
    def test_generate_protocols(self):
        """Test generation of health protocols"""
        parsed_snps = [
            ('rs7412', '19', 45411941, 'CC'),
            ('rs9939609', '16', 53820527, 'AA')
        ]
        
        dna_file = DNAFile(
            filename="test.txt",
            format=FileFormat.TWENTYTHREEANDME,
            total_snps=len(parsed_snps)
        )
        
        analyzer = SNPAnalyzer()
        result = analyzer.analyze_snps(parsed_snps, dna_file)
        
        generator = ProtocolGenerator()
        protocols = generator.generate_protocols(result)
        
        assert len(protocols) == 2  # One for longevity, one for metabolism
        assert all(p.protocol_id is not None for p in protocols)
        assert all(p.summary for p in protocols)
    
    def test_protocol_has_recommendations(self):
        """Test that protocols include recommendations"""
        parsed_snps = [
            ('rs7412', '19', 45411941, 'CC')
        ]
        
        dna_file = DNAFile(
            filename="test.txt",
            format=FileFormat.TWENTYTHREEANDME,
            total_snps=len(parsed_snps)
        )
        
        analyzer = SNPAnalyzer()
        result = analyzer.analyze_snps(parsed_snps, dna_file)
        
        generator = ProtocolGenerator()
        protocols = generator.generate_protocols(result)
        
        assert len(protocols) > 0
        protocol = protocols[0]
        assert len(protocol.recommendations) > 0
