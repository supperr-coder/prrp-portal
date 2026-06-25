"""Step 1 — Entity / UEN lookup."""
import streamlit as st


def render():
    st.markdown('<div class="section-title">Entity / UEN Lookup</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Enter the entity ID or UEN to begin.</div>', unsafe_allow_html=True)

    entity_id = st.text_input(
        "Entity ID / UEN",
        value=st.session_state.entity_id,
        placeholder="e.g. 202312345A",
        max_chars=20,
    )

    col1, _ = st.columns([1, 5])
    with col1:
        search = st.button("Search", type="primary", key="s1_search")

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
        if st.button("Next →", type="primary", key="s1_next"):
            st.session_state.step = 2
            st.rerun()
