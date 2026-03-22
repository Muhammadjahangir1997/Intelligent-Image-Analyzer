# ============================================================
#  ui/results.py  —  Display Analysis Results
# ============================================================

import json
import streamlit as st


def render_results(r: dict, chk_face, chk_car, chk_obj, chk_scene):
    """Render the full results section from parsed AI response."""
    st.divider()
    st.markdown("## 📊 Analysis Results")

    faces    = r.get("faces",    [])
    vehicles = r.get("vehicles", [])
    objects  = r.get("objects",  [])
    summary  = r.get("summary",  {})

    # ── Summary Metrics ───────────────────────────────────────────────────────
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("👤 Faces",      len(faces))
    c2.metric("🚗 Vehicles",   len(vehicles))
    c3.metric("📦 Objects",    len(objects))
    c4.metric("🌍 Setting",    str(summary.get("setting",    "?")).capitalize())
    c5.metric("🕐 Time of Day",str(summary.get("time_of_day","?")).capitalize())
    st.divider()

    # ── Face Results ──────────────────────────────────────────────────────────
    _render_faces(faces, chk_face)

    # ── Vehicle Results ───────────────────────────────────────────────────────
    _render_vehicles(vehicles, chk_car)

    # ── Object Results ────────────────────────────────────────────────────────
    _render_objects(objects, chk_obj)

    # ── Scene Description ─────────────────────────────────────────────────────
    _render_scene(r.get("scene_description", ""), chk_scene)

    st.divider()

    # ── Export ────────────────────────────────────────────────────────────────
    _render_export(r)


# ── Private helpers ───────────────────────────────────────────────────────────

def _render_faces(faces, chk_face):
    if not chk_face:
        return
    st.markdown("### 👤 Face Detection Results")
    if not faces:
        st.info("No faces detected in this image.")
        return
    cols = st.columns(min(len(faces), 3))
    for i, f in enumerate(faces):
        with cols[i % 3]:
            st.markdown(f"""
            <div class="det-card face">
                <div class="det-title">😊 Person #{f.get('id', i+1)}</div>
                <div class="det-sub">🎂 Estimated Age: <b>{f.get('estimated_age','Unknown')}</b></div>
                <div class="det-sub">⚧ Gender: <b>{f.get('gender','Unknown')}</b></div>
                <div class="det-sub">😶 Expression: <b>{f.get('expression','Unknown')}</b></div>
                <div class="det-sub" style="margin-top:0.4rem;color:#cbd5e1">
                    {f.get('description','')}
                </div>
            </div>""", unsafe_allow_html=True)


def _render_vehicles(vehicles, chk_car):
    if not chk_car:
        return
    st.markdown("### 🚗 Vehicle Detection Results")
    if not vehicles:
        st.info("No vehicles detected in this image.")
        return
    for v in vehicles:
        plate = v.get("number_plate", "Not visible")
        plate_color = "#10b981" if plate.lower() not in ("not visible","n/a","") else "#64748b"
        st.markdown(f"""
        <div class="det-card car">
            <div class="det-title">
                🚗 {str(v.get('type','Vehicle')).capitalize()} — {v.get('color','Unknown Color')}
            </div>
            <div class="det-sub">🏷️ Make / Model: <b>{v.get('make_model','Unknown')}</b></div>
            <div class="det-sub">
                🔢 Number Plate: <b style="color:{plate_color}">{plate}</b>
            </div>
            <div class="det-sub" style="margin-top:0.4rem;color:#cbd5e1">
                {v.get('description','')}
            </div>
        </div>""", unsafe_allow_html=True)


def _render_objects(objects, chk_obj):
    if not chk_obj:
        return
    st.markdown("### 📦 Detected Objects")
    if not objects:
        st.info("No objects detected in this image.")
        return
    cols = st.columns(3)
    for i, obj in enumerate(objects[:12]):
        with cols[i % 3]:
            conf = int(obj.get("confidence", 80))
            color = "#10b981" if conf >= 85 else "#f59e0b" if conf >= 65 else "#ef4444"
            st.markdown(f"""
            <div class="det-card obj">
                <div class="det-title">{obj.get('emoji','📦')} {obj.get('name','Unknown Object')}</div>
                <div class="det-sub">🗂️ Category: <b>{str(obj.get('category','?')).capitalize()}</b></div>
                <div class="det-sub">📝 {obj.get('details','—')}</div>
                <div class="det-sub" style="margin-top:0.4rem">
                    Confidence: <b style="color:{color}">{conf}%</b>
                </div>
            </div>""", unsafe_allow_html=True)
            st.progress(conf / 100)


def _render_scene(description, chk_scene):
    if not chk_scene:
        return
    st.markdown("### 🎭 Full Scene Description")
    if description:
        st.markdown(f'<div class="scene-box">{description}</div>', unsafe_allow_html=True)
    else:
        st.info("No scene description available.")


def _render_export(r):
    col_a, col_b = st.columns(2)
    with col_a:
        with st.expander("🔧 View Raw JSON Response"):
            st.json(r)
    with col_b:
        st.download_button(
            label="⬇️ Download Results as JSON",
            data=json.dumps(r, indent=2),
            file_name="visionai_results.json",
            mime="application/json"
        )
