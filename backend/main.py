from fastapi import FastAPI, UploadFile, File
from ai.protocols.longevity_optimizer import generate_protocol_from_dna

app = FastAPI(
    title="GeniusDNA API",
    description="AI-Powered Longevity Engine - DNA analysis and personalized protocols",
    version="0.1.0"
)


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "message": "GeniusDNA API is running",
        "version": "0.1.0"
    }


@app.post("/upload_dna")
async def upload_dna(file: UploadFile = File(...)):
    """
    Upload DNA data for analysis and receive personalized longevity protocol.
    
    Args:
        file: DNA data file (text format with SNP information)
        
    Returns:
        Personalized optimization protocol based on genetic variants
    """
    contents = await file.read()
    snp_data = contents.decode("utf-8")
    protocol = generate_protocol_from_dna(snp_data)
    return {"optimized_protocol": protocol}
