from typing import List, Tuple, Dict
from ..models import SNP, HealthCategory, AnalysisResult, DNAFile
from ..data.snp_database import SNPDatabase
import uuid


class SNPAnalyzer:
    """Analyzer for detecting and evaluating health-related SNPs"""
    
    def __init__(self):
        self.snp_db = SNPDatabase()
    
    def analyze_snps(
        self, 
        parsed_snps: List[Tuple[str, str, int, str]], 
        dna_file: DNAFile
    ) -> AnalysisResult:
        """
        Analyze parsed SNPs for health implications
        
        Args:
            parsed_snps: List of tuples (rsid, chromosome, position, genotype)
            dna_file: DNA file metadata
            
        Returns:
            AnalysisResult with analyzed SNPs and summary
        """
        analyzed_snps = []
        category_counts = {category: 0 for category in HealthCategory}
        
        for rsid, chromosome, position, genotype in parsed_snps:
            # Check if this SNP is in our health database
            if self.snp_db.is_known_snp(rsid):
                snp_info = self.snp_db.get_snp_info(rsid)
                if snp_info:
                    gene, category, _, description, recommendations = snp_info
                    risk_level = self.snp_db.assess_risk(rsid, genotype)
                    
                    snp = SNP(
                        rsid=rsid,
                        chromosome=chromosome,
                        position=position,
                        genotype=genotype,
                        gene=gene,
                        category=category,
                        risk_level=risk_level,
                        description=description,
                        recommendations=recommendations
                    )
                    
                    analyzed_snps.append(snp)
                    category_counts[category] += 1
        
        # Create analysis result
        analysis_result = AnalysisResult(
            analysis_id=str(uuid.uuid4()),
            dna_file=dna_file,
            analyzed_snps=analyzed_snps,
            category_summary=category_counts
        )
        
        return analysis_result
    
    def get_snps_by_category(
        self, 
        analysis_result: AnalysisResult, 
        category: HealthCategory
    ) -> List[SNP]:
        """
        Get all SNPs from analysis result for a specific category
        
        Args:
            analysis_result: Analysis result to filter
            category: Health category to filter by
            
        Returns:
            List of SNPs in the specified category
        """
        return [snp for snp in analysis_result.analyzed_snps if snp.category == category]
    
    def get_high_priority_snps(self, analysis_result: AnalysisResult) -> List[SNP]:
        """
        Get SNPs that require high priority attention
        
        Args:
            analysis_result: Analysis result to filter
            
        Returns:
            List of high-risk SNPs
        """
        from ..models import RiskLevel
        return [
            snp for snp in analysis_result.analyzed_snps 
            if snp.risk_level == RiskLevel.HIGH
        ]
