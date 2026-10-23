import streamlit as st
from google import genai
from google.genai import types
from dotenv import load_dotenv
import time
import os

load_dotenv()

# ── Page Configuration ────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Dawai Samjho · AI Medical Assistant",
    page_icon="D",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Modern SaaS Styling & Continuous Wheel Rotation ───────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Inter:wght@400;500;600;700&display=swap');

    /* Global Typography */
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        color: #f1f5f9;
        letter-spacing: -0.01em;
    }

    /* Living High-Contrast Animated Dark Background */
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    .stApp {
        background: linear-gradient(-45deg, #070914, #1e1b4b, #0c2d48, #2e1065, #063730, #070914);
        background-size: 320% 320%;
        animation: gradientShift 14s ease infinite;
        min-height: 100vh;
    }

    /* High-Visibility Floating Aurora Orbs */
    .stApp::before {
        content: '';
        position: fixed;
        top: 2%;
        left: 8%;
        width: 580px;
        height: 580px;
        background: radial-gradient(circle, rgba(99, 102, 241, 0.38) 0%, rgba(124, 58, 237, 0.22) 40%, transparent 72%);
        border-radius: 50%;
        filter: blur(80px);
        pointer-events: none;
        z-index: 0;
        animation: floatOrb1 11s ease-in-out infinite alternate;
    }

    .stApp::after {
        content: '';
        position: fixed;
        bottom: 2%;
        right: 8%;
        width: 580px;
        height: 580px;
        background: radial-gradient(circle, rgba(16, 185, 129, 0.32) 0%, rgba(6, 182, 212, 0.24) 40%, transparent 72%);
        border-radius: 50%;
        filter: blur(80px);
        pointer-events: none;
        z-index: 0;
        animation: floatOrb2 13s ease-in-out infinite alternate;
    }

    @keyframes floatOrb1 {
        0% { transform: translate(0, 0) scale(1); }
        100% { transform: translate(70px, 50px) scale(1.18); }
    }

    @keyframes floatOrb2 {
        0% { transform: translate(0, 0) scale(1); }
        100% { transform: translate(-60px, -70px) scale(1.22); }
    }

    /* Clean Streamlit Headers */
    header[data-testid="stHeader"] {
        background: transparent !important;
    }

    /* Hero Section */
    .hero-container {
        text-align: center;
        padding: 1.5rem 1rem 2.2rem 1rem;
        position: relative;
        z-index: 1;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
    }

    /* Wheel-Style Rotating Capsule */
    .wheel-capsule-container {
        display: flex;
        justify-content: center;
        align-items: center;
        margin-bottom: 1.1rem;
    }

    .wheel-capsule {
        width: 72px;
        height: 72px;
        display: flex;
        align-items: center;
        justify-content: center;
        animation: wheelSpin 3.5s linear infinite;
        transform-origin: center center;
    }

    @keyframes wheelSpin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }

    .capsule-pill {
        width: 24px;
        height: 64px;
        border-radius: 999px;
        position: relative;
        overflow: hidden;
        box-shadow: 0 0 25px rgba(244, 63, 94, 0.55), 0 0 25px rgba(99, 102, 241, 0.55);
        border: 1px solid rgba(255, 255, 255, 0.25);
    }

    .capsule-pill .half-red {
        width: 100%;
        height: 50%;
        background: linear-gradient(135deg, #f43f5e, #be123c);
    }

    .capsule-pill .half-white {
        width: 100%;
        height: 50%;
        background: linear-gradient(135deg, #ffffff, #e2e8f0);
    }

    .capsule-pill .gloss-line {
        position: absolute;
        top: 5px;
        left: 4px;
        width: 5px;
        height: 54px;
        border-radius: 999px;
        background: linear-gradient(to bottom, rgba(255,255,255,0.95), rgba(255,255,255,0.1));
    }

    /* Badge */
    .badge-pill {
        display: inline-flex;
        align-items: center;
        gap: 7px;
        background: rgba(99, 102, 241, 0.15);
        border: 1px solid rgba(99, 102, 241, 0.4);
        color: #a5b4fc;
        font-size: 0.78rem;
        font-weight: 600;
        letter-spacing: 0.05em;
        text-transform: uppercase;
        padding: 5px 14px;
        border-radius: 999px;
        margin-bottom: 0.8rem;
        box-shadow: 0 4px 14px rgba(99, 102, 241, 0.2);
        backdrop-filter: blur(8px);
    }

    .badge-dot {
        width: 7px;
        height: 7px;
        background: #34d399;
        border-radius: 50%;
        box-shadow: 0 0 8px #34d399;
        animation: pulseDot 2s infinite;
    }

    @keyframes pulseDot {
        0%, 100% { opacity: 1; transform: scale(1); }
        50% { opacity: 0.5; transform: scale(0.85); }
    }

    .hero-title {
        font-size: 3.2rem;
        font-weight: 800;
        letter-spacing: -0.03em;
        background: linear-gradient(135deg, #ffffff 30%, #cbd5e1 70%, #94a3b8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
        line-height: 1.1;
        text-align: center;
    }

    .hero-subtitle {
        color: #94a3b8;
        font-size: 1.05rem;
        font-weight: 400;
        line-height: 1.6;
        text-align: center;
        max-width: 660px;
        margin: 0.7rem auto 0 auto;
        text-wrap: balance;
    }

    /* Side-by-Side Panel Boxes */
    .panel-box {
        background: rgba(15, 23, 42, 0.65);
        border: 1px solid rgba(255, 255, 255, 0.09);
        border-radius: 16px;
        padding: 1.4rem 1.6rem 1.2rem 1.6rem;
        margin-bottom: 1rem;
        backdrop-filter: blur(14px);
        box-shadow: 0 12px 28px rgba(0, 0, 0, 0.25);
    }

    .panel-title {
        font-size: 0.92rem;
        font-weight: 700;
        color: #f8fafc;
        letter-spacing: 0.06em;
        text-transform: uppercase;
        margin-bottom: 0.3rem;
    }

    .panel-desc {
        font-size: 0.86rem;
        color: #64748b;
        line-height: 1.45;
    }

    /* Input Styling */
    .stTextInput > div > div > input {
        background: rgba(2, 6, 23, 0.65) !important;
        border: 1px solid rgba(255, 255, 255, 0.12) !important;
        border-radius: 12px !important;
        color: #f8fafc !important;
        font-size: 0.98rem !important;
        padding: 0.85rem 1.1rem !important;
        transition: all 0.2s ease !important;
    }

    .stTextInput > div > div > input:focus {
        border-color: #818cf8 !important;
        box-shadow: 0 0 0 3px rgba(129, 140, 248, 0.2) !important;
    }

    /* Action Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 50%, #06b6d4 100%) !important;
        color: #ffffff !important;
        font-weight: 700 !important;
        font-size: 0.98rem !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.75rem 1.8rem !important;
        width: 100% !important;
        box-shadow: 0 8px 22px rgba(79, 70, 229, 0.35) !important;
        transition: transform 0.18s ease, box-shadow 0.18s ease !important;
        letter-spacing: 0.02em !important;
        margin-top: 0.6rem !important;
    }

    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 12px 28px rgba(79, 70, 229, 0.5) !important;
    }

    /* Medical Report Card */
    .medical-report-card {
        background: linear-gradient(180deg, rgba(15, 23, 42, 0.88) 0%, rgba(13, 27, 42, 0.92) 100%);
        border: 1px solid rgba(52, 211, 153, 0.3);
        border-radius: 18px;
        padding: 2.2rem;
        margin-top: 2rem;
        box-shadow: 0 24px 48px rgba(0, 0, 0, 0.45), 0 0 35px rgba(52, 211, 153, 0.1);
        backdrop-filter: blur(20px);
    }

    .medical-report-card h2 {
        color: #34d399 !important;
        font-size: 1.75rem !important;
        font-weight: 800 !important;
        border-bottom: 1px solid rgba(255, 255, 255, 0.09);
        padding-bottom: 0.8rem;
        margin-bottom: 1.3rem;
        letter-spacing: -0.02em;
    }

    .medical-report-card h3 {
        color: #a5b4fc !important;
        font-size: 1.15rem !important;
        font-weight: 700 !important;
        margin-top: 1.4rem !important;
        margin-bottom: 0.4rem !important;
        letter-spacing: -0.01em;
    }

    .medical-report-card p, .medical-report-card li {
        color: #e2e8f0 !important;
        font-size: 0.98rem !important;
        line-height: 1.7 !important;
    }

    /* Detection Info Banner */
    .scan-badge {
        background: rgba(56, 189, 248, 0.12);
        border: 1px solid rgba(56, 189, 248, 0.35);
        color: #38bdf8;
        padding: 0.8rem 1.2rem;
        border-radius: 12px;
        margin-top: 1.5rem;
        font-size: 0.95rem;
        font-weight: 600;
    }

    /* Disclaimer Box */
    .disclaimer-banner {
        background: rgba(245, 158, 11, 0.08);
        border: 1px solid rgba(245, 158, 11, 0.28);
        border-radius: 12px;
        padding: 0.9rem 1.2rem;
        color: #fde68a;
        font-size: 0.88rem;
        line-height: 1.55;
        margin-top: 1.5rem;
    }
</style>
""", unsafe_allow_html=True)

# ── Gemini Client Setup ───────────────────────────────────────────────────────
client = genai.Client()
MODEL = "gemma-4-26b-a4b-it"
VISION_MODEL = "gemini-3.5-flash-lite"

# ── Professional Medical Prompt (No Emojis) ───────────────────────────────────
SYSTEM_PROMPT = """You are a professional clinical assistant called "Dawai Samjho".
Explain the given medicine clearly in balanced Roman Urdu and simple English for patients and families in Pakistan.

Respond ONLY in this structured markdown format (do NOT include any emojis):

## [Full Medicine Brand Name & Active Composition]

### Purpose & Indication (Kis Liye Hai)
[2-3 clear, simple sentences in easy Roman Urdu explaining what medical condition this medicine treats]

### Dosage & Timing (Kab Aur Kaise Leni Hai)
[Specific instructions on when and how to take it: khane ke baad ya pehle, din mein kitni martaba]

### Common Side Effects (Aam Nuqsanat)
[3-4 bullet points detailing common mild side effects]

### Precautions & Interactions (Parhez Aur Ehtiyat)
[Foods, drinks, or other habits to strictly avoid while taking this medicine]

### Emergency Warning Signs (Doctor Ko Kab Dikhana Hai)
[2-3 severe symptoms indicating the patient must stop the medication and consult a physician immediately]

Keep the language professional, respectful, accurate, and completely free of emojis."""

# ── Resilient Analysis Functions ──────────────────────────────────────────────
def analyze_by_name(medicine_name: str) -> str:
    """Explains medicine using Gemma 4 with resilient retry/fallback."""
    prompt = f"{SYSTEM_PROMPT}\n\nMedicine name or prescription text to analyze:\n{medicine_name}"

    for _ in range(2):
        try:
            response = client.models.generate_content(
                model=MODEL,
                contents=prompt,
            )
            if response and response.text:
                return response.text
        except Exception:
            time.sleep(1)

    try:
        response = client.models.generate_content(
            model=VISION_MODEL,
            contents=prompt,
        )
        return response.text
    except Exception as e:
        raise e


def extract_text_from_image(image_bytes: bytes, mime_type: str) -> str:
    """Uses high-speed vision to accurately detect medicine details from photos."""
    prompt = (
        "You are an expert pharmacist and OCR scanner. "
        "Carefully read all visible text on this medicine package, blister strip, box, bottle, or prescription. "
        "Extract the exact brand name, active ingredients (generic formula), and strength (e.g. 500mg, 650mg). "
        "Return just the clean, concise detected medicine details without emojis."
    )
    response = client.models.generate_content(
        model=VISION_MODEL,
        contents=[
            types.Part.from_bytes(data=image_bytes, mime_type=mime_type),
            prompt,
        ],
    )
    return response.text.strip()


def analyze_by_image(image_bytes: bytes, mime_type: str) -> tuple[str, str]:
    """Scans image with vision, then performs full medical breakdown with Gemma 4."""
    detected_info = extract_text_from_image(image_bytes, mime_type)
    explanation = analyze_by_name(detected_info)
    return detected_info, explanation


# ── Hero Section with Continuous Wheel-Spinning Capsule ───────────────────────
st.markdown("""
<div class="hero-container">
    <div class="wheel-capsule-container">
        <div class="wheel-capsule" title="Dawai Samjho AI">
            <div class="capsule-pill">
                <div class="half-red"></div>
                <div class="half-white"></div>
                <div class="gloss-line"></div>
            </div>
        </div>
    </div>
    <div class="badge-pill">
        <span class="badge-dot"></span>
        <span>Powered by Gemma 4</span>
    </div>
    <h1 class="hero-title">Dawai Samjho</h1>
    <p class="hero-subtitle">
        Prescription ya medicine ki photo upload karein — AI apko simple Roman Urdu aur English mein mukammal tafseel samjhaye ga.
    </p>
</div>
""", unsafe_allow_html=True)

# ── Side-by-Side Sections Layout ──────────────────────────────────────────────
col_left, col_right = st.columns(2, gap="large")

with col_left:
    st.markdown("""
    <div class="panel-box">
        <div class="panel-title">Photo Scanner</div>
        <div class="panel-desc">Upload a photo of your medicine box, blister strip, or doctor prescription (JPG or PNG)</div>
    </div>
    """, unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        "Upload Medicine Photo",
        type=["jpg", "jpeg", "png"],
        label_visibility="collapsed",
    )

    if uploaded_file:
        st.image(uploaded_file, caption="Selected Medicine Photo", width="stretch")

    btn_scan = st.button("Scan & Analyze Photo", key="btn_scan_img")

with col_right:
    st.markdown("""
    <div class="panel-box">
        <div class="panel-title">Direct Search</div>
        <div class="panel-desc">Type any medicine brand name or active generic formula directly</div>
    </div>
    """, unsafe_allow_html=True)

    medicine_input = st.text_input(
        "Medicine Search Input",
        placeholder="e.g. Nuberol Forte, Panadol, Augmentin 625mg, Brufen 400...",
        label_visibility="collapsed",
    )

    btn_search = st.button("Analyze Medicine Name", key="btn_analyze_text")

# ── Report Container ──────────────────────────────────────────────────────────
if btn_scan and uploaded_file:
    with st.spinner("Analyzing image details and generating medical guidance report..."):
        try:
            img_bytes = uploaded_file.getvalue()
            ext = uploaded_file.name.split(".")[-1].lower()
            mime_type = "image/png" if ext == "png" else "image/jpeg"

            detected_name, report = analyze_by_image(img_bytes, mime_type)

            st.markdown(f"""
            <div class="scan-badge">
                <b>Detected from Image:</b> {detected_name}
            </div>
            """, unsafe_allow_html=True)

            st.markdown(f"""
            <div class="medical-report-card">
                {report}
            </div>
            """, unsafe_allow_html=True)

            st.markdown("""
            <div class="disclaimer-banner">
                <b>Medical Disclaimer:</b> This application provides general educational guidance only. Always consult a licensed physician or certified pharmacist before starting, changing, or discontinuing any prescribed treatment.
            </div>
            """, unsafe_allow_html=True)

        except Exception as e:
            st.error(f"Error during analysis: {e}")

elif btn_scan and not uploaded_file:
    st.warning("Please upload a medicine photo first.")

if btn_search:
    if medicine_input.strip():
        with st.spinner("Reviewing pharmaceutical details with Gemma 4..."):
            try:
                report = analyze_by_name(medicine_input.strip())

                st.markdown(f"""
                <div class="medical-report-card">
                    {report}
                </div>
                """, unsafe_allow_html=True)

                st.markdown("""
                <div class="disclaimer-banner">
                    <b>Medical Disclaimer:</b> This application provides general educational guidance only. Always consult a licensed physician or certified pharmacist before starting, changing, or discontinuing any prescribed treatment.
                </div>
                """, unsafe_allow_html=True)

            except Exception as e:
                st.error(f"Error during analysis: {e}")
    else:
        st.warning("Please enter a medicine name.")

# ── Professional Clean Footer ─────────────────────────────────────────────────
st.markdown("""
<div style="text-align: center; margin-top: 4rem; padding-bottom: 2rem; color: #475569; font-size: 0.82rem; letter-spacing: 0.02em;">
    Built for <b>Hacktoberfest Faisalabad</b> · Powered by <b>Gemma 4</b> (Apache 2.0)
</div>
""", unsafe_allow_html=True)
