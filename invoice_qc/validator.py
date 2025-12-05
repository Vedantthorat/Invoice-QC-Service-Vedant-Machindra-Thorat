from dateutil.parser import parse as parse_date

# ------------------------------
# Validate ONE invoice
# ------------------------------
def validate_invoice(inv):
    errors = []

    # Required fields
    if not inv.get("invoice_number"):
        errors.append("missing_field: invoice_number")

    if not inv.get("invoice_date"):
        errors.append("missing_field: invoice_date")
    else:
        try:
            parse_date(inv["invoice_date"])
        except:
            errors.append("format_error: invoice_date_invalid")

    # Business rule: totals must match
    net = inv.get("net_total")
    tax = inv.get("tax_amount")
    gross = inv.get("gross_total")

    if net is not None and tax is not None and gross is not None:
        if abs((net + tax) - gross) > 1:
            errors.append("business_rule: totals_mismatch")

    return {
        "invoice_id": inv.get("invoice_number"),
        "is_valid": len(errors) == 0,
        "errors": errors
    }


# ------------------------------
# Validate ALL invoices
# ------------------------------
def validate_all_invoices(invoices):
    results = []
    error_counts = {}

    for inv in invoices:
        result = validate_invoice(inv)
        results.append(result)

        for err in result["errors"]:
            error_counts[err] = error_counts.get(err, 0) + 1

    summary = {
        "total_invoices": len(invoices),
        "valid_invoices": sum(r["is_valid"] for r in results),
        "invalid_invoices": sum(not r["is_valid"] for r in results),
        "error_counts": error_counts
    }

    return results, summary
