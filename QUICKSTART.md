# GeniusDNA Quick Start Guide

## Installation

1. **Clone the repository:**
```bash
git clone https://github.com/ChandieFae/GeniusDNA.git
cd GeniusDNA
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

## Running the Application

### Option 1: Using the run script
```bash
./run_server.sh
```

### Option 2: Using uvicorn directly
```bash
uvicorn backend.main:app --reload
```

The server will start at `http://localhost:8000`

## Testing the API

### 1. Check if the server is running:
```bash
curl http://localhost:8000/
```

Expected response:
```json
{
  "message": "GeniusDNA API is running",
  "version": "0.1.0"
}
```

### 2. Upload DNA data:
```bash
curl -X POST "http://localhost:8000/upload_dna" \
  -F "file=@data/sample_dna.txt"
```

Expected response:
```json
{
  "optimized_protocol": {
    "detox": "You may have reduced CYP2C9 function. Avoid NSAIDs, increase cruciferous vegetables.",
    "methylation": "MTHFR variant detected. Supplement with methylated B12 and folate.",
    "metabolism": "ADRB3 variant suggests lower fat burning. Prioritize HIIT and green tea extract.",
    "vitamin_d": "VDR gene variant. Monitor vitamin D levels closely and supplement as needed."
  }
}
```

## Interactive API Documentation

Once the server is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Running Tests

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_api.py

# Run with coverage
pytest --cov=. --cov-report=html
```

## Creating Your Own DNA Data File

Create a text file with SNP identifiers (one per line):

```text
rs1799853
rs1801133
rs4994
rs731236
```

Currently supported SNPs:
- `rs1799853` - CYP2C9 (Drug metabolism)
- `rs1801133` - MTHFR (Methylation)
- `rs4994` - ADRB3 (Metabolism)
- `rs731236` - VDR (Vitamin D)

## Project Structure

```
GeniusDNA/
├── backend/           # FastAPI application
│   ├── main.py       # API endpoints
│   ├── api/          # API routes (for future expansion)
│   └── services/     # Business logic (for future expansion)
├── ai/
│   └── protocols/    # AI protocol generation
│       └── longevity_optimizer.py
├── tests/            # Test suite
├── data/             # Sample data and references
└── docs/             # Documentation
```

## Next Steps

1. Explore the [API Documentation](docs/API.md)
2. Read the [Architecture Overview](docs/ARCHITECTURE.md)
3. Check the [Roadmap](README.md#-roadmap) for upcoming features

## Troubleshooting

### Port already in use
If port 8000 is already in use, specify a different port:
```bash
uvicorn backend.main:app --port 8001
```

### Module not found errors
Make sure you're running uvicorn from the project root:
```bash
# From GeniusDNA/ directory:
uvicorn backend.main:app --reload
```

### Import errors
Ensure all dependencies are installed:
```bash
pip install -r requirements.txt
```

## Support

For issues and questions, please visit the [GitHub repository](https://github.com/ChandieFae/GeniusDNA).
