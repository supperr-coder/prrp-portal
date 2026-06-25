"""Step 3 — GST registration calculator."""
import streamlit as st
from frontend.utils.data import compute_gst, to_csv_bytes

GST_THRESHOLD = 1_000_000


def render():
    eid = st.session_state.entity_id
    st.markdown('<div class="section-title">GST Registration Calculator</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-sub">Revenue breakdown by calendar year for GST threshold assessment.</div>',
        unsafe_allow_html=True,
    )

    col_a, _ = st.columns([2, 4])
    with col_a:
        year = st.selectbox("Calendar Year", options=[2022, 2023, 2024, 2025], index=2)
        calc = st.button("Calculate", type="primary")

    if calc or st.session_state.gst_results is not None:
        df = compute_gst(eid, year)
        st.session_state.gst_results = df

        gst_col = [c for c in df.columns if "GST" in c][0]

        def highlight_total(row):
            style = "background-color: #e8f0fe; font-weight: bold"
            return [style if "TOTAL" in str(row["Quarter"]) else "" for _ in row]

        st.dataframe(df.style.apply(highlight_total, axis=1),
                     use_container_width=True, hide_index=True)

        total_gst = df.loc[df["Quarter"].str.startswith("TOTAL"), gst_col].values[0]
        total_rev = df.loc[df["Quarter"].str.startswith("TOTAL"), "Total Revenue ($)"].values[0]

        threshold_hit = total_rev >= GST_THRESHOLD
        st.info(
            f"**GST Registration Threshold:** SGD {GST_THRESHOLD:,.0f}\n\n"
            f"**{eid}** — Total Revenue ({year}): **SGD {total_rev:,.0f}** | "
            f"Estimated GST Payable: **SGD {total_gst:,.2f}**\n\n"
            + ("⚠️ Revenue **exceeds** the GST registration threshold." if threshold_hit
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
