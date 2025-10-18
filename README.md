# GeniusDNA

A bio-optimization platform for personalized health insights based on genetic data.

## Overview

GeniusDNA is a comprehensive bio-optimization platform that analyzes DNA data to provide personalized health recommendations. Users can upload full DNA files (23andMe or VCF format) to detect SNPs (Single Nucleotide Polymorphisms) related to:

- **Longevity**: Genes associated with aging and lifespan
- **Detoxification**: Metabolic pathways for toxin processing
- **Metabolism**: Energy production and nutrient processing
- **Skin Aging**: Collagen, elastin, and skin health markers
- **Brain Health**: Cognitive function and neuroprotection

## Features

### Current Version
- FastAPI backend for high-performance data processing
- DNA file parsing for 23andMe and VCF formats
- SNP detection for multiple health categories
- AI-powered health protocol generation
- RESTful API endpoints for DNA upload and analysis

### Future Enhancements
- Blood biomarker integration
- Wearable device data integration
- Gut and skin microbiome analysis
- React frontend dashboard
- Personalized, trackable recommendations
- Dynamic health goals based on genetic and epigenetic input

## Installation

1. Clone the repository:
```bash
git clone https://github.com/ChandieFae/GeniusDNA.git
cd GeniusDNA
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Starting the Server

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

### API Documentation

Interactive API documentation is available at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### API Endpoints

#### Upload DNA File
```
POST /api/v1/dna/upload
```
Upload a DNA file (23andMe or VCF format) for analysis.

#### Get Analysis Results
```
GET /api/v1/dna/analysis/{analysis_id}
```
Retrieve analysis results for a specific DNA upload.

#### Get Health Protocols
```
GET /api/v1/protocols/{analysis_id}
```
Get AI-generated health protocols based on DNA analysis.

## DNA File Formats

### 23andMe Format
Text file with header lines starting with `#`, followed by tab-separated values:
```
# rsid  chromosome  position  genotype
rs1234567  1  12345  AG
```

### VCF Format
Standard Variant Call Format with header lines and variant data:
```
##fileformat=VCFv4.2
#CHROM  POS  ID  REF  ALT  QUAL  FILTER  INFO  FORMAT  SAMPLE
1  12345  rs1234567  A  G  .  PASS  .  GT  0/1
```

## Health Categories

### Longevity Markers
- APOE: Alzheimer's risk and longevity
- FOXO3: Longevity and stress resistance
- SIRT1: Aging and cellular health

### Detox Markers
- GSTM1: Glutathione S-transferase
- CYP1A2: Caffeine metabolism
- NAT2: Toxin acetylation

### Metabolism Markers
- FTO: Fat mass and obesity
- MC4R: Appetite regulation
- PPARG: Glucose metabolism

### Skin Aging Markers
- COL1A1: Collagen production
- MMP1: Matrix metalloproteinase
- SOD2: Antioxidant defense

### Brain Health Markers
- BDNF: Neuroplasticity
- COMT: Neurotransmitter metabolism
- APOE: Cognitive function

## Project Structure

```
GeniusDNA/
├── app/
│   ├── main.py              # FastAPI application entry point
│   ├── models/              # Data models
│   ├── parsers/             # DNA file parsers
│   ├── analyzers/           # SNP analysis logic
│   ├── api/                 # API routes
│   └── data/                # SNP database
├── tests/                   # Test suite
├── requirements.txt         # Python dependencies
└── README.md               # Documentation
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer

This software is for informational purposes only and is not intended to diagnose, treat, cure, or prevent any disease. Always consult with a healthcare professional before making any health decisions.