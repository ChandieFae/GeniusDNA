# GeniusDNA Architecture

## Overview

GeniusDNA is an AI-powered longevity platform that analyzes DNA data to provide personalized health optimization protocols.

## System Components

### Backend (`/backend`)

#### API Layer (`/backend/api`)
- REST API endpoints for DNA upload and analysis
- Currently implemented in `main.py`

#### Services Layer (`/backend/services`)
- DNA interpretation services
- Biomarker processing (planned)
- User data management (planned)

#### Main Application (`/backend/main.py`)
- FastAPI application
- DNA upload endpoint: `POST /upload_dna`
- Health check endpoint: `GET /`

### AI Engine (`/ai`)

#### Protocol Generation (`/ai/protocols/longevity_optimizer.py`)
- Analyzes SNP data for genetic variants
- Generates personalized recommendations based on:
  - **CYP2C9** (rs1799853): Drug metabolism and detoxification
  - **MTHFR** (rs1801133): Methylation pathway
  - **ADRB3** (rs4994): Metabolism and fat burning
  - **VDR** (rs731236): Vitamin D receptor

### Data (`/data`)
- SNP reference files (planned)
- Sample data for testing

### Frontend (`/frontend`)
- React + Tailwind UI dashboard (planned)
- User profile and recommendations display

### Tests (`/tests`)
- Unit tests for protocol generation
- API integration tests
- Test coverage for all core functionality

## Data Flow

1. User uploads DNA data file via API endpoint
2. FastAPI receives and decodes the file content
3. SNP data is passed to the longevity optimizer
4. AI engine analyzes genetic variants
5. Personalized protocol is generated
6. Results are returned to the user

## Technology Stack

- **Backend Framework**: FastAPI
- **Language**: Python 3.8+
- **Testing**: pytest
- **API Documentation**: OpenAPI/Swagger (built into FastAPI)

## Future Enhancements

- VCF and 23andMe format parsers
- Real-time biomarker tracking integration
- Epigenetic analysis
- User authentication and data persistence
- Frontend dashboard
- Advanced AI protocol engine with machine learning
