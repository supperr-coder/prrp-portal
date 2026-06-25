"""PRRP Portal — Streamlit entry point."""
import streamlit as st
from frontend.assets.styles import inject
from frontend.components.stepper import render_stepper
from frontend.components import (
    entity_lookup,
    data_tables,
    gst_calculator,
    report_generator,
)

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="PRRP Portal",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="collapsed",
)
inject()

# ── Session state defaults ────────────────────────────────────────────────────
_DEFAULTS = {
    "step":         1,
    "entity_id":    "",
    "entity_valid": False,
    "draft_report": "",
}
for _k, _v in _DEFAULTS.items():
    if _k not in st.session_state:
        st.session_state[_k] = _v

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("# 🏛️ PRRP Portal")
st.markdown("**Property, Revenue & Registration Portal** — Internal Assessment Tool")
st.divider()

render_stepper(st.session_state.step)

# ── Guard: must complete Step 1 first ────────────────────────────────────────
if not st.session_state.entity_valid and st.session_state.step > 1:
    st.warning("Please complete Step 1 first.")
    st.session_state.step = 1

# ── Step router ───────────────────────────────────────────────────────────────
match st.session_state.step:
    case 1: entity_lookup.render()
    case 2: data_tables.render()
    case 3: gst_calculator.render()
    case 4: report_generator.render()
