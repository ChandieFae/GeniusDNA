# 🧬 GeniusDNA

An AI-powered bio-optimization engine that parses your raw DNA data (e.g., 23andMe) and returns personalized longevity protocols based on key genetic markers (SNPs).

---

## 🚀 Setup

1. **Clone the repo**
2. Install dependencies:
   ```bash
   pip install fastapi uvicorn
## Run the Server
uvicorn backend.main:app --reload

---

##Test the parser
pip install pytest
pytest tests/test_parser.py

---

##🧪 Try It Out (DNA Upload)

Use data/sample_dna.txt as a test file.

Open Postman or use curl:
curl -X POST "http://localhost:8000/upload_dna" \
     -F "file=@data/sample_dna.txt"
---

##📁 Project Structure
geniusdna/
├── backend/
│   └── main.py
├── ai/
│   └── protocols/
│       └── longevity_optimizer.py
├── data/
│   └── sample_dna.txt
├── tests/
│   └── test_parser.py
└── README.md

---

##👁️ Future Features

VCF file support

Blood & wearable data integration

Skin/microbiome modules

React dashboard UI


---








