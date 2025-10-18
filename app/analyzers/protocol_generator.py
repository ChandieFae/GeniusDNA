from typing import List, Dict
from ..models import HealthProtocol, AnalysisResult, SNP, HealthCategory, RiskLevel
import uuid


class ProtocolGenerator:
    """AI-powered health protocol generator based on genetic analysis"""
    
    def generate_protocols(self, analysis_result: AnalysisResult) -> List[HealthProtocol]:
        """
        Generate personalized health protocols based on analysis results
        
        Args:
            analysis_result: DNA analysis result
            
        Returns:
            List of health protocols for each relevant category
        """
        protocols = []
        
        # Generate protocol for each health category with findings
        for category in HealthCategory:
            category_snps = [
                snp for snp in analysis_result.analyzed_snps 
                if snp.category == category
            ]
            
            if category_snps:
                protocol = self._generate_category_protocol(
                    analysis_result.analysis_id,
                    category,
                    category_snps
                )
                protocols.append(protocol)
        
        return protocols
    
    def _generate_category_protocol(
        self,
        analysis_id: str,
        category: HealthCategory,
        snps: List[SNP]
    ) -> HealthProtocol:
        """Generate protocol for a specific health category"""
        
        # Collect all recommendations from SNPs
        all_recommendations = []
        supplements = []
        lifestyle_changes = []
        dietary_advice = []
        
        for snp in snps:
            all_recommendations.extend(snp.recommendations)
        
        # Deduplicate recommendations
        all_recommendations = list(set(all_recommendations))
        
        # Categorize recommendations
        for rec in all_recommendations:
            rec_lower = rec.lower()
            if any(word in rec_lower for word in ['supplement', 'vitamin', 'mineral', 'omega', 'nac', 'glutathione']):
                supplements.append(rec)
            elif any(word in rec_lower for word in ['diet', 'food', 'eat', 'intake', 'meal']):
                dietary_advice.append(rec)
            else:
                lifestyle_changes.append(rec)
        
        # Calculate priority based on risk levels
        high_risk_count = sum(1 for snp in snps if snp.risk_level == RiskLevel.HIGH)
        if high_risk_count > 0:
            priority = "high"
        elif len(snps) > 2:
            priority = "medium"
        else:
            priority = "low"
        
        # Generate summary
        summary = self._generate_summary(category, snps, high_risk_count)
        
        return HealthProtocol(
            protocol_id=str(uuid.uuid4()),
            analysis_id=analysis_id,
            category=category,
            summary=summary,
            recommendations=all_recommendations,
            supplements=supplements if supplements else ["Consult with healthcare provider for personalized supplementation"],
            lifestyle_changes=lifestyle_changes if lifestyle_changes else ["Maintain a healthy lifestyle with regular exercise"],
            dietary_advice=dietary_advice if dietary_advice else ["Follow a balanced, whole-foods diet"],
            priority=priority
        )
    
    def _generate_summary(
        self,
        category: HealthCategory,
        snps: List[SNP],
        high_risk_count: int
    ) -> str:
        """Generate AI-powered summary for category"""
        
        summaries = {
            HealthCategory.LONGEVITY: self._longevity_summary,
            HealthCategory.DETOX: self._detox_summary,
            HealthCategory.METABOLISM: self._metabolism_summary,
            HealthCategory.SKIN_AGING: self._skin_aging_summary,
            HealthCategory.BRAIN_HEALTH: self._brain_health_summary
        }
        
        return summaries[category](snps, high_risk_count)
    
    def _longevity_summary(self, snps: List[SNP], high_risk_count: int) -> str:
        """Generate longevity protocol summary"""
        genes = [snp.gene for snp in snps]
        
        summary = f"Analysis of {len(snps)} longevity-related genetic markers including {', '.join(set(genes))}. "
        
        if high_risk_count > 0:
            summary += f"You have {high_risk_count} marker(s) associated with higher risk that require attention. "
            summary += "Focus on proactive lifestyle interventions, particularly cardiovascular health, cognitive training, and stress management."
        else:
            summary += "Your genetic profile shows favorable longevity markers. Maintain healthy lifestyle habits to maximize your genetic potential."
        
        return summary
    
    def _detox_summary(self, snps: List[SNP], high_risk_count: int) -> str:
        """Generate detox protocol summary"""
        summary = f"Analysis of {len(snps)} detoxification-related genetic markers. "
        
        if high_risk_count > 0:
            summary += "Your genetic profile indicates reduced detoxification capacity in certain pathways. "
            summary += "Support your liver and detox systems with targeted nutrition and minimize toxin exposure."
        else:
            summary += "Your detoxification pathways show normal function. Continue supporting liver health with a nutrient-rich diet."
        
        return summary
    
    def _metabolism_summary(self, snps: List[SNP], high_risk_count: int) -> str:
        """Generate metabolism protocol summary"""
        summary = f"Analysis of {len(snps)} metabolism-related genetic markers. "
        
        if high_risk_count > 0:
            summary += "Your genetic profile suggests increased susceptibility to weight gain and metabolic challenges. "
            summary += "Focus on portion control, regular physical activity, and balanced macronutrient intake."
        else:
            summary += "Your metabolic markers are favorable. Maintain a balanced diet and regular exercise routine."
        
        return summary
    
    def _skin_aging_summary(self, snps: List[SNP], high_risk_count: int) -> str:
        """Generate skin aging protocol summary"""
        summary = f"Analysis of {len(snps)} skin health and aging-related genetic markers. "
        
        if high_risk_count > 0:
            summary += "Your genetic profile indicates increased susceptibility to skin aging and collagen breakdown. "
            summary += "Prioritize sun protection, antioxidant-rich skincare, and collagen-supporting nutrition."
        else:
            summary += "Your skin health markers are favorable. Continue protecting against UV damage and oxidative stress."
        
        return summary
    
    def _brain_health_summary(self, snps: List[SNP], high_risk_count: int) -> str:
        """Generate brain health protocol summary"""
        summary = f"Analysis of {len(snps)} brain health and cognitive function markers. "
        
        if high_risk_count > 0:
            summary += "Your genetic profile suggests areas requiring attention for optimal cognitive health. "
            summary += "Focus on neuroprotective lifestyle factors including exercise, sleep, stress management, and cognitive training."
        else:
            summary += "Your brain health markers are favorable. Maintain cognitive fitness through lifelong learning and healthy lifestyle habits."
        
        return summary
