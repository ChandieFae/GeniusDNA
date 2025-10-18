from enum import Enum
from typing import List, Optional, Dict
from pydantic import BaseModel, Field
from datetime import datetime


class FileFormat(str, Enum):
    """Supported DNA file formats"""
    TWENTYTHREEANDME = "23andme"
    VCF = "vcf"


class HealthCategory(str, Enum):
    """Health categories for SNP analysis"""
    LONGEVITY = "longevity"
    DETOX = "detox"
    METABOLISM = "metabolism"
    SKIN_AGING = "skin_aging"
    BRAIN_HEALTH = "brain_health"


class RiskLevel(str, Enum):
    """Risk assessment levels"""
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    PROTECTIVE = "protective"


class SNP(BaseModel):
    """Single Nucleotide Polymorphism model"""
    rsid: str = Field(..., description="Reference SNP ID")
    chromosome: str = Field(..., description="Chromosome number")
    position: int = Field(..., description="Position on chromosome")
    genotype: str = Field(..., description="User's genotype (e.g., 'AG', 'TT')")
    gene: Optional[str] = Field(None, description="Associated gene")
    category: HealthCategory = Field(..., description="Health category")
    risk_level: RiskLevel = Field(..., description="Risk assessment")
    description: str = Field(..., description="SNP description")
    recommendations: List[str] = Field(default_factory=list, description="Health recommendations")


class DNAFile(BaseModel):
    """DNA file upload model"""
    filename: str = Field(..., description="Original filename")
    format: FileFormat = Field(..., description="File format")
    upload_time: datetime = Field(default_factory=datetime.utcnow, description="Upload timestamp")
    total_snps: int = Field(0, description="Total SNPs in file")


class AnalysisResult(BaseModel):
    """DNA analysis result model"""
    analysis_id: str = Field(..., description="Unique analysis identifier")
    dna_file: DNAFile = Field(..., description="Source DNA file")
    analyzed_snps: List[SNP] = Field(default_factory=list, description="Analyzed SNPs")
    category_summary: Dict[HealthCategory, int] = Field(
        default_factory=dict, description="SNP count by category"
    )
    analysis_time: datetime = Field(default_factory=datetime.utcnow, description="Analysis timestamp")
    
    class Config:
        use_enum_values = True


class HealthProtocol(BaseModel):
    """AI-generated health protocol"""
    protocol_id: str = Field(..., description="Unique protocol identifier")
    analysis_id: str = Field(..., description="Associated analysis ID")
    category: HealthCategory = Field(..., description="Health category")
    summary: str = Field(..., description="Protocol summary")
    recommendations: List[str] = Field(default_factory=list, description="Detailed recommendations")
    supplements: List[str] = Field(default_factory=list, description="Suggested supplements")
    lifestyle_changes: List[str] = Field(default_factory=list, description="Lifestyle modifications")
    dietary_advice: List[str] = Field(default_factory=list, description="Dietary recommendations")
    priority: str = Field("medium", description="Priority level (low, medium, high)")
    
    class Config:
        use_enum_values = True
