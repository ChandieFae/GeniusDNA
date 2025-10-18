# GeniusDNA API Documentation

## Base URL
```
http://localhost:8000
```

## Endpoints

### Health Check
```
GET /
```

**Response:**
```json
{
  "message": "GeniusDNA API is running",
  "version": "0.1.0"
}
```

### Upload DNA Data
```
POST /upload_dna
```

Upload DNA data for analysis and receive personalized longevity protocol.

**Request:**
- Content-Type: `multipart/form-data`
- Body: DNA data file (text format containing SNP identifiers)

**Example DNA Data File:**
```
rs1799853
rs1801133
rs4994
rs731236
```

**Response:**
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

**Supported SNPs:**

| SNP ID | Gene | Function | Recommendation Category |
|--------|------|----------|------------------------|
| rs1799853 | CYP2C9 | Drug metabolism | Detoxification |
| rs1801133 | MTHFR | Methylation | B vitamin supplementation |
| rs4994 | ADRB3 | Fat metabolism | Exercise & metabolism |
| rs731236 | VDR | Vitamin D receptor | Vitamin D optimization |

**Example cURL Request:**
```bash
curl -X POST "http://localhost:8000/upload_dna" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@dna_data.txt"
```

## Interactive Documentation

FastAPI provides automatic interactive API documentation:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
