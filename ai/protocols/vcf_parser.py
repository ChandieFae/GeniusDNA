def parse_vcf_to_snps(vcf_text: str) -> list:
    """
    Parses a VCF (Variant Call Format) file and extracts SNP IDs (rsIDs).
    Returns a list of SNP IDs for downstream protocol generation.
    """
    snp_ids = []

    for line in vcf_text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue  # Skip headers and comments

        parts = line.split('\t')
        if len(parts) >= 3:
            rsid = parts[2]
            if rsid.startswith("rs"):
                snp_ids.append(rsid)

    return snp_ids
