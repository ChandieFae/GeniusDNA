from typing import Dict, List, Tuple, Optional
from ..models import HealthCategory, RiskLevel


class SNPDatabase:
    """Database of known health-related SNPs"""
    
    # SNP database structure: rsid -> (gene, category, risk_genotypes, description, recommendations)
    SNP_DATA: Dict[str, Tuple[str, HealthCategory, Dict[str, RiskLevel], str, List[str]]] = {
        # LONGEVITY MARKERS
        "rs7412": (
            "APOE",
            HealthCategory.LONGEVITY,
            {"CC": RiskLevel.PROTECTIVE, "CT": RiskLevel.LOW, "TT": RiskLevel.MODERATE},
            "APOE ε2 allele associated with reduced Alzheimer's risk and increased longevity",
            [
                "Maintain heart-healthy diet rich in omega-3 fatty acids",
                "Regular cardiovascular exercise",
                "Monitor cholesterol levels regularly"
            ]
        ),
        "rs429358": (
            "APOE",
            HealthCategory.LONGEVITY,
            {"CC": RiskLevel.LOW, "CT": RiskLevel.MODERATE, "TT": RiskLevel.HIGH},
            "APOE ε4 allele associated with increased Alzheimer's risk",
            [
                "Consider Mediterranean diet",
                "Engage in cognitive training exercises",
                "Prioritize quality sleep and stress management",
                "Regular physical exercise, especially aerobic"
            ]
        ),
        "rs2802292": (
            "FOXO3",
            HealthCategory.LONGEVITY,
            {"GG": RiskLevel.PROTECTIVE, "GT": RiskLevel.LOW, "TT": RiskLevel.MODERATE},
            "FOXO3 gene variant associated with exceptional longevity",
            [
                "Practice intermittent fasting or caloric restriction",
                "Include antioxidant-rich foods in diet",
                "Regular moderate exercise"
            ]
        ),
        
        # DETOX MARKERS
        "rs1065852": (
            "CYP1A2",
            HealthCategory.DETOX,
            {"AA": RiskLevel.LOW, "AC": RiskLevel.MODERATE, "CC": RiskLevel.HIGH},
            "Caffeine metabolism - slow metabolizers have increased cardiovascular risk with high caffeine intake",
            [
                "Moderate caffeine intake if slow metabolizer",
                "Avoid caffeine in late afternoon/evening",
                "Stay hydrated"
            ]
        ),
        "rs1801280": (
            "NAT2",
            HealthCategory.DETOX,
            {"TT": RiskLevel.LOW, "TC": RiskLevel.MODERATE, "CC": RiskLevel.HIGH},
            "Acetylation capacity affecting drug and toxin metabolism",
            [
                "Be cautious with medications requiring acetylation",
                "Support liver health with cruciferous vegetables",
                "Consider N-acetylcysteine supplementation"
            ]
        ),
        "rs1695": (
            "GSTP1",
            HealthCategory.DETOX,
            {"AA": RiskLevel.LOW, "AG": RiskLevel.MODERATE, "GG": RiskLevel.HIGH},
            "Glutathione S-transferase enzyme affecting detoxification capacity",
            [
                "Support glutathione production with sulfur-rich foods",
                "Consider glutathione or NAC supplementation",
                "Minimize exposure to environmental toxins"
            ]
        ),
        
        # METABOLISM MARKERS
        "rs9939609": (
            "FTO",
            HealthCategory.METABOLISM,
            {"TT": RiskLevel.LOW, "TA": RiskLevel.MODERATE, "AA": RiskLevel.HIGH},
            "Fat mass and obesity-associated gene affecting body weight regulation",
            [
                "Focus on portion control and mindful eating",
                "Prioritize protein-rich breakfast",
                "Regular physical activity, especially HIIT",
                "Avoid high-fat, high-sugar processed foods"
            ]
        ),
        "rs1801282": (
            "PPARG",
            HealthCategory.METABOLISM,
            {"CC": RiskLevel.MODERATE, "CG": RiskLevel.LOW, "GG": RiskLevel.PROTECTIVE},
            "PPAR-gamma affecting insulin sensitivity and fat metabolism",
            [
                "Focus on complex carbohydrates over simple sugars",
                "Include healthy fats (omega-3s, nuts, avocado)",
                "Regular exercise to improve insulin sensitivity"
            ]
        ),
        "rs17782313": (
            "MC4R",
            HealthCategory.METABOLISM,
            {"TT": RiskLevel.LOW, "TC": RiskLevel.MODERATE, "CC": RiskLevel.HIGH},
            "Melanocortin 4 receptor affecting appetite and energy balance",
            [
                "Practice mindful eating and hunger awareness",
                "Regular meal timing to regulate appetite",
                "High-protein, high-fiber diet for satiety"
            ]
        ),
        
        # SKIN AGING MARKERS
        "rs1800012": (
            "COL1A1",
            HealthCategory.SKIN_AGING,
            {"GG": RiskLevel.LOW, "GT": RiskLevel.MODERATE, "TT": RiskLevel.HIGH},
            "Collagen type I production affecting skin elasticity and aging",
            [
                "Increase vitamin C intake for collagen synthesis",
                "Consider collagen peptide supplementation",
                "Protect skin from UV damage with SPF",
                "Stay well-hydrated"
            ]
        ),
        "rs1799750": (
            "MMP1",
            HealthCategory.SKIN_AGING,
            {"GG": RiskLevel.LOW, "G-": RiskLevel.MODERATE, "--": RiskLevel.HIGH},
            "Matrix metalloproteinase affecting collagen breakdown",
            [
                "Use antioxidant-rich skincare (vitamin C, E)",
                "Minimize sun exposure and always use SPF 30+",
                "Include foods rich in vitamin A and beta-carotene",
                "Consider retinoid treatments"
            ]
        ),
        "rs4880": (
            "SOD2",
            HealthCategory.SKIN_AGING,
            {"CC": RiskLevel.PROTECTIVE, "CT": RiskLevel.LOW, "TT": RiskLevel.MODERATE},
            "Superoxide dismutase affecting antioxidant defense in skin",
            [
                "Increase intake of antioxidant-rich foods",
                "Consider vitamin E and selenium supplementation",
                "Minimize oxidative stress from pollution and smoking"
            ]
        ),
        
        # BRAIN HEALTH MARKERS
        "rs6265": (
            "BDNF",
            HealthCategory.BRAIN_HEALTH,
            {"CC": RiskLevel.LOW, "CT": RiskLevel.MODERATE, "TT": RiskLevel.HIGH},
            "Brain-derived neurotrophic factor affecting neuroplasticity and memory",
            [
                "Regular aerobic exercise to boost BDNF",
                "Engage in learning and cognitive challenges",
                "Ensure adequate sleep (7-9 hours)",
                "Consider omega-3 supplementation"
            ]
        ),
        "rs4680": (
            "COMT",
            HealthCategory.BRAIN_HEALTH,
            {"GG": RiskLevel.LOW, "GA": RiskLevel.MODERATE, "AA": RiskLevel.HIGH},
            "Catechol-O-methyltransferase affecting dopamine metabolism and stress response",
            [
                "Practice stress management techniques",
                "Ensure adequate magnesium and B-vitamin intake",
                "Optimize sleep quality",
                "Consider adaptogens for stress resilience"
            ]
        ),
    }
    
    @classmethod
    def get_snp_info(cls, rsid: str) -> Optional[Tuple[str, HealthCategory, Dict[str, RiskLevel], str, List[str]]]:
        """Get information for a specific SNP"""
        return cls.SNP_DATA.get(rsid)
    
    @classmethod
    def is_known_snp(cls, rsid: str) -> bool:
        """Check if SNP is in database"""
        return rsid in cls.SNP_DATA
    
    @classmethod
    def get_snps_by_category(cls, category: HealthCategory) -> List[str]:
        """Get all SNPs for a specific health category"""
        return [rsid for rsid, (_, cat, _, _, _) in cls.SNP_DATA.items() if cat == category]
    
    @classmethod
    def assess_risk(cls, rsid: str, genotype: str) -> RiskLevel:
        """Assess risk level for a given SNP and genotype"""
        snp_info = cls.get_snp_info(rsid)
        if snp_info is None:
            return RiskLevel.LOW
        
        _, _, risk_genotypes, _, _ = snp_info
        
        # Check exact match
        if genotype in risk_genotypes:
            return risk_genotypes[genotype]
        
        # Check reverse genotype (e.g., AG vs GA)
        reverse_genotype = genotype[::-1]
        if reverse_genotype in risk_genotypes:
            return risk_genotypes[reverse_genotype]
        
        # Default to low risk if genotype not found
        return RiskLevel.LOW


__all__ = ["SNPDatabase"]
