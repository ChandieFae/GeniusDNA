#!/usr/bin/env python3
"""
CLI tool to load, convert, and validate SNP database.

Features:
- Convert CSV to JSON
- Validate database integrity
- Support versioning
- Update metadata
"""

import json
import csv
import sys
import argparse
from pathlib import Path
from datetime import datetime


def csv_to_json(csv_path, json_path, version=None, generated_by="load_snp_db.py"):
    """Convert CSV to JSON format."""
    print(f"Converting {csv_path} to {json_path}...")
    
    # Read CSV
    entries = {}
    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        
        for row in reader:
            rsid = row['rsid']
            
            # Parse risk alleles and recommendations
            risk_alleles = row['risk_alleles'].split(',') if row['risk_alleles'] else []
            recommendations = row['recommendations'].split(' | ') if row['recommendations'] else []
            
            entries[rsid] = {
                'gene': row['gene'],
                'description': row['description'],
                'risk_alleles': risk_alleles,
                'recommendations': recommendations,
                'category': row['category'],
                'source': row['source'],
                'provenance': {
                    'version': row['provenance_version'],
                    'citation': row['provenance_citation']
                }
            }
    
    # Create JSON structure with metadata
    db_version = version or "0.2.0"
    json_data = {
        'metadata': {
            'version': db_version,
            'generated_by': generated_by,
            'citation': 'Mixed curation from dbSNP, ClinVar, PharmGKB, GWAS Catalog, SNPedia; see individual entries for source.',
            'notes': 'This database is for development and testing. Do NOT use for clinical decisions. Validate and cite primary literature before production use.'
        }
    }
    json_data.update(entries)
    
    # Write JSON
    with open(json_path, 'w') as f:
        json.dump(json_data, f, indent=2)
    
    print(f"✅ Converted {len(entries)} entries to JSON")
    return len(entries)


def json_to_csv(json_path, csv_path):
    """Convert JSON to CSV format."""
    print(f"Converting {json_path} to {csv_path}...")
    
    # Read JSON
    with open(json_path, 'r') as f:
        data = json.load(f)
    
    # Extract entries (skip metadata)
    csv_data = []
    for rsid, entry in data.items():
        if rsid == 'metadata':
            continue
        
        row = {
            'rsid': rsid,
            'gene': entry.get('gene', ''),
            'description': entry.get('description', ''),
            'risk_alleles': ','.join(entry.get('risk_alleles', [])),
            'recommendations': ' | '.join(entry.get('recommendations', [])),
            'category': entry.get('category', ''),
            'source': entry.get('source', ''),
            'provenance_version': entry.get('provenance', {}).get('version', ''),
            'provenance_citation': entry.get('provenance', {}).get('citation', '')
        }
        csv_data.append(row)
    
    # Write CSV
    with open(csv_path, 'w', newline='') as f:
        fieldnames = ['rsid', 'gene', 'description', 'risk_alleles', 'recommendations',
                     'category', 'source', 'provenance_version', 'provenance_citation']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(csv_data)
    
    print(f"✅ Converted {len(csv_data)} entries to CSV")
    return len(csv_data)


def validate_db(json_path, csv_path=None):
    """Run validation on database files."""
    import subprocess
    
    validator_script = Path(__file__).parent.parent / 'tools' / 'validate_snp_db.py'
    
    if not validator_script.exists():
        print(f"❌ Validator script not found: {validator_script}")
        return False
    
    cmd = [sys.executable, str(validator_script), str(json_path)]
    if csv_path:
        cmd.append(str(csv_path))
    
    result = subprocess.run(cmd)
    return result.returncode == 0


def update_version(json_path, new_version):
    """Update the version in JSON metadata."""
    print(f"Updating version to {new_version}...")
    
    with open(json_path, 'r') as f:
        data = json.load(f)
    
    if 'metadata' not in data:
        data['metadata'] = {}
    
    old_version = data['metadata'].get('version', 'unknown')
    data['metadata']['version'] = new_version
    data['metadata']['last_updated'] = datetime.now().isoformat()
    
    with open(json_path, 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"✅ Version updated: {old_version} → {new_version}")


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description='Load, convert, and validate SNP database',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Convert CSV to JSON
  python load_snp_db.py csv2json data/snp_database.csv data/snp_database.json

  # Convert JSON to CSV
  python load_snp_db.py json2csv data/snp_database.json data/snp_database.csv

  # Validate database
  python load_snp_db.py validate data/snp_database.json data/snp_database.csv

  # Update version
  python load_snp_db.py version data/snp_database.json 0.3.0
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Command to execute')
    
    # CSV to JSON
    csv2json_parser = subparsers.add_parser('csv2json', help='Convert CSV to JSON')
    csv2json_parser.add_argument('csv_file', type=Path, help='Input CSV file')
    csv2json_parser.add_argument('json_file', type=Path, help='Output JSON file')
    csv2json_parser.add_argument('--version', '-v', help='Database version')
    csv2json_parser.add_argument('--generated-by', default='load_snp_db.py', help='Generator name')
    
    # JSON to CSV
    json2csv_parser = subparsers.add_parser('json2csv', help='Convert JSON to CSV')
    json2csv_parser.add_argument('json_file', type=Path, help='Input JSON file')
    json2csv_parser.add_argument('csv_file', type=Path, help='Output CSV file')
    
    # Validate
    validate_parser = subparsers.add_parser('validate', help='Validate database')
    validate_parser.add_argument('json_file', type=Path, help='JSON file to validate')
    validate_parser.add_argument('csv_file', type=Path, nargs='?', help='CSV file to validate (optional)')
    
    # Update version
    version_parser = subparsers.add_parser('version', help='Update database version')
    version_parser.add_argument('json_file', type=Path, help='JSON file to update')
    version_parser.add_argument('new_version', help='New version number')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    try:
        if args.command == 'csv2json':
            csv_to_json(args.csv_file, args.json_file, args.version, args.generated_by)
            print("\n✅ Conversion complete!")
        
        elif args.command == 'json2csv':
            json_to_csv(args.json_file, args.csv_file)
            print("\n✅ Conversion complete!")
        
        elif args.command == 'validate':
            success = validate_db(args.json_file, args.csv_file)
            if not success:
                sys.exit(1)
        
        elif args.command == 'version':
            update_version(args.json_file, args.new_version)
    
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
