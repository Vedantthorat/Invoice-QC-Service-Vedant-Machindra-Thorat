# Invoice QC Service — Vedant Machindra Thorat

A simple **Invoice Extraction & Quality Control (QC)** system built for the DeepLogic AI internship assignment.  
The project extracts invoice data from PDFs, validates fields using business rules, and provides CLI + API + optional UI.

---

## 🚀 Features
- Extracts: invoice_id, invoice_date, net_total, tax_amount, gross_total, source_pdf  
- Validates completeness, formats, and totals  
- CLI tools for extract/validate  
- FastAPI backend  

---

## 📁 Folder Structure
invoice_qc/  
│── extractor.py  
│── validator.py  
│── cli.py  
│── api.py  
ui/  
│── index.html  
sample_pdfs/  
README.md  

---

## ⚙️ Setup
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt


### ⭐ Start the Server
cd Project # (or folder where invoice_qc exists)
uvicorn invoice_qc.api:app --reload


---

## 🖥 CLI Usage
python -m invoice_qc.cli extract --pdf-dir sample_pdfs --output extracted.json
python -m invoice_qc.cli validate --input extracted.json --report report.json
python -m invoice_qc.cli full-run --pdf-dir sample_pdfs --report report.json



---

## 🌐 API Endpoints
GET /health
POST /validate-json
POST /extract-and-validate-pdfs



Swagger Docs:
http://127.0.0.1:8000/docs


---

## 🎨 UI (Bonus)
Open:
ui/index.html



Supports:
- PDF upload + validation  
- JSON upload + validation  
- Summary + detailed errors  

---

## 🤖 AI Usage Notes
AI helped with:
- Regex cleanup  
- UI styling  
- Documentation  

---

## 📝 Summary
A clean, minimal invoice QC system demonstrating:
- PDF extraction  
- Rule-based validation  
- CLI + API development  
- Optional UI
