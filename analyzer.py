# ============================================================
#  core/analyzer.py  —  AI Image Analysis Logic
# ============================================================

import base64
import json
import re
import streamlit as st
from PIL import Image
import io
from groq import Groq


def prepare_image(uploaded_file) -> str:
    """Resize image and convert to base64 string."""
    img_bytes = uploaded_file.read()
    pil_img   = Image.open(io.BytesIO(img_bytes)).convert("RGB")

    if max(pil_img.size) > 1024:
        pil_img.thumbnail((1024, 1024), Image.LANCZOS)

    buf = io.BytesIO()
    pil_img.save(buf, format="JPEG", quality=85)
    return base64.standard_b64encode(buf.getvalue()).decode("utf-8")


def build_prompt(chk_face, chk_car, chk_obj, chk_scene) -> str:
    """Build the AI prompt based on selected detection options."""
    return f"""Analyze this image carefully and return ONLY a valid JSON object.
Do NOT include any markdown, backticks, or text outside the JSON.

Use this exact structure:
{{
  "objects": [
    {{"name": "object name", "emoji": "emoji", "confidence": 90,
      "category": "electronics/furniture/food/animal/person/vehicle/other",
      "details": "brief detail"}}
  ],
  "faces": [
    {{"id": 1, "estimated_age": "25-30 years", "gender": "Male/Female",
      "expression": "happy/neutral/sad/surprised/angry",
      "description": "brief description of the person"}}
  ],
  "vehicles": [
    {{"type": "car/truck/motorcycle/bus/van", "color": "color",
      "number_plate": "plate text or Not visible",
      "make_model": "brand and model if known",
      "description": "brief vehicle description"}}
  ],
  "scene_description": "Detailed English description of the entire scene — what is happening, who is present, background, lighting, colors, and overall mood.",
  "summary": {{
    "total_objects": 0,
    "has_faces": false,
    "has_vehicles": false,
    "setting": "indoor/outdoor",
    "time_of_day": "day/night/dawn/dusk/unknown"
  }}
}}

Detection rules:
{"- Detect ALL faces. Estimate age, gender, and expression carefully." if chk_face else "- Set faces to []."}
{"- Detect ALL vehicles. Try hard to read number plate characters." if chk_car else "- Set vehicles to []."}
{"- List every visible object, including small or background items." if chk_obj else "- Only include the single most prominent object."}
{"- Write a thorough detailed scene_description in English." if chk_scene else "- Keep scene_description to one sentence."}

Start with {{ and end with }}. Return ONLY valid JSON."""


def parse_response(raw: str):
    """Parse JSON from AI response, with fallback regex extraction."""
    raw = re.sub(r'^```json\s*', '', raw, flags=re.IGNORECASE)
    raw = re.sub(r'^```\s*', '', raw)
    raw = re.sub(r'\s*```$', '', raw).strip()

    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        match = re.search(r'\{[\s\S]*\}', raw)
        if match:
            return json.loads(match.group())
    return None


def analyze_image(uploaded_file, api_key, chk_face, chk_car, chk_obj, chk_scene):
    """Main function: sends image to Groq API and returns parsed result."""
    with st.spinner("🤖 AI is analyzing your image — please wait..."):
        try:
            b64_data = prepare_image(uploaded_file)
            prompt   = build_prompt(chk_face, chk_car, chk_obj, chk_scene)

            client   = Groq(api_key=api_key)
            response = client.chat.completions.create(
                model="meta-llama/llama-4-scout-17b-16e-instruct",
                messages=[{
                    "role": "user",
                    "content": [
                        {"type": "image_url",
                         "image_url": {"url": f"data:image/jpeg;base64,{b64_data}"}},
                        {"type": "text", "text": prompt}
                    ]
                }],
                max_tokens=2000,
                temperature=0.1,
            )

            raw    = response.choices[0].message.content.strip()
            result = parse_response(raw)

            if not result:
                st.error("❌ Could not parse the AI response. Please try again.")
                st.code(raw[:500])

            return result

        except Exception as e:
            err = str(e)
            if "401" in err or "invalid_api_key" in err.lower():
                st.error("❌ Invalid API Key. Check your key at console.groq.com.")
            elif "429" in err or "rate" in err.lower():
                st.error("❌ Rate limit reached. Please wait 1 minute and try again.")
            elif "model" in err.lower():
                st.error(f"❌ Model error: {err}")
            else:
                st.error(f"❌ Error: {err}")
            return None
