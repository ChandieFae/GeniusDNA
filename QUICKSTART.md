# GeniusDNA Quick Start Guide

Get started with GeniusDNA in 5 minutes!

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/ChandieFae/GeniusDNA.git
   cd GeniusDNA
   ```

2. **Create and activate virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Running the Server

Start the FastAPI server:

```bash
uvicorn app.main:app --reload
```

The server will start at `http://localhost:8000`

## Interactive API Documentation

Once the server is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Quick Test with cURL

### 1. Check server health
```bash
curl http://localhost:8000/api/v1/health
```

### 2. Upload a DNA file
```bash
curl -X POST http://localhost:8000/api/v1/dna/upload \
  -F "file=@examples/sample_23andme.txt"
```

Response will include an `analysis_id` like:
```json
{
  "status": "success",
  "message": "DNA file analyzed successfully. Found 14 health-related SNPs.",
  "analysis_id": "abc123...",
  "summary": {...}
}
```

### 3. Get detailed analysis
```bash
curl http://localhost:8000/api/v1/dna/analysis/{analysis_id}
```

### 4. Get health protocols
```bash
curl http://localhost:8000/api/v1/protocols/{analysis_id}
```

### 5. Get specific category protocol
```bash
curl http://localhost:8000/api/v1/protocols/{analysis_id}/brain_health
```

Available categories:
- `longevity` - Aging and lifespan markers
- `detox` - Detoxification pathways
- `metabolism` - Weight and energy metabolism
- `skin_aging` - Skin health and collagen
- `brain_health` - Cognitive function and neuroprotection

## Testing with Python

```python
import requests

# Upload DNA file
with open('examples/sample_23andme.txt', 'rb') as f:
    response = requests.post(
        'http://localhost:8000/api/v1/dna/upload',
        files={'file': f}
    )
    result = response.json()
    analysis_id = result['analysis_id']

# Get protocols
protocols = requests.get(
    f'http://localhost:8000/api/v1/protocols/{analysis_id}'
).json()

print(protocols)
```

## Running Tests

```bash
pytest tests/ -v
```

## Example DNA Files

The repository includes two sample DNA files:

- `examples/sample_23andme.txt` - 23andMe format
- `examples/sample_vcf.vcf` - VCF format

Both contain the same genetic data for testing purposes.

## Supported File Formats

### 23andMe Format
Tab-separated text file with header:
```
# rsid    chromosome    position    genotype
rs7412    19    45411941    CC
```

### VCF Format
Standard Variant Call Format:
```
##fileformat=VCFv4.2
#CHROM    POS    ID    REF    ALT    QUAL    FILTER    INFO    FORMAT    SAMPLE
19    45411941    rs7412    C    T    .    PASS    .    GT    0/0
```

## What Gets Analyzed

GeniusDNA analyzes SNPs related to:

1. **Longevity** - APOE, FOXO3, SIRT1
2. **Detoxification** - CYP1A2, NAT2, GSTP1
3. **Metabolism** - FTO, MC4R, PPARG
4. **Skin Aging** - COL1A1, MMP1, SOD2
5. **Brain Health** - BDNF, COMT

Each SNP includes:
- Risk assessment (protective, low, moderate, high)
- Personalized recommendations
- Supplement suggestions
- Lifestyle modifications
- Dietary advice

## Next Steps

- Explore the interactive API documentation at `/docs`
- Check out the complete README.md for more details
- Run the test suite to understand the codebase
- Try uploading your own DNA file (23andMe or VCF format)

## Troubleshooting

**Port already in use:**
```bash
uvicorn app.main:app --reload --port 8001
```

**Import errors:**
Make sure you're in the virtual environment:
```bash
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

**File upload errors:**
Ensure your DNA file is in valid 23andMe or VCF format.

## Support

For issues and questions, please visit:
https://github.com/ChandieFae/GeniusDNA/issues
