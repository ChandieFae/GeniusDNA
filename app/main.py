from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api import dna_router

# Create FastAPI application
app = FastAPI(
    title="GeniusDNA Bio-Optimization Platform",
    description="""
    GeniusDNA is a comprehensive bio-optimization platform that analyzes DNA data 
    to provide personalized health recommendations.
    
    ## Features
    
    * **DNA File Upload**: Support for 23andMe and VCF formats
    * **SNP Detection**: Identify health-related genetic markers
    * **Health Categories**: Longevity, Detox, Metabolism, Skin Aging, Brain Health
    * **AI-Powered Protocols**: Personalized health recommendations
    
    ## Supported File Formats
    
    * 23andMe raw data files
    * VCF (Variant Call Format) files
    
    ## Health Insights
    
    Our platform analyzes genetic markers related to:
    - Longevity and aging
    - Detoxification pathways
    - Metabolic function
    - Skin health and aging
    - Brain health and cognition
    """,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS for future frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(dna_router)


@app.on_event("startup")
async def startup_event():
    """Application startup event"""
    print("🧬 GeniusDNA Bio-Optimization Platform Starting...")
    print("📊 API Documentation: http://localhost:8000/docs")
    print("✅ Server ready to accept DNA file uploads")


@app.on_event("shutdown")
async def shutdown_event():
    """Application shutdown event"""
    print("👋 GeniusDNA shutting down...")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
