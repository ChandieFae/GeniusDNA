import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)


def test_root_endpoint():
    """Test the root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()
    assert response.json()["message"] == "GeniusDNA API is running"


def test_upload_dna_empty_file():
    """Test DNA upload with empty file"""
    files = {"file": ("test.txt", b"", "text/plain")}
    response = client.post("/upload_dna", files=files)
    assert response.status_code == 200
    assert "optimized_protocol" in response.json()
    assert response.json()["optimized_protocol"] == {}


def test_upload_dna_with_snps():
    """Test DNA upload with SNP data"""
    snp_data = b"rs1799853 rs1801133"
    files = {"file": ("dna_data.txt", snp_data, "text/plain")}
    response = client.post("/upload_dna", files=files)
    assert response.status_code == 200
    result = response.json()
    assert "optimized_protocol" in result
    protocol = result["optimized_protocol"]
    assert "detox" in protocol
    assert "methylation" in protocol


def test_upload_dna_all_variants():
    """Test DNA upload with all supported variants"""
    snp_data = b"rs1799853 rs1801133 rs4994 rs731236"
    files = {"file": ("dna_data.txt", snp_data, "text/plain")}
    response = client.post("/upload_dna", files=files)
    assert response.status_code == 200
    result = response.json()
    protocol = result["optimized_protocol"]
    assert len(protocol) == 4
    assert "detox" in protocol
    assert "methylation" in protocol
    assert "metabolism" in protocol
    assert "vitamin_d" in protocol


def test_upload_dna_no_matching_variants():
    """Test DNA upload with no matching variants"""
    snp_data = b"rs999999 rs888888"
    files = {"file": ("dna_data.txt", snp_data, "text/plain")}
    response = client.post("/upload_dna", files=files)
    assert response.status_code == 200
    result = response.json()
    assert result["optimized_protocol"] == {}
