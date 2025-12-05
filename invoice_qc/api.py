from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import tempfile
import os
import pdfplumber

from invoice_qc.validator import validate_all_invoices
from invoice_qc import extractor  # import your real extractor module


app = FastAPI()

# Enable CORS for frontend UI calls
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Invoice(BaseModel):
    invoice_number: Optional[str] = None
    invoice_date: Optional[str] = None
    seller_name: Optional[str] = None
    buyer_name: Optional[str] = None
    currency: Optional[str] = None
    net_total: Optional[float] = None
    tax_amount: Optional[float] = None
    gross_total: Optional[float] = None
    source_pdf: Optional[str] = None


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/validate-json")
async def validate_json(invoices: List[Invoice]):
    invoices_dicts = [inv.dict() for inv in invoices]
    results, summary = validate_all_invoices(invoices_dicts)
    return {"results": results, "summary": summary}


# =====================================================
#      Extract PDFs and Validate Invoices
# =====================================================
@app.post("/extract-and-validate-pdfs")
async def extract_and_validate_pdfs(files: List[UploadFile] = File(...)):
    extracted_invoices = []

    for file in files:
        # Save temp file for pdfplumber
        temp_path = os.path.join(tempfile.gettempdir(), file.filename)
        
        with open(temp_path, "wb") as f:
            f.write(await file.read())

        # Extract text from PDF
        with pdfplumber.open(temp_path) as pdf:
            text = ""
            for page in pdf.pages:
                t = page.extract_text() or ""
                text += t + "\n"

        # Use your existing extraction function
        invoice_data = extractor.extract_invoice_fields(text)
        invoice_data["source_pdf"] = file.filename

        extracted_invoices.append(invoice_data)

        # Remove temp file
        os.remove(temp_path)

    # Validate invoices
    results, summary = validate_all_invoices(extracted_invoices)

    return {
        "extracted_invoices": extracted_invoices,
        "results": results,
        "summary": summary
    }
