#!/usr/bin/env python3
"""
Validator for SNP database (JSON and CSV formats).

Checks:
- Metadata presence and structure
- Per-entry provenance (citation, version)
- Required fields for each SNP entry
- Consistency between JSON and CSV if both exist
"""

import json
import csv
import sys
from pathlib import Path


def validate_json_metadata(data):
    """Validate metadata structure in JSON."""
    errors = []
    
    if 'metadata' not in data:
        errors.append("Missing 'metadata' key in JSON")
        return errors
    
    metadata = data['metadata']
    required_fields = ['version', 'generated_by', 'citation', 'notes']
    
    for field in required_fields:
        if field not in metadata:
            errors.append(f"Missing '{field}' in metadata")
    
    return errors


def validate_json_entry(rsid, entry):
    """Validate a single SNP entry in JSON."""
    errors = []
    
    required_fields = ['gene', 'description', 'risk_alleles', 'recommendations', 
                      'category', 'source', 'provenance']
    
    for field in required_fields:
        if field not in entry:
            errors.append(f"{rsid}: Missing required field '{field}'")
    
    # Validate provenance structure
    if 'provenance' in entry:
        prov = entry['provenance']
        if not isinstance(prov, dict):
            errors.append(f"{rsid}: Provenance must be a dictionary")
        else:
            if 'version' not in prov:
                errors.append(f"{rsid}: Missing 'version' in provenance")
            if 'citation' not in prov:
                errors.append(f"{rsid}: Missing 'citation' in provenance")
    
    # Validate risk_alleles is a list
    if 'risk_alleles' in entry and not isinstance(entry['risk_alleles'], list):
        errors.append(f"{rsid}: 'risk_alleles' must be a list")
    
    # Validate recommendations is a list
    if 'recommendations' in entry and not isinstance(entry['recommendations'], list):
        errors.append(f"{rsid}: 'recommendations' must be a list")
    
    return errors


def validate_json(json_path):
    """Validate JSON database."""
    print(f"Validating JSON: {json_path}")
    errors = []
    
    try:
        with open(json_path, 'r') as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        return [f"Invalid JSON: {e}"]
    except FileNotFoundError:
        return [f"File not found: {json_path}"]
    
    # Validate metadata
    errors.extend(validate_json_metadata(data))
    
    # Validate entries
    entry_count = 0
    for key, value in data.items():
        if key == 'metadata':
            continue
        
        if not key.startswith('rs'):
            errors.append(f"Invalid rsID format: {key}")
        
        errors.extend(validate_json_entry(key, value))
        entry_count += 1
    
    print(f"  Found {entry_count} SNP entries")
    
    return errors


def validate_csv(csv_path):
    """Validate CSV database."""
    print(f"Validating CSV: {csv_path}")
    errors = []
    
    required_columns = ['rsid', 'gene', 'description', 'risk_alleles', 
                       'recommendations', 'category', 'source', 
                       'provenance_version', 'provenance_citation']
    
    try:
        with open(csv_path, 'r') as f:
            reader = csv.DictReader(f)
            
            # Check headers
            if reader.fieldnames is None:
                return ["CSV file is empty or malformed"]
            
            missing_cols = set(required_columns) - set(reader.fieldnames)
            if missing_cols:
                errors.append(f"Missing required columns: {missing_cols}")
            
            # Validate entries
            entry_count = 0
            for row_num, row in enumerate(reader, start=2):
                rsid = row.get('rsid', '')
                
                if not rsid.startswith('rs'):
                    errors.append(f"Row {row_num}: Invalid rsID format: {rsid}")
                
                # Check required fields are not empty (except recommendations which can be empty)
                for col in required_columns:
                    if col == 'recommendations':
                        continue  # Recommendations can be empty
                    if col in row and not row[col]:
                        errors.append(f"Row {row_num} ({rsid}): Empty field '{col}'")
                
                # Check provenance fields
                if not row.get('provenance_version'):
                    errors.append(f"Row {row_num} ({rsid}): Missing provenance version")
                if not row.get('provenance_citation'):
                    errors.append(f"Row {row_num} ({rsid}): Missing provenance citation")
                
                entry_count += 1
            
            print(f"  Found {entry_count} SNP entries")
    
    except FileNotFoundError:
        return [f"File not found: {csv_path}"]
    except Exception as e:
        return [f"Error reading CSV: {e}"]
    
    return errors


def validate_consistency(json_path, csv_path):
    """Validate consistency between JSON and CSV."""
    print("Validating JSON-CSV consistency...")
    errors = []
    
    try:
        # Load JSON
        with open(json_path, 'r') as f:
            json_data = json.load(f)
        
        json_rsids = set(k for k in json_data.keys() if k != 'metadata')
        
        # Load CSV
        with open(csv_path, 'r') as f:
            reader = csv.DictReader(f)
            csv_rsids = set(row['rsid'] for row in reader)
        
        # Check consistency
        only_in_json = json_rsids - csv_rsids
        only_in_csv = csv_rsids - json_rsids
        
        if only_in_json:
            errors.append(f"RSIDs only in JSON: {only_in_json}")
        if only_in_csv:
            errors.append(f"RSIDs only in CSV: {only_in_csv}")
        
        if not errors:
            print(f"  {len(json_rsids)} entries consistent across JSON and CSV")
    
    except Exception as e:
        errors.append(f"Error checking consistency: {e}")
    
    return errors


def main():
    """Main validation function."""
    if len(sys.argv) < 2:
        print("Usage: python validate_snp_db.py <json_file> [csv_file]")
        print("  If csv_file is omitted, consistency check is skipped")
        sys.exit(1)
    
    json_path = Path(sys.argv[1])
    csv_path = Path(sys.argv[2]) if len(sys.argv) > 2 else None
    
    all_errors = []
    
    # Validate JSON
    all_errors.extend(validate_json(json_path))
    
    # Validate CSV if provided
    if csv_path:
        all_errors.extend(validate_csv(csv_path))
        
        # Check consistency
        if json_path.exists() and csv_path.exists():
            all_errors.extend(validate_consistency(json_path, csv_path))
    
    # Report results
    print("\n" + "="*50)
    if all_errors:
        print(f"VALIDATION FAILED - {len(all_errors)} error(s):")
        for error in all_errors:
            print(f"  ❌ {error}")
        sys.exit(1)
    else:
        print("✅ VALIDATION PASSED - All checks successful!")
        sys.exit(0)


if __name__ == '__main__':
    main()
