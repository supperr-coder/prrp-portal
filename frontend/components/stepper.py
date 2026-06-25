"""Horizontal stepper UI component."""
import streamlit as st

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
            circle_cls, label_cls, marker = "done",   "",       "✓"
        elif i == current:
            circle_cls, label_cls, marker = "active", "active", str(i)
        else:
            circle_cls, label_cls, marker = "todo",   "",       str(i)

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
