import os
import pdfplumber
import re
from dateutil.parser import parse as parse_date


# ------------------------------
# Convert German number format
# ------------------------------
def extract_number(value):
    try:
        return float(value.replace(".", "").replace(",", "."))
    except:
        return None


# ------------------------------
# Extract Invoice Number
# ------------------------------
def extract_invoice_number(text):
    m = re.search(r"Bestellung\s+([A-Za-z0-9]+)", text, re.IGNORECASE)
    if m:
        return m.group(1)
    return None


# ------------------------------
# Extract Invoice Date
# ------------------------------
def extract_invoice_date(text):
    m = re.search(r"(\d{1,2}[.\-/]\d{1,2}[.\-/]\d{4})", text)
    if m:
        try:
            return str(parse_date(m.group(1)).date())
        except:
            return None
    return None


# ------------------------------
# Extract Totals (NET, TAX, GROSS)
# ------------------------------
def extract_totals(text):
    # ---------- NET ----------
    net_match = re.search(
        r"Gesamtwert\s*(?:EUR)?\s*([0-9]{1,3}[.,][0-9]{2})",
        text,
        re.IGNORECASE
    )
    net = extract_number(net_match.group(1)) if net_match else None

    # ---------- TAX ----------
    tax = None
    mwst = re.search(r"MwSt", text, re.IGNORECASE)
    if mwst:
        after = text[mwst.end():]

        nums = re.findall(r"([0-9]{1,3}[.,][0-9]{2})", after)

        nums = [n for n in nums if not n.endswith("00")]  # ignore 19,00%

        if nums:
            tax = extract_number(nums[0])

    # ---------- GROSS ----------
    gross_match = re.search(
        r"Gesamtwert inkl\. MwSt\.\s*(?:EUR)?\s*([0-9.,]+)",
        text,
        re.IGNORECASE
    )
    gross = extract_number(gross_match.group(1)) if gross_match else None

    return net, tax, gross


# ------------------------------
# Extract EVERYTHING from a PDF
# ------------------------------
def extract_invoice_fields(text):
    invoice_number = extract_invoice_number(text)
    invoice_date = extract_invoice_date(text)
    net, tax, gross = extract_totals(text)

    return {
        "invoice_number": invoice_number,
        "invoice_date": invoice_date,
        "net_total": net,
        "tax_amount": tax,
        "gross_total": gross
    }


# ------------------------------
# PDF to text
# ------------------------------
def extract_text_from_pdf(path):
    with pdfplumber.open(path) as pdf:
        text = ""
        for page in pdf.pages:
            t = page.extract_text() or ""
            text += t + "\n"
    return text


# ------------------------------
# One invoice file
# ------------------------------
def extract_invoice(path):
    text = extract_text_from_pdf(path)
    invoice = extract_invoice_fields(text)
    invoice["source_pdf"] = path
    return invoice


# ------------------------------
# All invoices in folder
# ------------------------------
def extract_all_invoices(folder):
    invoices = []
    for file in os.listdir(folder):
        if file.lower().endswith(".pdf"):
            path = os.path.join(folder, file)
            invoice = extract_invoice(path)
            invoices.append(invoice)
    return invoices
