#!/usr/bin/env python3
"""
GeniusDNA AI Longevity Engine

This module analyzes raw DNA text data (23andMe format or VCF) and detects relevant SNPs
that map to health traits like detox, methylation, vitamin D synthesis, fat metabolism,
mitochondrial function, cognitive traits, and aging. Based on the presence of key SNPs,
it generates personalized longevity protocols and recommendations.
"""

import csv
import re
from typing import Dict, List, Tuple, Set
from dataclasses import dataclass
from enum import Enum


class Genotype(Enum):
    """Genotype classifications"""
    HOMOZYGOUS_NORMAL = "normal"
    HETEROZYGOUS = "carrier"
    HOMOZYGOUS_VARIANT = "at_risk"


@dataclass
class SNP:
    """SNP (Single Nucleotide Polymorphism) data structure"""
    rsid: str
    chromosome: str
    position: str
    genotype: str
    
    
@dataclass
class SNPInfo:
    """Information about a specific SNP and its health implications"""
    rsid: str
    gene: str
    trait: str
    risk_allele: str
    normal_allele: str
    description: str
    recommendations: List[str]


class SNPDatabase:
    """Database of known SNPs and their health implications"""
    
    def __init__(self):
        self.snps = self._initialize_snp_database()
    
    def _initialize_snp_database(self) -> Dict[str, SNPInfo]:
        """Initialize comprehensive SNP database with health implications"""
        snps = {}
        
        # DETOX-RELATED SNPs
        snps['rs1695'] = SNPInfo(
            rsid='rs1695',
            gene='GSTP1',
            trait='Detoxification',
            risk_allele='G',
            normal_allele='A',
            description='Affects phase II detoxification and glutathione conjugation. The G allele (Val105) has reduced activity.',
            recommendations=[
                'Increase glutathione precursors (NAC, glycine, glutamine)',
                'Support with cruciferous vegetables (broccoli, Brussels sprouts)',
                'Consider milk thistle supplementation',
                'Minimize exposure to environmental toxins'
            ]
        )
        
        snps['rs1065852'] = SNPInfo(
            rsid='rs1065852',
            gene='CYP2D6',
            trait='Drug Metabolism',
            risk_allele='T',
            normal_allele='C',
            description='Affects metabolism of many medications. Variant affects drug clearance rates.',
            recommendations=[
                'Consult healthcare provider about medication dosing',
                'Be cautious with codeine and similar medications',
                'Monitor liver function regularly',
                'Support liver health with B vitamins'
            ]
        )
        
        snps['rs762551'] = SNPInfo(
            rsid='rs762551',
            gene='CYP1A2',
            trait='Caffeine Metabolism',
            risk_allele='C',
            normal_allele='A',
            description='Slow caffeine metabolizer. C allele carriers metabolize caffeine slowly, increasing cardiovascular risk with high intake.',
            recommendations=[
                'Limit caffeine intake to <200mg/day if CC genotype',
                'Avoid caffeine after 2pm for better sleep',
                'Consider switching to green tea for antioxidants',
                'Monitor heart rate and blood pressure with caffeine use'
            ]
        )
        
        snps['rs366631'] = SNPInfo(
            rsid='rs366631',
            gene='GSTM1',
            trait='Glutathione Detoxification',
            risk_allele='deletion',
            normal_allele='present',
            description='GSTM1 deletion common in population. Null genotype reduces capacity to neutralize toxins and oxidative stress.',
            recommendations=[
                'Increase antioxidant intake (vitamin C, E, selenium)',
                'Supplement with NAC (N-acetyl cysteine) 600-1200mg/day',
                'Eat sulfur-rich foods (garlic, onions, cruciferous vegetables)',
                'Limit exposure to cigarette smoke and air pollution'
            ]
        )
        
        snps['rs4646436'] = SNPInfo(
            rsid='rs4646436',
            gene='CYP1A1',
            trait='Phase I Detoxification',
            risk_allele='C',
            normal_allele='T',
            description='Affects activation and detoxification of polycyclic aromatic hydrocarbons (PAHs).',
            recommendations=[
                'Avoid charred or smoked meats',
                'Increase intake of detox-supporting vegetables',
                'Support with DIM or I3C supplements',
                'Regular sauna use for toxin elimination'
            ]
        )
        
        # Add GSTT1 for additional glutathione detox coverage
        snps['rs4630'] = SNPInfo(
            rsid='rs4630',
            gene='GSTT1',
            trait='Glutathione Detoxification',
            risk_allele='deletion',
            normal_allele='present',
            description='GSTT1 deletion affects phase II detoxification. Null genotype impairs ability to detoxify certain environmental toxins.',
            recommendations=[
                'Support glutathione production with NAC',
                'Increase cruciferous vegetable intake',
                'Avoid exposure to organic solvents and pesticides',
                'Support liver function with milk thistle'
            ]
        )
        
        # METHYLATION SNPs
        snps['rs1801133'] = SNPInfo(
            rsid='rs1801133',
            gene='MTHFR',
            trait='Methylation',
            risk_allele='T',
            normal_allele='C',
            description='C677T variant reduces MTHFR enzyme activity by 30-70%. Affects folate metabolism and homocysteine levels.',
            recommendations=[
                'Take methylfolate (5-MTHF) instead of folic acid',
                'Supplement with methylcobalamin (B12) 1000mcg daily',
                'Include B6 (P5P form) 50mg daily',
                'Monitor homocysteine levels (keep <8 µmol/L)',
                'Eat folate-rich foods (leafy greens, legumes)'
            ]
        )
        
        snps['rs1801131'] = SNPInfo(
            rsid='rs1801131',
            gene='MTHFR',
            trait='Methylation',
            risk_allele='C',
            normal_allele='A',
            description='A1298C variant affects MTHFR enzyme activity. Combined with C677T, can significantly impact methylation.',
            recommendations=[
                'Support methylation with B-complex including methylated forms',
                'Consider TMG (trimethylglycine) supplementation',
                'Ensure adequate choline intake',
                'Monitor neurotransmitter levels'
            ]
        )
        
        snps['rs1801394'] = SNPInfo(
            rsid='rs1801394',
            gene='MTRR',
            trait='Methylation',
            risk_allele='G',
            normal_allele='A',
            description='Affects methionine synthase reductase, important for B12 recycling.',
            recommendations=[
                'Take high-dose methylcobalamin (B12)',
                'Support with methylfolate',
                'Consider adenosylcobalamin for mitochondrial function',
                'Monitor B12 levels regularly'
            ]
        )
        
        # VITAMIN D SYNTHESIS
        snps['rs2282679'] = SNPInfo(
            rsid='rs2282679',
            gene='GC',
            trait='Vitamin D Binding',
            risk_allele='C',
            normal_allele='T',
            description='Affects vitamin D binding protein levels and bioavailability.',
            recommendations=[
                'Monitor vitamin D levels (target 50-80 ng/mL)',
                'May require higher vitamin D3 supplementation (2000-5000 IU)',
                'Combine with vitamin K2 and magnesium',
                'Get regular sun exposure (15-20 min daily)'
            ]
        )
        
        snps['rs10741657'] = SNPInfo(
            rsid='rs10741657',
            gene='CYP2R1',
            trait='Vitamin D Synthesis',
            risk_allele='A',
            normal_allele='G',
            description='Affects conversion of vitamin D to 25-hydroxyvitamin D.',
            recommendations=[
                'Higher vitamin D3 supplementation may be needed',
                'Monitor 25-OH vitamin D levels regularly',
                'Ensure adequate sun exposure',
                'Support with magnesium for vitamin D activation'
            ]
        )
        
        # FAT METABOLISM
        snps['rs9939609'] = SNPInfo(
            rsid='rs9939609',
            gene='FTO',
            trait='Fat Mass and Obesity',
            risk_allele='A',
            normal_allele='T',
            description='Strongly associated with BMI and obesity risk. Affects appetite regulation.',
            recommendations=[
                'Focus on high-protein diet (30% of calories)',
                'Practice intermittent fasting',
                'Regular cardiovascular exercise (45+ min, 5x/week)',
                'Avoid high-glycemic foods',
                'Monitor portion sizes carefully'
            ]
        )
        
        snps['rs1801282'] = SNPInfo(
            rsid='rs1801282',
            gene='PPARG',
            trait='Fat Metabolism',
            risk_allele='G',
            normal_allele='C',
            description='Pro12Ala variant affects insulin sensitivity and fat storage.',
            recommendations=[
                'Emphasize monounsaturated fats (olive oil, avocados)',
                'Include omega-3 fatty acids',
                'Practice carbohydrate timing around exercise',
                'Consider berberine or metformin for insulin sensitivity'
            ]
        )
        
        # MITOCHONDRIAL FUNCTION
        snps['rs8192678'] = SNPInfo(
            rsid='rs8192678',
            gene='PPARGC1A',
            trait='Mitochondrial Biogenesis',
            risk_allele='T',
            normal_allele='C',
            description='PGC-1α Gly482Ser variant. Affects mitochondrial biogenesis and energy metabolism.',
            recommendations=[
                'High-intensity interval training (HIIT) 3x/week',
                'Support with CoQ10 (100-200mg ubiquinol)',
                'PQQ (pyrroloquinoline quinone) 20mg daily',
                'Alpha-lipoic acid 300-600mg daily',
                'Ensure adequate B-vitamins for energy metabolism'
            ]
        )
        
        snps['rs659366'] = SNPInfo(
            rsid='rs659366',
            gene='UCP2',
            trait='Mitochondrial Uncoupling',
            risk_allele='A',
            normal_allele='G',
            description='Affects mitochondrial uncoupling protein 2, impacting energy efficiency and ROS production.',
            recommendations=[
                'Support mitochondria with NAD+ precursors (NMN or NR)',
                'Antioxidant support (vitamin C, E, selenium)',
                'Magnesium supplementation for ATP production',
                'Consider cold exposure for mitochondrial adaptation',
                'Practice fasting to enhance mitochondrial efficiency'
            ]
        )
        
        # COGNITIVE TRAITS
        snps['rs4680'] = SNPInfo(
            rsid='rs4680',
            gene='COMT',
            trait='Dopamine Metabolism',
            risk_allele='A',
            normal_allele='G',
            description='Val158Met variant. Met (A) allele has slower COMT activity, affecting dopamine breakdown and stress response.',
            recommendations=[
                'Manage stress with meditation and mindfulness',
                'Avoid excessive caffeine if Met/Met (can increase anxiety)',
                'Support with magnesium and B6',
                'SAMe supplementation may help (400-800mg)',
                'Adaptogenic herbs (Rhodiola, Ashwagandha)'
            ]
        )
        
        snps['rs6265'] = SNPInfo(
            rsid='rs6265',
            gene='BDNF',
            trait='Neuroplasticity',
            risk_allele='A',
            normal_allele='G',
            description='Val66Met variant affects brain-derived neurotrophic factor. Impacts learning, memory, and neuroplasticity.',
            recommendations=[
                'Regular aerobic exercise (30+ min, 5x/week)',
                'Omega-3 supplementation (EPA/DHA 2g daily)',
                'Lion\'s Mane mushroom for NGF support',
                'Curcumin with black pepper for brain health',
                'Practice new skills and lifelong learning',
                'Ensure quality sleep (7-9 hours)'
            ]
        )
        
        snps['rs429358'] = SNPInfo(
            rsid='rs429358',
            gene='APOE',
            trait='Alzheimer\'s Risk',
            risk_allele='C',
            normal_allele='T',
            description='APOE ε4 variant (C allele). Major genetic risk factor for Alzheimer\'s disease and cardiovascular disease.',
            recommendations=[
                'Follow Mediterranean or ketogenic diet',
                'Aggressive cardiovascular disease prevention',
                'High-dose omega-3 (EPA/DHA 2-3g daily)',
                'Regular cognitive stimulation',
                'Optimize sleep and treat sleep apnea',
                'Control inflammation (monitor hsCRP)',
                'Consider MCT oil for ketone production',
                'Avoid head trauma and contact sports'
            ]
        )
        
        snps['rs7412'] = SNPInfo(
            rsid='rs7412',
            gene='APOE',
            trait='Alzheimer\'s Protection',
            risk_allele='T',
            normal_allele='C',
            description='APOE ε2 variant (T allele at rs7412). Associated with lower Alzheimer\'s risk but higher triglyceride levels.',
            recommendations=[
                'Monitor triglyceride and cholesterol levels',
                'Emphasize healthy fats (omega-3, monounsaturated)',
                'Regular cardiovascular exercise',
                'Maintain cognitive engagement'
            ]
        )
        
        # AGING AND LONGEVITY
        snps['rs2802292'] = SNPInfo(
            rsid='rs2802292',
            gene='FOXO3',
            trait='Longevity',
            risk_allele='T',
            normal_allele='G',
            description='Strongly associated with human longevity. G allele linked to extended lifespan.',
            recommendations=[
                'Practice caloric restriction or intermittent fasting',
                'Regular moderate exercise',
                'Stress management and meditation',
                'Support autophagy with resveratrol or spermidine',
                'Maintain lean body mass'
            ]
        )
        
        snps['rs1061170'] = SNPInfo(
            rsid='rs1061170',
            gene='CFH',
            trait='Inflammation and Aging',
            risk_allele='C',
            normal_allele='T',
            description='Affects complement factor H, involved in inflammation and age-related macular degeneration.',
            recommendations=[
                'Anti-inflammatory diet',
                'Lutein and zeaxanthin for eye health',
                'Omega-3 supplementation',
                'Monitor inflammatory markers',
                'Regular eye exams'
            ]
        )
        
        snps['rs1800450'] = SNPInfo(
            rsid='rs1800450',
            gene='SIRT1',
            trait='Cellular Aging',
            risk_allele='T',
            normal_allele='C',
            description='Affects sirtuin 1 activity, important for DNA repair and longevity.',
            recommendations=[
                'Resveratrol supplementation (250-500mg)',
                'NAD+ precursors (NMN 250-500mg or NR 300mg)',
                'Fasting and caloric restriction',
                'Regular exercise for SIRT1 activation',
                'Adequate sleep for DNA repair'
            ]
        )
        
        return snps
    
    def get_snp_info(self, rsid: str) -> SNPInfo:
        """Get information for a specific SNP"""
        return self.snps.get(rsid)
    
    def get_all_snps(self) -> Dict[str, SNPInfo]:
        """Get all SNPs in database"""
        return self.snps


class DNAParser:
    """Parser for DNA data files in various formats"""
    
    @staticmethod
    def parse_23andme(filepath: str) -> Dict[str, SNP]:
        """
        Parse 23andMe format DNA file
        Format: rsid, chromosome, position, genotype
        """
        snps = {}
        
        with open(filepath, 'r') as f:
            for line in f:
                line = line.strip()
                
                # Skip comments and header
                if line.startswith('#') or not line:
                    continue
                
                parts = line.split('\t')
                if len(parts) >= 4:
                    rsid, chromosome, position, genotype = parts[0], parts[1], parts[2], parts[3]
                    
                    # Only keep valid RSIDs
                    if rsid.startswith('rs'):
                        snps[rsid] = SNP(
                            rsid=rsid,
                            chromosome=chromosome,
                            position=position,
                            genotype=genotype
                        )
        
        return snps
    
    @staticmethod
    def parse_csv(filepath: str) -> Dict[str, SNP]:
        """
        Parse CSV format DNA file
        Expected columns: rsid, chromosome, position, genotype
        """
        snps = {}
        
        with open(filepath, 'r') as f:
            reader = csv.DictReader(f)
            
            for row in reader:
                rsid = row.get('rsid', '').strip()
                chromosome = row.get('chromosome', '').strip()
                position = row.get('position', '').strip()
                genotype = row.get('genotype', '').strip()
                
                if rsid.startswith('rs'):
                    snps[rsid] = SNP(
                        rsid=rsid,
                        chromosome=chromosome,
                        position=position,
                        genotype=genotype
                    )
        
        return snps
    
    @staticmethod
    def parse_vcf(filepath: str) -> Dict[str, SNP]:
        """
        Parse VCF (Variant Call Format) file
        """
        snps = {}
        
        with open(filepath, 'r') as f:
            for line in f:
                line = line.strip()
                
                # Skip headers
                if line.startswith('##'):
                    continue
                
                # Column header line
                if line.startswith('#CHROM'):
                    continue
                
                if not line:
                    continue
                
                parts = line.split('\t')
                if len(parts) >= 5:
                    chrom = parts[0]
                    pos = parts[1]
                    rsid = parts[2] if parts[2] != '.' else None
                    ref = parts[3]
                    alt = parts[4]
                    
                    # Extract genotype from FORMAT and sample columns
                    if len(parts) >= 10:
                        format_fields = parts[8].split(':')
                        sample_data = parts[9].split(':')
                        
                        # Find GT (genotype) field
                        if 'GT' in format_fields:
                            gt_index = format_fields.index('GT')
                            genotype_code = sample_data[gt_index]
                            
                            # Convert VCF genotype notation (0/0, 0/1, 1/1) to nucleotides
                            genotype = DNAParser._vcf_genotype_to_alleles(
                                genotype_code, ref, alt
                            )
                            
                            if rsid and rsid.startswith('rs'):
                                snps[rsid] = SNP(
                                    rsid=rsid,
                                    chromosome=chrom,
                                    position=pos,
                                    genotype=genotype
                                )
        
        return snps
    
    @staticmethod
    def _vcf_genotype_to_alleles(gt_code: str, ref: str, alt: str) -> str:
        """Convert VCF genotype code to allele string"""
        # Handle phased (|) and unphased (/) separators
        gt_code = gt_code.replace('|', '/')
        
        if '/' not in gt_code:
            return '--'
        
        alleles = []
        for allele_num in gt_code.split('/'):
            if allele_num == '.':
                alleles.append('-')
            elif allele_num == '0':
                alleles.append(ref)
            elif allele_num == '1':
                alleles.append(alt.split(',')[0])  # Take first ALT if multiple
            else:
                alleles.append('-')
        
        return ''.join(alleles)


class LongevityEngine:
    """Main engine for analyzing DNA and generating personalized recommendations"""
    
    def __init__(self):
        self.snp_database = SNPDatabase()
    
    def analyze_dna(self, dna_data: Dict[str, SNP]) -> Dict[str, any]:
        """
        Analyze DNA data and generate comprehensive report
        
        Args:
            dna_data: Dictionary of rsid -> SNP objects
        
        Returns:
            Dictionary containing analysis results and recommendations
        """
        results = {
            'detox': [],
            'methylation': [],
            'vitamin_d': [],
            'fat_metabolism': [],
            'mitochondrial': [],
            'cognitive': [],
            'aging': [],
            'summary': [],
            'priority_recommendations': []
        }
        
        risk_scores = {
            'detox': 0,
            'methylation': 0,
            'vitamin_d': 0,
            'fat_metabolism': 0,
            'mitochondrial': 0,
            'cognitive': 0,
            'aging': 0
        }
        
        # Analyze each SNP in the database
        for rsid, snp_info in self.snp_database.get_all_snps().items():
            if rsid in dna_data:
                user_snp = dna_data[rsid]
                genotype_analysis = self._analyze_genotype(user_snp, snp_info)
                
                # Categorize by trait
                category = self._categorize_trait(snp_info.trait)
                if category:
                    results[category].append({
                        'rsid': rsid,
                        'gene': snp_info.gene,
                        'genotype': user_snp.genotype,
                        'status': genotype_analysis['status'],
                        'description': snp_info.description,
                        'recommendations': snp_info.recommendations
                    })
                    
                    # Update risk scores
                    if genotype_analysis['status'] in ['carrier', 'at_risk']:
                        risk_scores[category] += genotype_analysis['risk_level']
        
        # Generate summary and priority recommendations
        results['summary'] = self._generate_summary(risk_scores)
        results['priority_recommendations'] = self._generate_priority_recommendations(results)
        
        return results
    
    def _analyze_genotype(self, snp: SNP, snp_info: SNPInfo) -> Dict[str, any]:
        """Analyze a specific genotype and determine risk level"""
        genotype = snp.genotype.upper()
        risk_allele = snp_info.risk_allele.upper()
        normal_allele = snp_info.normal_allele.upper()
        
        # Handle special cases
        if risk_allele == 'DELETION' or normal_allele == 'DELETION':
            return {
                'status': 'unknown',
                'risk_level': 0
            }
        
        # Count risk alleles
        risk_allele_count = genotype.count(risk_allele)
        
        if risk_allele_count == 0:
            return {
                'status': 'normal',
                'risk_level': 0
            }
        elif risk_allele_count == 1:
            return {
                'status': 'carrier',
                'risk_level': 1
            }
        else:
            return {
                'status': 'at_risk',
                'risk_level': 2
            }
    
    def _categorize_trait(self, trait: str) -> str:
        """Categorize a trait into main categories"""
        trait_lower = trait.lower()
        
        # Check cognitive first (more specific) to avoid 'metabolism' matching detox
        if any(term in trait_lower for term in ['cognitive', 'dopamine', 'neuroplasticity', 'alzheimer', 'brain']):
            return 'cognitive'
        elif 'methylation' in trait_lower:
            return 'methylation'
        elif 'vitamin d' in trait_lower:
            return 'vitamin_d'
        elif any(term in trait_lower for term in ['fat', 'obesity', 'weight']):
            return 'fat_metabolism'
        elif any(term in trait_lower for term in ['mitochondrial', 'energy', 'uncoupling', 'biogenesis']):
            return 'mitochondrial'
        elif any(term in trait_lower for term in ['detox', 'drug', 'caffeine', 'glutathione', 'phase']):
            return 'detox'
        elif any(term in trait_lower for term in ['aging', 'longevity', 'inflammation', 'cellular']):
            return 'aging'
        
        return None
    
    def _generate_summary(self, risk_scores: Dict[str, int]) -> List[str]:
        """Generate summary of analysis"""
        summary = []
        
        for category, score in risk_scores.items():
            if score == 0:
                level = "Low risk"
            elif score <= 3:
                level = "Moderate risk"
            else:
                level = "Higher risk"
            
            category_name = category.replace('_', ' ').title()
            summary.append(f"{category_name}: {level} (score: {score})")
        
        return summary
    
    def _generate_priority_recommendations(self, results: Dict) -> List[str]:
        """Generate prioritized list of top recommendations"""
        priority = []
        
        # Collect all at-risk SNPs
        at_risk_snps = []
        for category in ['detox', 'methylation', 'vitamin_d', 'fat_metabolism', 
                        'mitochondrial', 'cognitive', 'aging']:
            for snp_result in results[category]:
                if snp_result['status'] == 'at_risk':
                    at_risk_snps.append(snp_result)
        
        # Generate top recommendations
        if at_risk_snps:
            priority.append("=== HIGH PRIORITY GENETIC VARIANTS DETECTED ===\n")
            
            for snp in at_risk_snps:
                priority.append(f"\n{snp['gene']} ({snp['rsid']}): {snp['genotype']}")
                priority.append(f"Status: {snp['status'].upper()}")
                priority.append(f"Description: {snp['description']}")
                priority.append("\nRecommended Actions:")
                for rec in snp['recommendations']:
                    priority.append(f"  • {rec}")
        else:
            priority.append("Good news! No high-risk variants detected in analyzed genes.")
        
        return priority
    
    def generate_report(self, results: Dict) -> str:
        """Generate human-readable report"""
        report = []
        report.append("=" * 80)
        report.append("GENIUSDNA AI LONGEVITY ENGINE - GENETIC ANALYSIS REPORT")
        report.append("=" * 80)
        report.append("")
        
        # Summary section
        report.append("RISK SUMMARY")
        report.append("-" * 80)
        for item in results['summary']:
            report.append(item)
        report.append("")
        
        # Priority recommendations
        report.append("\nPRIORITY RECOMMENDATIONS")
        report.append("-" * 80)
        for item in results['priority_recommendations']:
            report.append(item)
        report.append("")
        
        # Detailed results by category
        categories = [
            ('detox', 'DETOXIFICATION GENES'),
            ('methylation', 'METHYLATION GENES'),
            ('vitamin_d', 'VITAMIN D METABOLISM'),
            ('fat_metabolism', 'FAT METABOLISM'),
            ('mitochondrial', 'MITOCHONDRIAL FUNCTION'),
            ('cognitive', 'COGNITIVE FUNCTION'),
            ('aging', 'AGING AND LONGEVITY')
        ]
        
        for category, title in categories:
            if results[category]:
                report.append(f"\n{title}")
                report.append("-" * 80)
                
                for snp in results[category]:
                    report.append(f"\n{snp['gene']} ({snp['rsid']})")
                    report.append(f"  Genotype: {snp['genotype']}")
                    report.append(f"  Status: {snp['status']}")
                    report.append(f"  Description: {snp['description']}")
                    
                    if snp['status'] in ['carrier', 'at_risk']:
                        report.append("  Recommendations:")
                        for rec in snp['recommendations']:
                            report.append(f"    • {rec}")
                    
                    report.append("")
        
        report.append("=" * 80)
        report.append("End of Report")
        report.append("=" * 80)
        
        return "\n".join(report)


def main():
    """Main function demonstrating usage"""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python genius_dna.py <dna_file>")
        print("Supported formats: 23andMe (.txt), CSV (.csv), VCF (.vcf)")
        sys.exit(1)
    
    filepath = sys.argv[1]
    
    # Determine file type and parse
    print(f"Loading DNA data from {filepath}...")
    
    if filepath.endswith('.vcf'):
        dna_data = DNAParser.parse_vcf(filepath)
    elif filepath.endswith('.csv'):
        dna_data = DNAParser.parse_csv(filepath)
    else:
        # Default to 23andMe format
        dna_data = DNAParser.parse_23andme(filepath)
    
    print(f"Loaded {len(dna_data)} SNPs from file")
    
    # Analyze DNA
    print("\nAnalyzing genetic variants...")
    engine = LongevityEngine()
    results = engine.analyze_dna(dna_data)
    
    # Generate and print report
    report = engine.generate_report(results)
    print("\n" + report)


if __name__ == "__main__":
    main()
