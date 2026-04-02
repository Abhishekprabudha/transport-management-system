import streamlit as st


def kpi_card(title: str, value, subtitle: str = ""):
    st.markdown(
        f"""
        <div class='kpi-card'>
            <div class='kpi-title'>{title}</div>
            <div class='kpi-value'>{value}</div>
            <div class='kpi-sub'>{subtitle}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def status_badge(text: str):
    return f"<span class='status-badge'>{text}</span>"
