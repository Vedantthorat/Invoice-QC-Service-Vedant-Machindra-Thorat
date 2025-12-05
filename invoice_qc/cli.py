import json
import os
import typer

from invoice_qc.extractor import extract_invoice, extract_all_invoices
from invoice_qc.validator import validate_all_invoices

app = typer.Typer()


# ------------------------------
# Command 1: Extract PDFs → JSON
# ------------------------------
@app.command()
def extract(pdf_dir: str, output: str):
    """
    Extract all PDF invoices from the given directory.
    """
    invoices = extract_all_invoices(pdf_dir)

    with open(output, "w", encoding="utf-8") as f:
        json.dump(invoices, f, indent=2, ensure_ascii=False)

    typer.echo(f"Extracted {len(invoices)} invoices → {output}")


# ------------------------------
# Command 2: Validate JSON file
# ------------------------------
@app.command()
def validate(input: str, report: str):
    """
    Validate extracted invoices JSON.
    """
    with open(input, "r", encoding="utf-8") as f:
        invoices = json.load(f)

    results, summary = validate_all_invoices(invoices)

    with open(report, "w", encoding="utf-8") as f:
        json.dump({"results": results, "summary": summary}, f, indent=2)

    typer.echo("Validation completed.")
    typer.echo(f"Valid invoices: {summary['valid_invoices']}")
    typer.echo(f"Invalid invoices: {summary['invalid_invoices']}")


# ------------------------------
# Command 3: FULL RUN (Extract + Validate)
# ------------------------------
@app.command()
def full_run(pdf_dir: str, report: str):
    """
    Extract and validate invoices in one command.
    """
    temp_output = "temp_extracted.json"

    # Step 1: Extract
    invoices = extract_all_invoices(pdf_dir)
    with open(temp_output, "w", encoding="utf-8") as f:
        json.dump(invoices, f, indent=2)

    # Step 2: Validate
    results, summary = validate_all_invoices(invoices)

    with open(report, "w", encoding="utf-8") as f:
        json.dump({"results": results, "summary": summary}, f, indent=2)

    typer.echo(f"Full run completed. Summary saved to {report}")
    typer.echo(f"Valid invoices: {summary['valid_invoices']}")
    typer.echo(f"Invalid invoices: {summary['invalid_invoices']}")


if __name__ == "__main__":
    app()
