"""Step 4 — Document upload and draft report generator."""
import streamlit as st
from frontend.utils.report import generate_draft


def render():
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
            st.session_state.draft_report = generate_draft(eid, file_names)

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
