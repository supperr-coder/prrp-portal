"""Step 3 — GST registration calculator."""
import streamlit as st
from frontend.utils.data import compute_gst, to_excel_bytes_gst

GST_THRESHOLD = 1_000_000


def render():
    eid = st.session_state.entity_id
    st.markdown('<div class="section-title">GST Registration Calculator</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-sub">Select a calendar year and calculate the GST breakdown.</div>',
        unsafe_allow_html=True,
    )

    year = st.selectbox("Calendar Year", options=[2022, 2023, 2024, 2025], index=2, key="gst_year")

    if st.button("Calculate", type="primary", key="gst_calc"):
        df = compute_gst(eid, year)
        gst_col   = [c for c in df.columns if "GST" in c][0]
        total_gst = df.loc[df["Quarter"].str.startswith("TOTAL"), gst_col].values[0]
        total_rev = df.loc[df["Quarter"].str.startswith("TOTAL"), "Total Revenue ($)"].values[0]

        def highlight_total(row):
            style = "background-color: #e8f0fe; font-weight: bold"
            return [style if "TOTAL" in str(row["Quarter"]) else "" for _ in row]

        st.dataframe(df.style.apply(highlight_total, axis=1), width="stretch", hide_index=True)

        threshold_hit = total_rev >= GST_THRESHOLD
        st.info(
            f"**GST Registration Threshold:** SGD {GST_THRESHOLD:,.0f}\n\n"
            f"**{eid}** — Total Revenue ({year}): **SGD {total_rev:,.0f}** | "
            f"Estimated GST Payable: **SGD {total_gst:,.2f}**\n\n"
            + ("⚠️ Revenue **exceeds** the GST registration threshold." if threshold_hit
               else "✅ Revenue is **below** the GST registration threshold.")
        )

        st.download_button(
            "⬇ Download GST Breakdown (.xlsx)",
            data=to_excel_bytes_gst(df, year),
            file_name=f"{eid}_gst_{year}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            key="dl_gst_excel",
        )

    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("← Back", key="s3_back"):
            st.session_state.step = 2
            st.rerun()
    with col2:
        if st.button("Next →", type="primary", key="s3_next"):
            st.session_state.step = 4
            st.rerun()
