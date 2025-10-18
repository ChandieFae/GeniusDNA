"""
Longevity Optimizer AI Protocol

Sample-aware analysis for personalized longevity recommendations
based on genetic variants across multiple samples.
"""

from typing import Dict, List, Optional
from pathlib import Path
import json


class LongevityOptimizer:
    """AI protocol for analyzing genetic data and providing longevity recommendations."""
    
    def __init__(self, snp_db_path: Optional[Path] = None):
        """Initialize with SNP database."""
        self.snp_db = {}
        self.metadata = {}
        
        if snp_db_path and snp_db_path.exists():
            self.load_snp_database(snp_db_path)
    
    def load_snp_database(self, db_path: Path):
        """Load SNP database from JSON file."""
        with open(db_path, 'r') as f:
            data = json.load(f)
        
        # Extract metadata
        self.metadata = data.get('metadata', {})
        
        # Load SNP entries
        self.snp_db = {k: v for k, v in data.items() if k != 'metadata'}
    
    def analyze_sample(self, sample_variants: List[Dict], sample_name: str) -> Dict:
        """
        Analyze genetic variants for a specific sample.
        
        Args:
            sample_variants: List of variants with genotype data for the sample
            sample_name: Name of the sample being analyzed
        
        Returns:
            Analysis results with recommendations
        """
        risk_variants = []
        recommendations = []
        categories = {}
        
        for variant in sample_variants:
            rsid = variant.get('rsid')
            if not rsid or rsid not in self.snp_db:
                continue
            
            snp_info = self.snp_db[rsid]
            genotype = variant.get('genotype', {})
            alleles = genotype.get('alleles', [])
            
            # Check if sample has risk alleles
            risk_alleles = snp_info.get('risk_alleles', [])
            has_risk = self._check_risk_alleles(alleles, risk_alleles, variant)
            
            if has_risk:
                risk_count = self._count_risk_alleles(alleles, risk_alleles, variant)
                
                risk_variants.append({
                    'rsid': rsid,
                    'gene': snp_info.get('gene'),
                    'description': snp_info.get('description'),
                    'category': snp_info.get('category'),
                    'risk_count': risk_count,
                    'genotype': genotype.get('GT'),
                    'phased': genotype.get('phased', False)
                })
                
                # Collect recommendations
                snp_recommendations = snp_info.get('recommendations', [])
                recommendations.extend(snp_recommendations)
                
                # Group by category
                category = snp_info.get('category', 'other')
                if category not in categories:
                    categories[category] = []
                categories[category].append(rsid)
        
        # Deduplicate recommendations
        recommendations = list(set(recommendations))
        
        return {
            'sample_name': sample_name,
            'total_variants_analyzed': len(sample_variants),
            'risk_variants_found': len(risk_variants),
            'risk_variants': risk_variants,
            'recommendations': recommendations,
            'categories': categories,
            'database_version': self.metadata.get('version', 'unknown')
        }
    
    def _check_risk_alleles(self, alleles: List, risk_alleles: List[str], variant: Dict) -> bool:
        """Check if sample has any risk alleles."""
        ref = variant.get('ref', '')
        alt_list = variant.get('alt', [])
        
        # Map allele indices to actual nucleotides
        for allele_idx in alleles:
            if allele_idx is None:
                continue
            
            if allele_idx == 0:
                allele_nt = ref
            elif allele_idx > 0 and allele_idx <= len(alt_list):
                allele_nt = alt_list[allele_idx - 1]
            else:
                continue
            
            if allele_nt in risk_alleles:
                return True
        
        return False
    
    def _count_risk_alleles(self, alleles: List, risk_alleles: List[str], variant: Dict) -> int:
        """Count how many risk alleles the sample has."""
        ref = variant.get('ref', '')
        alt_list = variant.get('alt', [])
        count = 0
        
        for allele_idx in alleles:
            if allele_idx is None:
                continue
            
            if allele_idx == 0:
                allele_nt = ref
            elif allele_idx > 0 and allele_idx <= len(alt_list):
                allele_nt = alt_list[allele_idx - 1]
            else:
                continue
            
            if allele_nt in risk_alleles:
                count += 1
        
        return count
    
    def compare_samples(self, analyses: List[Dict]) -> Dict:
        """
        Compare multiple sample analyses to identify differences.
        
        Args:
            analyses: List of analysis results from analyze_sample()
        
        Returns:
            Comparison summary
        """
        comparison = {
            'samples': [a['sample_name'] for a in analyses],
            'shared_risks': [],
            'unique_risks': {}
        }
        
        # Find shared risk variants
        all_risk_rsids = [set(v['rsid'] for v in a['risk_variants']) for a in analyses]
        
        if all_risk_rsids:
            shared = set.intersection(*all_risk_rsids) if len(all_risk_rsids) > 1 else set()
            comparison['shared_risks'] = list(shared)
            
            # Find unique risks for each sample
            for analysis in analyses:
                sample_name = analysis['sample_name']
                sample_risks = set(v['rsid'] for v in analysis['risk_variants'])
                unique = sample_risks - shared
                comparison['unique_risks'][sample_name] = list(unique)
        
        return comparison
    
    def generate_report(self, analysis: Dict) -> str:
        """Generate a human-readable report from analysis results."""
        lines = []
        lines.append("="*60)
        lines.append(f"Longevity Optimization Report for {analysis['sample_name']}")
        lines.append("="*60)
        lines.append(f"Database Version: {analysis['database_version']}")
        lines.append(f"Variants Analyzed: {analysis['total_variants_analyzed']}")
        lines.append(f"Risk Variants Found: {analysis['risk_variants_found']}")
        lines.append("")
        
        if analysis['risk_variants']:
            lines.append("Risk Variants by Category:")
            for category, rsids in analysis['categories'].items():
                lines.append(f"\n  {category.upper()} ({len(rsids)} variants):")
                for rsid in rsids:
                    # Find variant details
                    for rv in analysis['risk_variants']:
                        if rv['rsid'] == rsid:
                            lines.append(f"    - {rsid} ({rv['gene']}): {rv['genotype']}")
                            break
            
            lines.append("\n" + "="*60)
            lines.append("RECOMMENDATIONS:")
            lines.append("="*60)
            for i, rec in enumerate(analysis['recommendations'], 1):
                lines.append(f"{i}. {rec}")
        else:
            lines.append("No risk variants found in analyzed data.")
        
        lines.append("\n" + "="*60)
        lines.append("DISCLAIMER: This analysis is for research and development only.")
        lines.append("Do NOT use for clinical decisions. Consult healthcare professionals.")
        lines.append("="*60)
        
        return "\n".join(lines)


def main():
    """Example usage."""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python longevity_optimizer.py <snp_database.json>")
        sys.exit(1)
    
    db_path = Path(sys.argv[1])
    
    optimizer = LongevityOptimizer(db_path)
    print(f"Loaded SNP database version {optimizer.metadata.get('version')}")
    print(f"Database contains {len(optimizer.snp_db)} SNPs")


if __name__ == '__main__':
    main()
