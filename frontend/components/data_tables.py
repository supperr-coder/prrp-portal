"""Step 2 — Income / Property / Tenancy data tables."""
import streamlit as st
from frontend.utils.data import (
    get_income_data,
    get_property_data,
    get_tenancy_data,
    to_excel_bytes,
    to_csv_bytes,
)


def render():
    eid = st.session_state.entity_id
    st.markdown('<div class="section-title">Extracted Data</div>', unsafe_allow_html=True)
    st.markdown(
        f'<div class="section-sub">Data for entity <strong>{eid}</strong> extracted from Maestro S3.</div>',
        unsafe_allow_html=True,
    )

    tab_inc, tab_prop, tab_ten = st.tabs(["📊 Income", "🏢 Property", "📋 Tenancy"])

    with tab_inc:
        df = get_income_data(eid)
        st.dataframe(df, width="stretch", hide_index=True)
        st.download_button("⬇ Download Income CSV", data=to_csv_bytes(df),
                           file_name=f"{eid}_income.csv", mime="text/csv",
                           key="dl_income_csv")

    with tab_prop:
        df = get_property_data(eid)
        st.dataframe(df, width="stretch", hide_index=True)
        st.download_button("⬇ Download Property CSV", data=to_csv_bytes(df),
                           file_name=f"{eid}_property.csv", mime="text/csv",
                           key="dl_property_csv")

    with tab_ten:
        df = get_tenancy_data(eid)
        st.dataframe(df, width="stretch", hide_index=True)
        st.download_button("⬇ Download Tenancy CSV", data=to_csv_bytes(df),
                           file_name=f"{eid}_tenancy.csv", mime="text/csv",
                           key="dl_tenancy_csv")

    st.divider()
    st.download_button(
        "⬇ Download All Tables as Excel (.xlsx)",
        data=to_excel_bytes(eid),
        file_name=f"{eid}_data.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        type="primary",
        key="dl_all_excel",
    )

    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("← Back", key="s2_back"):
            st.session_state.step = 1
            st.rerun()
    with col2:
        if st.button("Next →", type="primary", key="s2_next"):
            st.session_state.step = 3
            st.rerun()
