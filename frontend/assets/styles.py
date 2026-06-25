"""Global CSS injected once at app startup."""
import streamlit as st


def inject():
    st.markdown(
        """
        <style>
        #MainMenu, footer { visibility: hidden; }
        .stApp { background-color: #f8f9fa; }

        .card {
            background: #ffffff;
            border: 1px solid #e0e0e0;
            border-radius: 8px;
            padding: 2rem;
            margin-bottom: 1.5rem;
        }

        /* stepper */
        .stepper { display: flex; align-items: center; gap: 0; margin-bottom: 2rem; }
        .step { display: flex; align-items: center; gap: 0.5rem; flex: 1; }
        .step-circle {
            width: 32px; height: 32px; border-radius: 50%;
            display: flex; align-items: center; justify-content: center;
            font-weight: 700; font-size: 0.9rem; flex-shrink: 0;
        }
        .step-circle.done   { background: #1a73e8; color: #fff; }
        .step-circle.active { background: #1a73e8; color: #fff; }
        .step-circle.todo   { background: #e0e0e0; color: #888; }
        .step-label { font-size: 0.8rem; color: #555; line-height: 1.2; }
        .step-label.active { color: #1a73e8; font-weight: 600; }
        .step-connector { flex: 1; height: 2px; background: #e0e0e0; margin: 0 4px; }
        .step-connector.done { background: #1a73e8; }

        /* typography */
        .section-title { font-size: 1.25rem; font-weight: 700; color: #202124; margin-bottom: 0.25rem; }
        .section-sub   { font-size: 0.875rem; color: #5f6368; margin-bottom: 1.25rem; }

        /* primary button */
        div.stButton > button[kind="primary"] {
            background-color: #1a73e8; color: #fff;
            border: none; border-radius: 6px; padding: 0.5rem 1.5rem;
        }
        div.stButton > button[kind="primary"]:hover { background-color: #1558b0; }
        </style>
        """,
        unsafe_allow_html=True,
    )
