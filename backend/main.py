from fastapi import FastAPI, UploadFile, File
from ai.protocols.longevity_optimizer import generate_protocol_from_dna

app = FastAPI()

@app.post("/upload_dna")
async def upload_dna(file: UploadFile = File(...)):
    contents = await file.read()
    snp_data = contents.decode("utf-8")
    protocol = generate_protocol_from_dna(snp_data)
    return {"optimized_protocol": protocol}
