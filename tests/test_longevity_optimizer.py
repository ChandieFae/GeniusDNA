import pytest
from ai.protocols.longevity_optimizer import generate_protocol_from_dna


def test_generate_protocol_empty_data():
    """Test protocol generation with empty SNP data"""
    result = generate_protocol_from_dna("")
    assert result == {}


def test_generate_protocol_single_snp():
    """Test protocol generation with single SNP"""
    snp_data = "rs1799853"
    result = generate_protocol_from_dna(snp_data)
    assert "detox" in result
    assert "reduced CYP2C9 function" in result["detox"]


def test_generate_protocol_mthfr():
    """Test MTHFR variant detection"""
    snp_data = "rs1801133"
    result = generate_protocol_from_dna(snp_data)
    assert "methylation" in result
    assert "MTHFR variant" in result["methylation"]


def test_generate_protocol_metabolism():
    """Test metabolism variant detection"""
    snp_data = "rs4994"
    result = generate_protocol_from_dna(snp_data)
    assert "metabolism" in result
    assert "ADRB3" in result["metabolism"]


def test_generate_protocol_vitamin_d():
    """Test Vitamin D receptor variant"""
    snp_data = "rs731236"
    result = generate_protocol_from_dna(snp_data)
    assert "vitamin_d" in result
    assert "VDR gene variant" in result["vitamin_d"]


def test_generate_protocol_multiple_snps():
    """Test protocol generation with multiple SNPs"""
    snp_data = "rs1799853 rs1801133 rs4994 rs731236"
    result = generate_protocol_from_dna(snp_data)
    assert len(result) == 4
    assert "detox" in result
    assert "methylation" in result
    assert "metabolism" in result
    assert "vitamin_d" in result


def test_generate_protocol_no_matching_snps():
    """Test protocol generation with non-matching SNPs"""
    snp_data = "rs99999999 rs88888888"
    result = generate_protocol_from_dna(snp_data)
    assert result == {}
