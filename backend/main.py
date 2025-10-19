from fastapi import FastAPI, UploadFile, File
from ai.protocols.longevity_optimizer import generate_protocol_from_dna
from ai.protocols.vcf_parser import parse_vcf_to_snps  # <-- new import

app = FastAPI()

@app.post("/upload_dna")
async def upload_dna(file: UploadFile = File(...)):
    contents = await file.read()
    snp_data = contents.decode("utf-8")
    protocol = generate_protocol_from_dna(snp_data)
    return {"optimized_protocol": protocol}

@app.post("/upload_vcf")
async def upload_vcf(file: UploadFile = File(...)):
    contents = await file.read()
    vcf_text = contents.decode("utf-8")
    snp_ids = parse_vcf_to_snps(vcf_text)
    protocol = generate_protocol_from_dna('\n'.join(snp_ids))
    return {"optimized_protocol": protocol}

