def generate_protocol_from_dna(snp_raw_text: str) -> dict:
    """
    Generate personalized longevity protocol based on SNP data.
    
    Args:
        snp_raw_text: Raw DNA data containing SNP information
        
    Returns:
        Dictionary with personalized protocol recommendations
    """
    protocol = {}
    
    # CYP2C9 - Drug metabolism
    if "rs1799853" in snp_raw_text:
        protocol["detox"] = "You may have reduced CYP2C9 function. Avoid NSAIDs, increase cruciferous vegetables."
    
    # MTHFR - Methylation pathway
    if "rs1801133" in snp_raw_text:
        protocol["methylation"] = "MTHFR variant detected. Supplement with methylated B12 and folate."
    
    # ADRB3 - Metabolism and fat burning
    if "rs4994" in snp_raw_text:
        protocol["metabolism"] = "ADRB3 variant suggests lower fat burning. Prioritize HIIT and green tea extract."
    
    # VDR - Vitamin D receptor
    if "rs731236" in snp_raw_text:
        protocol["vitamin_d"] = "VDR gene variant. Monitor vitamin D levels closely and supplement as needed."
    
    return protocol
