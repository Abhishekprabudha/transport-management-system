import streamlit as st


def inject_styles():
    st.markdown(
        """
        <style>
        .kpi-card {
            background: #f7f9fc;
            padding: 16px;
            border-radius: 16px;
            border: 1px solid #d9e2f0;
            min-height: 112px;
        }
        .kpi-title {font-size: 0.9rem; color: #4b5563;}
        .kpi-value {font-size: 1.9rem; font-weight: 700; color: #0f172a;}
        .kpi-sub {font-size: 0.85rem; color: #2563eb;}
        .status-badge {
            display:inline-block; padding:6px 10px; border-radius:999px;
            background:#e0f2fe; color:#075985; font-weight:600;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
