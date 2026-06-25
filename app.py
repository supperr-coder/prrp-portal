import streamlit as st
import pandas as pd
import io
from datetime import date

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="PRRP Portal",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Global CSS (clean & minimal) ─────────────────────────────────────────────
st.markdown(
    """
    <style>
    /* hide default Streamlit menu / footer */
    #MainMenu, footer { visibility: hidden; }

    /* page background */
    .stApp { background-color: #f8f9fa; }

    /* card container */
    .card {
        background: #ffffff;
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        padding: 2rem;
        margin-bottom: 1.5rem;
    }

    /* stepper bar */
    .stepper {
        display: flex;
        align-items: center;
        gap: 0;
        margin-bottom: 2rem;
    }
    .step {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        flex: 1;
    }
    .step-circle {
        width: 32px;
        height: 32px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 700;
        font-size: 0.9rem;
        flex-shrink: 0;
    }
    .step-circle.done   { background: #1a73e8; color: #fff; }
    .step-circle.active { background: #1a73e8; color: #fff; }
    .step-circle.todo   { background: #e0e0e0; color: #888; }
    .step-label { font-size: 0.8rem; color: #555; line-height: 1.2; }
    .step-label.active { color: #1a73e8; font-weight: 600; }
    .step-connector { flex: 1; height: 2px; background: #e0e0e0; margin: 0 4px; }
    .step-connector.done { background: #1a73e8; }

    /* section heading */
    .section-title {
        font-size: 1.25rem;
        font-weight: 700;
        color: #202124;
        margin-bottom: 0.25rem;
    }
    .section-sub {
        font-size: 0.875rem;
        color: #5f6368;
        margin-bottom: 1.25rem;
    }

    /* primary button */
    div.stButton > button[kind="primary"] {
        background-color: #1a73e8;
        color: #fff;
        border: none;
        border-radius: 6px;
        padding: 0.5rem 1.5rem;
    }
    div.stButton > button[kind="primary"]:hover {
        background-color: #1558b0;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ── Session state defaults ────────────────────────────────────────────────────
def _init():
    defaults = {
        "step": 1,
        "entity_id": "",
        "entity_valid": False,
        "gst_results": None,
        "uploaded_files": [],
        "draft_report": "",
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

_init()

# ── Stepper renderer ──────────────────────────────────────────────────────────
STEPS = [
    "Entity Lookup",
    "Data Tables",
    "GST Calculator",
    "Report Generator",
]

def render_stepper(current: int):
    parts = []
    for i, label in enumerate(STEPS, start=1):
        if i < current:
            circle_cls = "done"
            label_cls  = ""
            marker = "✓"
        elif i == current:
            circle_cls = "active"
            label_cls  = "active"
            marker = str(i)
        else:
            circle_cls = "todo"
            label_cls  = ""
            marker = str(i)

        parts.append(
            f'<div class="step">'
            f'  <div class="step-circle {circle_cls}">{marker}</div>'
            f'  <span class="step-label {label_cls}">{label}</span>'
            f'</div>'
        )
        if i < len(STEPS):
            conn_cls = "done" if i < current else ""
            parts.append(f'<div class="step-connector {conn_cls}"></div>')

    st.markdown(
        f'<div class="stepper">{"".join(parts)}</div>',
        unsafe_allow_html=True,
    )

# ── Hardcoded sample data generators ─────────────────────────────────────────
def get_income_data(entity_id: str) -> pd.DataFrame:
    return pd.DataFrame({
        "Period":      ["Q1 2024", "Q2 2024", "Q3 2024", "Q4 2024"],
        "Revenue ($)": [320_000, 415_000, 390_000, 480_000],
        "Expenses ($)":[ 210_000, 260_000, 245_000, 295_000],
        "Net Income ($)":[110_000, 155_000, 145_000, 185_000],
        "Entity":      [entity_id] * 4,
    })

def get_property_data(entity_id: str) -> pd.DataFrame:
    return pd.DataFrame({
        "Property Address": [
            "10 Anson Rd #20-01, Singapore 079903",
            "1 Harbourfront Ave #14-05, Singapore 098632",
        ],
        "Type":            ["Commercial", "Industrial"],
        "Annual Value ($)":[ 85_000,       62_000],
        "Ownership Start": ["2019-03-01",  "2021-07-15"],
        "Ownership End":   ["Present",     "Present"],
        "Entity":          [entity_id, entity_id],
    })

def get_tenancy_data(entity_id: str) -> pd.DataFrame:
    return pd.DataFrame({
        "Tenant Name":       ["ABC Pte Ltd", "XYZ Corp", "Global Trade Sg"],
        "Lease Start":       ["2022-01-01",  "2023-04-01", "2024-01-01"],
        "Lease End":         ["2024-12-31",  "2025-03-31", "2025-12-31"],
        "Monthly Rent ($)":  [4_500,          3_200,        5_800],
        "Property Address":  [
            "10 Anson Rd #20-01",
            "10 Anson Rd #20-01",
            "1 Harbourfront Ave #14-05",
        ],
        "Entity":            [entity_id] * 3,
    })

def to_excel_bytes(entity_id: str) -> bytes:
    buf = io.BytesIO()
    with pd.ExcelWriter(buf, engine="openpyxl") as writer:
        get_income_data(entity_id).to_excel(writer,   sheet_name="Income",   index=False)
        get_property_data(entity_id).to_excel(writer, sheet_name="Property", index=False)
        get_tenancy_data(entity_id).to_excel(writer,  sheet_name="Tenancy",  index=False)
    return buf.getvalue()

def to_csv_bytes(df: pd.DataFrame) -> bytes:
    return df.to_csv(index=False).encode()

# ── GST calculator ────────────────────────────────────────────────────────────
def compute_gst(entity_id: str, year: int) -> pd.DataFrame:
    quarterly = {
        "Q1": 320_000, "Q2": 415_000, "Q3": 390_000, "Q4": 480_000,
    }
    gst_rate = 0.09
    rows = []
    for q, rev in quarterly.items():
        taxable = rev * 0.80  # 80 % taxable (hardcoded assumption)
        gst     = taxable * gst_rate
        rows.append({
            "Quarter":         f"{q} {year}",
            "Total Revenue ($)": rev,
            "Taxable Revenue ($)": taxable,
            f"GST @ {gst_rate*100:.0f}% ($)": round(gst, 2),
            "Exempt Revenue ($)": rev - taxable,
        })
    df = pd.DataFrame(rows)
    total_row = pd.DataFrame([{
        "Quarter": f"TOTAL {year}",
        "Total Revenue ($)": df["Total Revenue ($)"].sum(),
        "Taxable Revenue ($)": df["Taxable Revenue ($)"].sum(),
        f"GST @ {gst_rate*100:.0f}% ($)": df[f"GST @ {gst_rate*100:.0f}% ($)"].sum(),
        "Exempt Revenue ($)": df["Exempt Revenue ($)"].sum(),
    }])
    return pd.concat([df, total_row], ignore_index=True)

# ── LLM draft (hardcoded) ─────────────────────────────────────────────────────
def generate_draft(entity_id: str, file_names: list[str]) -> str:
    today = date.today().strftime("%d %B %Y")
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

# ── Step renderers ────────────────────────────────────────────────────────────

def step1_entity_lookup():
    st.markdown('<div class="section-title">Entity / UEN Lookup</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Enter the entity ID or UEN to begin.</div>', unsafe_allow_html=True)

    entity_id = st.text_input(
        "Entity ID / UEN",
        value=st.session_state.entity_id,
        placeholder="e.g. 202312345A",
        max_chars=20,
    )

    col1, col2 = st.columns([1, 5])
    with col1:
        search = st.button("Search", type="primary", use_container_width=True)

    if search:
        if entity_id.strip():
            st.session_state.entity_id    = entity_id.strip().upper()
            st.session_state.entity_valid = True
            st.session_state.step         = 2
            st.rerun()
        else:
            st.error("Please enter a valid Entity ID / UEN.")

    if st.session_state.entity_valid:
        st.success(f"Entity **{st.session_state.entity_id}** is loaded. Proceed to the next step.")
        if st.button("Next →", type="primary"):
            st.session_state.step = 2
            st.rerun()


def step2_data_tables():
    eid = st.session_state.entity_id
    st.markdown('<div class="section-title">Extracted Data</div>', unsafe_allow_html=True)
    st.markdown(
        f'<div class="section-sub">Data for entity <strong>{eid}</strong> extracted from Maestro S3.</div>',
        unsafe_allow_html=True,
    )

    tab_inc, tab_prop, tab_ten = st.tabs(["📊 Income", "🏢 Property", "📋 Tenancy"])

    with tab_inc:
        df = get_income_data(eid)
        st.dataframe(df, use_container_width=True, hide_index=True)
        st.download_button(
            "⬇ Download Income CSV",
            data=to_csv_bytes(df),
            file_name=f"{eid}_income.csv",
            mime="text/csv",
        )

    with tab_prop:
        df = get_property_data(eid)
        st.dataframe(df, use_container_width=True, hide_index=True)
        st.download_button(
            "⬇ Download Property CSV",
            data=to_csv_bytes(df),
            file_name=f"{eid}_property.csv",
            mime="text/csv",
        )

    with tab_ten:
        df = get_tenancy_data(eid)
        st.dataframe(df, use_container_width=True, hide_index=True)
        st.download_button(
            "⬇ Download Tenancy CSV",
            data=to_csv_bytes(df),
            file_name=f"{eid}_tenancy.csv",
            mime="text/csv",
        )

    st.divider()
    st.download_button(
        "⬇ Download All Tables as Excel (.xlsx)",
        data=to_excel_bytes(eid),
        file_name=f"{eid}_data.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        type="primary",
    )

    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("← Back"):
            st.session_state.step = 1
            st.rerun()
    with col2:
        if st.button("Next →", type="primary"):
            st.session_state.step = 3
            st.rerun()


def step3_gst_calculator():
    eid = st.session_state.entity_id
    st.markdown('<div class="section-title">GST Registration Calculator</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-sub">Revenue breakdown by calendar year for GST threshold assessment.</div>',
        unsafe_allow_html=True,
    )

    col_a, col_b = st.columns([2, 4])
    with col_a:
        year = st.selectbox("Calendar Year", options=[2022, 2023, 2024, 2025], index=2)
        calc = st.button("Calculate", type="primary")

    if calc or st.session_state.gst_results is not None:
        df = compute_gst(eid, year)
        st.session_state.gst_results = df

        # highlight total row
        def highlight_total(row):
            return ["background-color: #e8f0fe; font-weight: bold" if "TOTAL" in str(row["Quarter"]) else "" for _ in row]

        st.dataframe(
            df.style.apply(highlight_total, axis=1),
            use_container_width=True,
            hide_index=True,
        )

        gst_col = [c for c in df.columns if "GST" in c][0]
        total_gst = df.loc[df["Quarter"].str.startswith("TOTAL"), gst_col].values[0]
        total_rev = df.loc[df["Quarter"].str.startswith("TOTAL"), "Total Revenue ($)"].values[0]

        threshold = 1_000_000
        st.info(
            f"**GST Registration Threshold:** SGD {threshold:,.0f}\n\n"
            f"**{eid}** — Total Revenue ({year}): **SGD {total_rev:,.0f}** | "
            f"Estimated GST Payable: **SGD {total_gst:,.2f}**\n\n"
            + ("⚠️ Revenue **exceeds** the GST registration threshold." if total_rev >= threshold
               else "✅ Revenue is **below** the GST registration threshold.")
        )

        st.download_button(
            "⬇ Download GST Breakdown CSV",
            data=to_csv_bytes(df),
            file_name=f"{eid}_gst_{year}.csv",
            mime="text/csv",
        )

    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("← Back"):
            st.session_state.step = 2
            st.rerun()
    with col2:
        if st.button("Next →", type="primary"):
            st.session_state.step = 4
            st.rerun()


def step4_report_generator():
    eid = st.session_state.entity_id
    st.markdown('<div class="section-title">Document Upload & Report Generator</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-sub">Upload supporting documents. A draft assessment report will be generated.</div>',
        unsafe_allow_html=True,
    )

    uploaded = st.file_uploader(
        "Upload documents (FormSG, contracts, invoices, listings)",
        accept_multiple_files=True,
        type=["pdf", "docx", "xlsx", "csv", "png", "jpg", "jpeg"],
    )

    if uploaded:
        st.success(f"{len(uploaded)} file(s) uploaded successfully.")
        for f in uploaded:
            st.markdown(f"- `{f.name}` ({f.size / 1024:.1f} KB)")

    st.divider()

    if st.button("✨ Generate Draft Report", type="primary"):
        file_names = [f.name for f in uploaded] if uploaded else []
        with st.spinner("Generating draft report…"):
            draft = generate_draft(eid, file_names)
        st.session_state.draft_report = draft

    if st.session_state.draft_report:
        st.markdown("#### Draft Report")
        st.text_area(
            label="",
            value=st.session_state.draft_report,
            height=450,
            label_visibility="collapsed",
        )
        st.download_button(
            "⬇ Download Report (.txt)",
            data=st.session_state.draft_report.encode(),
            file_name=f"{eid}_draft_report.txt",
            mime="text/plain",
            type="primary",
        )

    if st.button("← Back"):
        st.session_state.step = 3
        st.rerun()


# ── Main layout ───────────────────────────────────────────────────────────────
st.markdown("# 🏛️ PRRP Portal")
st.markdown("**Property, Revenue & Registration Portal** — Internal Assessment Tool")
st.divider()

render_stepper(st.session_state.step)

with st.container():
    st.markdown('<div class="card">', unsafe_allow_html=True)

    if not st.session_state.entity_valid and st.session_state.step > 1:
        st.warning("Please complete Step 1 first.")
        st.session_state.step = 1

    if st.session_state.step == 1:
        step1_entity_lookup()
    elif st.session_state.step == 2:
        step2_data_tables()
    elif st.session_state.step == 3:
        step3_gst_calculator()
    elif st.session_state.step == 4:
        step4_report_generator()

    st.markdown('</div>', unsafe_allow_html=True)
