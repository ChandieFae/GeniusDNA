"""Tests for DNA file parsers"""
import pytest
from app.parsers import DNAParser, parse_dna_file
from app.models import FileFormat


class TestDNAParser:
    """Test DNA file parsing functionality"""
    
    def test_detect_23andme_format(self):
        """Test detection of 23andMe format"""
        content = """# rsid\tchromosome\tposition\tgenotype
rs4477212\t1\t82154\tAA
rs3094315\t1\t752566\tAG
rs3131972\t1\t752721\tGG"""
        
        parser = DNAParser()
        format_detected = parser.detect_format(content)
        assert format_detected == FileFormat.TWENTYTHREEANDME
    
    def test_detect_vcf_format(self):
        """Test detection of VCF format"""
        content = """##fileformat=VCFv4.2
##contig=<ID=1,length=249250621>
#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\tSAMPLE
1\t82154\trs4477212\tA\tG\t.\tPASS\t.\tGT\t0/1"""
        
        parser = DNAParser()
        format_detected = parser.detect_format(content)
        assert format_detected == FileFormat.VCF
    
    def test_parse_23andme_file(self):
        """Test parsing of 23andMe format"""
        content = """# rsid\tchromosome\tposition\tgenotype
rs4477212\t1\t82154\tAA
rs3094315\t1\t752566\tAG
rs3131972\t1\t752721\tGG"""
        
        parser = DNAParser()
        snps = parser.parse_23andme(content)
        
        assert len(snps) == 3
        assert snps[0] == ('rs4477212', '1', 82154, 'AA')
        assert snps[1] == ('rs3094315', '1', 752566, 'AG')
        assert snps[2] == ('rs3131972', '1', 752721, 'GG')
    
    def test_parse_vcf_file(self):
        """Test parsing of VCF format"""
        content = """##fileformat=VCFv4.2
#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\tSAMPLE
1\t82154\trs4477212\tA\tG\t.\tPASS\t.\tGT\t0/1"""
        
        parser = DNAParser()
        snps = parser.parse_vcf(content)
        
        assert len(snps) == 1
        assert snps[0][0] == 'rs4477212'
        assert snps[0][1] == '1'
        assert snps[0][2] == 82154
    
    def test_parse_dna_file_auto_detect(self):
        """Test automatic format detection"""
        content = """# rsid\tchromosome\tposition\tgenotype
rs4477212\t1\t82154\tAA"""
        
        snps = parse_dna_file(content)
        assert len(snps) > 0
    
    def test_invalid_format_raises_error(self):
        """Test that invalid format raises ValueError"""
        content = "This is not a valid DNA file"
        
        with pytest.raises(ValueError):
            parse_dna_file(content)
