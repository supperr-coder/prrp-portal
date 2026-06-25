"""Draft report generator (hardcoded; swap with LLM API call later)."""
from datetime import date


def generate_draft(entity_id: str, file_names: list[str]) -> str:
    today      = date.today().strftime("%d %B %Y")
    files_list = "\n".join(f"  - {f}" for f in file_names) if file_names else "  - (no files uploaded)"
    return f"""DRAFT REPORT — PRRP Assessment
Generated: {today}
Entity / UEN: {entity_id}

────────────────────────────────────────────────────────
1. EXECUTIVE SUMMARY
────────────────────────────────────────────────────────
This report summarises the preliminary assessment of {entity_id} based on the
documents provided and data extracted from IRAS/ACRA records. The findings
below are subject to further verification and should not be treated as a final
determination.

────────────────────────────────────────────────────────
2. DOCUMENTS REVIEWED
────────────────────────────────────────────────────────
{files_list}

────────────────────────────────────────────────────────
3. FINANCIAL OVERVIEW
────────────────────────────────────────────────────────
Based on the extracted income data, {entity_id} recorded total revenue of
approximately SGD 1,605,000 for FY2024. Net income stood at approximately
SGD 595,000, reflecting a net margin of ~37%.

Key observations:
  • Revenue grew consistently across all four quarters of FY2024.
  • No significant anomalies were identified in the expense breakdown.
  • Taxable revenue for GST purposes is estimated at SGD 1,284,000.

────────────────────────────────────────────────────────
4. PROPERTY & TENANCY ASSESSMENT
────────────────────────────────────────────────────────
{entity_id} holds two commercial/industrial properties with a combined annual
value of SGD 147,000. Three tenancy agreements are on record, with the latest
commencing January 2024.

────────────────────────────────────────────────────────
5. GST COMPLIANCE NOTE
────────────────────────────────────────────────────────
Based on the GST breakdown, estimated GST payable for FY2024 is SGD 115,560.
Please verify against filed GST F5/F8 returns.

────────────────────────────────────────────────────────
6. RECOMMENDATIONS & NEXT STEPS
────────────────────────────────────────────────────────
  1. Cross-verify revenue figures against bank statements and invoices.
  2. Confirm property ownership dates with SLA records.
  3. Obtain executed copies of all tenancy agreements for audit trail.
  4. Review supporting invoices uploaded to confirm GST input claims.

────────────────────────────────────────────────────────
DISCLAIMER: This is an AI-assisted draft. All figures must be independently
verified before use in any official assessment or proceeding.
────────────────────────────────────────────────────────
"""
