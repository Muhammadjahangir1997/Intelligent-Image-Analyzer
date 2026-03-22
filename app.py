
import streamlit as st
from ui.layout import render_header, render_sidebar, render_upload_section
from ui.results import render_results
from core.analyzer import analyze_image

st.set_page_config(
    page_title="VisionAI — Intelligent Image Analyzer",
    page_icon="🔍",
    layout="wide"
)

# Load CSS
from ui.styles import load_css
load_css()

# ── Render UI ─────────────────────────────────────────────
render_header()

api_key, chk_face, chk_car, chk_obj, chk_scene = render_sidebar()

uploaded, analyze_clicked = render_upload_section(api_key)

# ── Run Analysis ──────────────────────────────────────────
if uploaded and api_key and analyze_clicked:
    result = analyze_image(uploaded, api_key, chk_face, chk_car, chk_obj, chk_scene)
    if result:
        st.session_state["result"] = result
        st.success("✅ Analysis complete! Scroll down to see results.")

# ── Show Results ──────────────────────────────────────────
if "result" in st.session_state:
    render_results(
        st.session_state["result"],
        chk_face, chk_car, chk_obj, chk_scene
    )
