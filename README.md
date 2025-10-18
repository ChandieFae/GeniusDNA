# 🧬 GeniusDNA: AI-Powered Longevity Engine

GeniusDNA is a bio-optimization platform that outpaces legacy services like 23andMe by merging full DNA parsing with real-time biomarker tracking, epigenetic analysis, and AI-personalized longevity protocols.

## 🚀 Features

- **DNA Analysis**: Upload and analyze genetic data for personalized insights
- **AI-Powered Protocols**: Receive customized longevity and health optimization recommendations
- **SNP Detection**: Identify key genetic variants affecting:
  - Drug metabolism (CYP2C9)
  - Methylation pathways (MTHFR)
  - Fat burning and metabolism (ADRB3)
  - Vitamin D absorption (VDR)

## 📁 Project Structure

```
GeniusDNA/
├── backend/
│   ├── api/               # API routes for DNA upload and analysis
│   ├── services/          # AI + DNA interpretation engine
│   └── main.py            # FastAPI app entry point
├── frontend/              # React + Tailwind UI (planned)
├── ai/
│   └── protocols/         # Personalized protocol generation logic
│       └── longevity_optimizer.py
├── data/                  # SNP reference files, sample data
├── tests/                 # Unit and integration tests
├── docs/                  # System architecture and API documentation
└── requirements.txt       # Python dependencies
```

## 🛠️ Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup

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

## 🏃 Running the Application

Start the FastAPI server:

```bash
cd backend
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

### Interactive API Documentation

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 🧪 Testing

Run all tests:

```bash
pytest
```

Run tests with coverage:

```bash
pytest --cov=. --cov-report=html
```

## 📝 API Usage

### Upload DNA Data

```bash
curl -X POST "http://localhost:8000/upload_dna" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@dna_data.txt"
```

### Example DNA Data File

Create a file `dna_data.txt` with SNP identifiers:
```
rs1799853
rs1801133
rs4994
rs731236
```

### Example Response

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

## 🔬 Supported Genetic Variants

| SNP ID | Gene | Function | Recommendation |
|--------|------|----------|----------------|
| rs1799853 | CYP2C9 | Drug metabolism | Detoxification guidance |
| rs1801133 | MTHFR | Methylation | B vitamin optimization |
| rs4994 | ADRB3 | Fat metabolism | Exercise & supplement advice |
| rs731236 | VDR | Vitamin D receptor | Vitamin D monitoring |

## 🗺️ Roadmap

- [ ] Add real SNP parser (VCF/23andMe formats)
- [ ] Create frontend dashboard with React + Tailwind
- [ ] Integrate real biomarker APIs
- [ ] Expand AI protocol engine with more genetic variants
- [ ] Add user authentication and data persistence
- [ ] Implement epigenetic analysis
- [ ] Add real-time biomarker tracking

## 📚 Documentation

- [Architecture Overview](docs/ARCHITECTURE.md)
- [API Documentation](docs/API.md)

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

See the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

GeniusDNA is a prototype for educational and research purposes. It should not be used as a substitute for professional medical advice, diagnosis, or treatment. Always consult with qualified healthcare providers regarding health decisions.