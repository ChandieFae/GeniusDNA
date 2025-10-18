from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from typing import Dict, List
from datetime import datetime

from ..models import DNAFile, AnalysisResult, HealthProtocol, FileFormat
from ..parsers import parse_dna_file, DNAParser
from ..analyzers import SNPAnalyzer, ProtocolGenerator

router = APIRouter(prefix="/api/v1", tags=["dna"])

# In-memory storage for demo (replace with database in production)
analysis_storage: Dict[str, AnalysisResult] = {}
protocol_storage: Dict[str, List[HealthProtocol]] = {}


@router.get("/")
async def root():
    """API root endpoint"""
    return {
        "message": "GeniusDNA Bio-Optimization Platform API",
        "version": "1.0.0",
        "documentation": "/docs"
    }


@router.post("/dna/upload")
async def upload_dna_file(file: UploadFile = File(...)):
    """
    Upload and analyze a DNA file (23andMe or VCF format)
    
    Args:
        file: DNA file upload
        
    Returns:
        Analysis result with detected SNPs and health insights
    """
    try:
        # Read file content
        content = await file.read()
        content_str = content.decode('utf-8')
        
        # Detect file format
        parser = DNAParser()
        file_format = parser.detect_format(content_str)
        
        if file_format is None:
            raise HTTPException(
                status_code=400,
                detail="Unable to detect DNA file format. Please upload a valid 23andMe or VCF file."
            )
        
        # Parse DNA file
        try:
            parsed_snps = parse_dna_file(content_str, file_format)
        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=f"Error parsing DNA file: {str(e)}"
            )
        
        if not parsed_snps:
            raise HTTPException(
                status_code=400,
                detail="No valid SNPs found in the uploaded file."
            )
        
        # Create DNA file metadata
        dna_file = DNAFile(
            filename=file.filename,
            format=file_format,
            upload_time=datetime.utcnow(),
            total_snps=len(parsed_snps)
        )
        
        # Analyze SNPs
        analyzer = SNPAnalyzer()
        analysis_result = analyzer.analyze_snps(parsed_snps, dna_file)
        
        # Store analysis result
        analysis_storage[analysis_result.analysis_id] = analysis_result
        
        # Generate health protocols
        protocol_gen = ProtocolGenerator()
        protocols = protocol_gen.generate_protocols(analysis_result)
        protocol_storage[analysis_result.analysis_id] = protocols
        
        return {
            "status": "success",
            "message": f"DNA file analyzed successfully. Found {len(analysis_result.analyzed_snps)} health-related SNPs.",
            "analysis_id": analysis_result.analysis_id,
            "summary": {
                "total_snps_uploaded": dna_file.total_snps,
                "health_snps_analyzed": len(analysis_result.analyzed_snps),
                "categories": analysis_result.category_summary
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )


@router.get("/dna/analysis/{analysis_id}")
async def get_analysis(analysis_id: str):
    """
    Get detailed analysis results for a specific DNA upload
    
    Args:
        analysis_id: Unique analysis identifier
        
    Returns:
        Complete analysis result with all detected SNPs
    """
    if analysis_id not in analysis_storage:
        raise HTTPException(
            status_code=404,
            detail=f"Analysis with ID {analysis_id} not found"
        )
    
    analysis = analysis_storage[analysis_id]
    
    return {
        "status": "success",
        "analysis": analysis
    }


@router.get("/protocols/{analysis_id}")
async def get_protocols(analysis_id: str):
    """
    Get AI-generated health protocols for a specific analysis
    
    Args:
        analysis_id: Unique analysis identifier
        
    Returns:
        List of personalized health protocols by category
    """
    if analysis_id not in protocol_storage:
        raise HTTPException(
            status_code=404,
            detail=f"Protocols for analysis ID {analysis_id} not found"
        )
    
    protocols = protocol_storage[analysis_id]
    
    return {
        "status": "success",
        "analysis_id": analysis_id,
        "protocols": protocols,
        "total_protocols": len(protocols)
    }


@router.get("/protocols/{analysis_id}/{category}")
async def get_category_protocol(analysis_id: str, category: str):
    """
    Get health protocol for a specific category
    
    Args:
        analysis_id: Unique analysis identifier
        category: Health category (longevity, detox, metabolism, skin_aging, brain_health)
        
    Returns:
        Health protocol for the specified category
    """
    if analysis_id not in protocol_storage:
        raise HTTPException(
            status_code=404,
            detail=f"Protocols for analysis ID {analysis_id} not found"
        )
    
    protocols = protocol_storage[analysis_id]
    
    # Find protocol for the specified category
    category_protocol = next(
        (p for p in protocols if p.category == category),
        None
    )
    
    if category_protocol is None:
        raise HTTPException(
            status_code=404,
            detail=f"No protocol found for category '{category}' in this analysis"
        )
    
    return {
        "status": "success",
        "protocol": category_protocol
    }


@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "GeniusDNA API"
    }
