
import streamlit as st


def render_header():
    """Render the top header with title and feature tags."""
    st.markdown("# Intelligent Image Analyzer")
    # st.markdown("**Powered by LLaMA 4 Vision · Detect Objects · Faces · Vehicles · Number Plates**")
    st.markdown("""
    <div class="tag-row">
        <span class="tag">👤 Face & Age</span>
        <span class="tag">🚗 Vehicle & Plate</span>
        <span class="tag">📦 Object Detection</span>
        <span class="tag">🎭 Scene Description</span>
        <span class="tag">✅ 100% Free</span>
    </div>
    """, unsafe_allow_html=True)
    st.divider()


def render_sidebar():
    """Render the sidebar with API key input and detection options.
    Returns: (api_key, chk_face, chk_car, chk_obj, chk_scene)
    """
    with st.sidebar:
        st.markdown("## ⚙️ Configuration")
        # st.markdown('<div class="free-badge">✅ 100% FREE — No Payment Required</div>',
        #             unsafe_allow_html=True)
        # st.markdown("Uses **Groq Cloud API** with LLaMA 4 Vision — completely free.")
        st.markdown("")

        api_key = st.text_input(
            "🔑 Groq API Key",
            type="password",
            placeholder="gsk_...",
            help="Get your free key at console.groq.com"
        )
        # st.markdown("""
        # **How to get a free API Key:**
        # 1. Visit [console.groq.com](https://console.groq.com)
        # 2. Sign up with your Google account
        # 3. Go to **API Keys → Create API Key**
        # 4. Copy and paste it above
        # """)

        st.divider()
        st.markdown("### 🎯 Detection Options")
        chk_face  = st.checkbox("👤 Face Detection + Age Estimation", value=True)
        chk_car   = st.checkbox("🚗 Vehicle + Number Plate Reading",  value=True)
        chk_obj   = st.checkbox("📦 All Objects Detection",           value=True)
        chk_scene = st.checkbox("🎭 Full Scene Description",          value=True)

        st.divider()
        st.markdown("### ℹ️ About")
        st.info("""
        **VisionAI** is an AI-powered image analysis system (Final Year Project).
        Uses Meta's LLaMA 4 Vision via Groq's free API for real-time image understanding.
        """)

    return api_key, chk_face, chk_car, chk_obj, chk_scene


def render_upload_section(api_key):
    """Render image upload and analyze button.
    Returns: (uploaded_file, analyze_clicked)
    """
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 📁 Upload Image")
        uploaded = st.file_uploader(
            "Choose an image file",
            type=["png", "jpg", "jpeg", "webp"],
            label_visibility="collapsed"
        )
        if uploaded:
            st.image(uploaded, caption="Preview — Uploaded Image", use_column_width=True)
            size_kb = len(uploaded.getvalue()) / 1024
            st.caption(f"📄 `{uploaded.name}` · `{size_kb:.1f} KB` · `{uploaded.type}`")

    analyze_clicked = False
    with col2:
        st.markdown("### 🚀 Run Analysis")
        if not uploaded:
            st.info("👈 Please upload an image on the left to get started.")
        elif not api_key:
            st.warning("👈 Please enter your Groq API Key in the sidebar.")
        else:
            st.success("✅ Ready to analyze! Click the button below.")
            analyze_clicked = st.button("🔍 Analyze Image", use_container_width=True)

    return uploaded, analyze_clicked
