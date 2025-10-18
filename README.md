# GeniusDNA

GeniusDNA is a developer-focused DNA analysis toolkit and prototype AI longevity engine.  
This repository contains parsers for common consumer DNA formats (23andMe, VCF, CSV), a sample SNP database with provenance, a protocol generator, a FastAPI backend, and supporting CLI tools & tests.

> WARNING: The SNP database and recommendations in this repo are for development and testing only. They are NOT clinical advice. Validate all variants and citations against primary literature and clinical sources before using in production or for healthcare decisions.

## Quickstart

1. Create a virtual environment and install dependencies:
   ```bash
   python -m venv .venv
   source .venv/bin/activate     # Windows: .venv\Scripts\activate
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```

2. Run the API (development):
   ```bash
   # from repo root
   uvicorn backend.main:app --reload
   # open http://127.0.0.1:8000/docs for interactive API docs
   ```

3. Upload a DNA file to the API (example):
   ```bash
   curl -X POST "http://127.0.0.1:8000/upload_dna" -F "file=@data/sample_23andme.txt"
   ```

## SNP Database (versioned & provenance)

- JSON: `data/snp_database.json` — primary runtime DB. Includes `metadata` (version, generated_by, citation, notes) and per-entry `provenance`.
- CSV: `data/snp_database.csv` — canonical CSV export with provenance columns for easier editing and CI.

Do NOT use the DB for clinical decisions. Each entry contains `source` and `provenance.citation` to help you track primary evidence.

## DB CLI & Validator

Two helper tools are included:

- Converter / CLI: `cli/load_snp_db.py`
  - Convert CSV → JSON and set version:
    ```bash
    python cli/load_snp_db.py convert --csv data/snp_database.csv --out data/snp_database.json --version 0.2.1
    ```
  - Validate DB:
    ```bash
    python cli/load_snp_db.py validate --json data/snp_database.json --csv data/snp_database.csv
    ```

- Validator: `tools/validate_snp_db.py`
  - A small script that checks required fields and metadata.
    ```bash
    python tools/validate_snp_db.py --json data/snp_database.json --csv data/snp_database.csv
    ```

## Running Tests Locally

From repo root:

- Ensure repo root is on PYTHONPATH so tests import local packages:
  - macOS/Linux:
    ```bash
    export PYTHONPATH=$(pwd)
    pytest -q
    ```
  - Windows (PowerShell):
    ```powershell
    $env:PYTHONPATH = (Get-Location).Path
    pytest -q
    ```

Tests include parser/unit tests and multisample/phased-VCF tests.

## How to Watch PR CI (GitHub Actions)

You can watch the draft PR CI run from the browser or from the terminal. The CI workflow file is `.github/workflows/ci.yml` (runs pytest on pushes and PRs).

1. Web UI
   - Open the PR: `https://github.com/ChandieFae/GeniusDNA/pull/6`
   - Click the "Checks" tab or the "Details" links next to each check to view job logs and artifacts.
   - Expand each job and click a step to view its stdout/stderr.

2. GitHub CLI (recommended)
   - Authenticate if necessary:
     ```bash
     gh auth login
     ```
   - List recent runs for the repo or the workflow:
     ```bash
     gh run list --repo ChandieFae/GeniusDNA --workflow ci.yml
     ```
     Or filter by branch:
     ```bash
     gh run list --repo ChandieFae/GeniusDNA --branch feature/expand-snp-db-provenance-cli
     ```
   - Get the run ID and stream logs:
     ```bash
     gh run view <run-id> --repo ChandieFae/GeniusDNA --log
     ```
     Or watch live output:
     ```bash
     gh run watch <run-id> --repo ChandieFae/GeniusDNA
     ```
   - Open the PR in your browser from CLI:
     ```bash
     gh pr view 6 --repo ChandieFae/GeniusDNA --web
     ```

3. Raw GitHub Actions API (if you prefer curl)
   - List workflow runs for a branch:
     ```bash
     curl -H "Authorization: token $GITHUB_TOKEN" \
       "https://api.github.com/repos/ChandieFae/GeniusDNA/actions/runs?branch=feature/expand-snp-db-provenance-cli"
     ```
   - Download logs for a run:
     ```bash
     curl -L -H "Authorization: token $GITHUB_TOKEN" \
       "https://api.github.com/repos/ChandieFae/GeniusDNA/actions/runs/<run-id>/logs" -o logs.zip
     ```

## Merge flow (after CI passes)

1. Make draft PR ready:
   - Web UI: click "Ready for review"
   - CLI:
     ```bash
     gh pr ready 6 --repo ChandieFae/GeniusDNA
     ```

2. Merge when checks are green:
   ```bash
   # merge commit
   gh pr merge 6 --repo ChandieFae/GeniusDNA --merge
   # or squash
   gh pr merge 6 --repo ChandieFae/GeniusDNA --squash
   ```

3. Optionally, delete the feature branch:
   ```bash
   gh pr merge 6 --repo ChandieFae/GeniusDNA --delete-branch
   ```

## Contributing

- Add or update SNP entries in `data/snp_database.csv`. Use `cli/load_snp_db.py convert` to regenerate JSON and set a new `metadata.version`.
- Always include `provenance_citation` for new entries.
- Update tests when you change parsing behavior or DB schema.

## License & Disclaimer

- License: MIT (see LICENSE).
- This repository is for research and development only. Not medical advice. Consult clinicians and primary literature before using this dataset for health decisions.
