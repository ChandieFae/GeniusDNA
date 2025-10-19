def generate_protocol_from_dna(snp_raw_text: str) -> dict:
    lines = snp_raw_text.splitlines()
    snp_ids = [line.split('\t')[0] for line in lines if not line.startswith('#')]
    protocol = {}

    if "rs1799853" in snp_ids:
        protocol["detox"] = "Reduced CYP2C9. Avoid NSAIDs; boost cruciferous intake."

    if "rs1801133" in snp_ids:
        protocol["methylation"] = "MTHFR variant. Supplement with methylated folate + B12."

    if "rs4994" in snp_ids:
        protocol["metabolism"] = "ADRB3 variant. Prioritize HIIT and green tea extract."

    if "rs731236" in snp_ids:
        protocol["vitamin_d"] = "VDR variant. Monitor vitamin D levels and supplement accordingly."

    return protocol
