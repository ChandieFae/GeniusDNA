"""
GeniusDNA VCF Parser with Multi-Sample Support

Parses VCF files with support for:
- Multi-sample VCF files
- Phased and unphased genotypes
- Sample-aware analysis
"""

from pathlib import Path
from typing import Dict, List, Optional, Tuple


class VCFParser:
    """Parse VCF files with multi-sample and phasing support."""
    
    def __init__(self, vcf_path: Optional[Path] = None):
        """Initialize VCF parser."""
        self.vcf_path = vcf_path
        self.samples = []
        self.variants = []
        
        if vcf_path and vcf_path.exists():
            self.parse_file(vcf_path)
    
    def parse_file(self, vcf_path: Path):
        """Parse VCF file."""
        self.vcf_path = vcf_path
        self.samples = []
        self.variants = []
        
        with open(vcf_path, 'r') as f:
            for line in f:
                line = line.strip()
                
                if line.startswith('##'):
                    continue  # Skip meta-information
                elif line.startswith('#CHROM'):
                    self._parse_header(line)
                elif line and not line.startswith('#'):
                    self._parse_variant(line)
    
    def _parse_header(self, line: str):
        """Parse header line to extract sample names."""
        parts = line.split('\t')
        if len(parts) > 9:
            self.samples = parts[9:]
    
    def _parse_variant(self, line: str):
        """Parse variant line."""
        parts = line.split('\t')
        if len(parts) < 8:
            return
        
        chrom = parts[0]
        pos = int(parts[1])
        rsid = parts[2] if parts[2] != '.' else None
        ref = parts[3]
        alt = parts[4].split(',')
        qual = parts[5]
        filter_field = parts[6]
        info = parts[7]
        
        # Parse genotypes
        format_field = parts[8] if len(parts) > 8 else ''
        genotypes = {}
        
        if len(parts) > 9 and format_field:
            format_keys = format_field.split(':')
            for i, sample_name in enumerate(self.samples):
                if 9 + i < len(parts):
                    sample_data = parts[9 + i]
                    genotypes[sample_name] = self._parse_genotype(sample_data, format_keys)
        
        variant = {
            'chrom': chrom,
            'pos': pos,
            'rsid': rsid,
            'ref': ref,
            'alt': alt,
            'qual': qual,
            'filter': filter_field,
            'info': info,
            'genotypes': genotypes
        }
        
        self.variants.append(variant)
    
    def _parse_genotype(self, sample_data: str, format_keys: List[str]) -> Dict:
        """Parse genotype data for a sample."""
        values = sample_data.split(':')
        result = {}
        
        for key, value in zip(format_keys, values):
            if key == 'GT':
                result['GT'] = value
                
                # Determine if phased
                result['phased'] = '|' in value
                
                # Extract alleles
                if '|' in value:
                    alleles = value.split('|')
                elif '/' in value:
                    alleles = value.split('/')
                else:
                    alleles = [value]
                
                # Convert to integers, handle missing data (.)
                result['alleles'] = []
                for a in alleles:
                    if a == '.':
                        result['alleles'].append(None)
                    elif a.isdigit():
                        result['alleles'].append(int(a))
                    else:
                        result['alleles'].append(None)
            else:
                result[key] = value
        
        return result
    
    def get_sample_genotype(self, rsid: str, sample_name: str) -> Optional[Dict]:
        """Get genotype for a specific sample at a variant."""
        for variant in self.variants:
            if variant['rsid'] == rsid:
                return variant['genotypes'].get(sample_name)
        return None
    
    def get_variant(self, rsid: str) -> Optional[Dict]:
        """Get variant by rsID."""
        for variant in self.variants:
            if variant['rsid'] == rsid:
                return variant
        return None
    
    def get_all_samples(self) -> List[str]:
        """Get list of all sample names."""
        return self.samples
    
    def is_phased(self, rsid: str, sample_name: str) -> bool:
        """Check if a genotype is phased."""
        gt = self.get_sample_genotype(rsid, sample_name)
        return gt.get('phased', False) if gt else False
    
    def has_risk_allele(self, rsid: str, sample_name: str, risk_allele_idx: int = 1) -> Tuple[bool, int]:
        """
        Check if sample has risk allele.
        
        Returns:
            (has_risk, count) where count is 0, 1, or 2
        """
        gt = self.get_sample_genotype(rsid, sample_name)
        if not gt or 'alleles' not in gt:
            return False, 0
        
        alleles = gt['alleles']
        count = sum(1 for a in alleles if a == risk_allele_idx)
        
        return count > 0, count
    
    def get_sample_variants(self, sample_name: str) -> List[Dict]:
        """Get all variants for a specific sample."""
        if sample_name not in self.samples:
            return []
        
        sample_variants = []
        for variant in self.variants:
            if sample_name in variant['genotypes']:
                variant_copy = variant.copy()
                variant_copy['genotype'] = variant['genotypes'][sample_name]
                sample_variants.append(variant_copy)
        
        return sample_variants


def main():
    """Example usage."""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python genius_dna.py <vcf_file> [sample_name]")
        sys.exit(1)
    
    vcf_path = Path(sys.argv[1])
    sample_name = sys.argv[2] if len(sys.argv) > 2 else None
    
    parser = VCFParser(vcf_path)
    
    print(f"Parsed VCF: {vcf_path}")
    print(f"Samples: {', '.join(parser.get_all_samples())}")
    print(f"Variants: {len(parser.variants)}")
    
    if sample_name:
        print(f"\nVariants for {sample_name}:")
        for variant in parser.get_sample_variants(sample_name):
            rsid = variant['rsid'] or f"{variant['chrom']}:{variant['pos']}"
            gt = variant['genotype']
            phased = "phased" if gt.get('phased') else "unphased"
            print(f"  {rsid}: {gt['GT']} ({phased})")


if __name__ == '__main__':
    main()
