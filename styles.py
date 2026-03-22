# ============================================================
#  ui/styles.py  —  All CSS Styling
# ============================================================

import streamlit as st


def load_css():
    st.markdown("""
    <style>
        .stApp { background-color: #050810; color: #e2e8f0; }
        h1 { color: #00e5ff !important; }
        h2, h3 { color: #a78bfa !important; }

        /* Detection Cards */
        .det-card {
            background: #111827;
            border: 1px solid #1f2a3a;
            border-radius: 10px;
            padding: 1rem;
            margin-bottom: 0.75rem;
            color: #e2e8f0;
        }
        .det-card.face { border-left: 4px solid #00e5ff; }
        .det-card.car  { border-left: 4px solid #ff6b35; }
        .det-card.obj  { border-left: 4px solid #a78bfa; }

        .det-title {
            font-size: 1.05rem;
            font-weight: bold;
            margin-bottom: 0.3rem;
        }
        .det-sub {
            font-size: 0.82rem;
            color: #94a3b8;
            margin-bottom: 0.15rem;
        }

        /* Scene Description Box */
        .scene-box {
            background: #0d1117;
            border: 1px solid #1f2a3a;
            border-radius: 10px;
            padding: 1.2rem 1.5rem;
            line-height: 1.9;
            font-size: 0.95rem;
            color: #e2e8f0;
        }

        /* Analyze Button */
        .stButton > button {
            background: linear-gradient(135deg, #00e5ff, #7c3aed) !important;
            color: #000 !important;
            font-weight: 800 !important;
            border: none !important;
            border-radius: 8px !important;
        }

        /* Free Badge */
        .free-badge {
            background: linear-gradient(135deg, #10b981, #059669);
            color: white;
            padding: 0.3rem 0.8rem;
            border-radius: 20px;
            font-size: 0.75rem;
            font-weight: bold;
            display: inline-block;
            margin-bottom: 0.5rem;
        }

        /* Header Tags */
        .tag-row { display: flex; gap: 0.5rem; flex-wrap: wrap; margin-top: 0.5rem; }
        .tag {
            background: rgba(0,229,255,0.1);
            border: 1px solid rgba(0,229,255,0.25);
            color: #00e5ff;
            font-size: 0.72rem;
            padding: 0.2rem 0.6rem;
            border-radius: 4px;
            font-weight: 600;
        }
    </style>
    """, unsafe_allow_html=True)
