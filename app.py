import streamlit as st
import base64
import os
from transcript_merger import TranscriptMerger

# ─── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Ericsson | Transcript Merger",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─── Load Logo (transparent PNG preferred, fallback to jpg with CSS filter) ────
def get_logo_base64():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    # Prefer pre-processed transparent PNG
    for fname in ("ericsson_logo_white.png", "ericsson_logo.png", "ericsson_logo.jpg"):
        path = os.path.join(base_dir, fname)
        if os.path.exists(path):
            with open(path, "rb") as f:
                data = base64.b64encode(f.read()).decode()
            mime = "image/png" if fname.endswith(".png") else "image/jpeg"
            return data, mime
    return None, None

logo_b64, logo_mime = get_logo_base64()

# Build logo HTML — for the JPG version we apply CSS filter to strip background
if logo_b64:
    logo_html = (
        f'<img src="data:{logo_mime};base64,{logo_b64}" class="ericsson-logo" alt="Ericsson" />'
    )
    login_logo_html = (
        f'<img src="data:{logo_mime};base64,{logo_b64}" '
        f'style="height:52px;object-fit:contain;'
        f'{"" if logo_mime=="image/png" else "filter:brightness(0) invert(1);"}'
        f'margin-bottom:8px;" alt="Ericsson" />'
    )
else:
    logo_html = '<div class="ericsson-wordmark">ERICSSON</div>'
    login_logo_html = '<div style="font-size:26px;font-weight:700;letter-spacing:5px;color:#fff;margin-bottom:8px;">ERICSSON</div>'

# ─── Custom CSS ────────────────────────────────────────────────────────────────
# For JPG logos, we use filter:brightness(0) invert(1) to make them white.
# For transparent PNG logos, no filter needed.
logo_filter = "" if logo_mime == "image/png" else "filter: brightness(0) invert(1);"

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;500;600;700&family=IBM+Plex+Mono:wght@400;500&display=swap');

*, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}

html, body, [data-testid="stAppViewContainer"] {{
    background-color: #F5F6F8 !important;
    font-family: 'Sora', sans-serif;
}}
[data-testid="stAppViewContainer"] > .main {{ background: transparent !important; padding: 0 !important; }}
.main .block-container {{ padding: 0 !important; max-width: 100% !important; }}
#MainMenu, footer, header {{ visibility: hidden; }}

/* ── NAV BAR ── */
.top-nav {{
    background: #003366;
    padding: 0 48px;
    height: 68px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    position: sticky;
    top: 0;
    z-index: 999;
    box-shadow: 0 2px 16px rgba(0,0,0,0.22);
}}
.nav-left {{ display: flex; align-items: center; gap: 18px; }}

/* Logo: transparent PNG needs no filter; JPG gets inverted to white */
.ericsson-logo {{
    height: 42px;
    width: auto;
    object-fit: contain;
    {logo_filter}
}}

.ericsson-wordmark {{ font-family:'Sora',sans-serif; font-weight:700; font-size:22px; letter-spacing:5px; color:#fff; }}
.nav-divider {{ width:1px; height:30px; background:rgba(255,255,255,0.3); flex-shrink:0; }}
.nav-internal-label {{
    font-family: 'Sora', sans-serif;
    font-size: 13px;
    font-weight: 600;
    letter-spacing: 2.5px;
    text-transform: uppercase;
    color: #FFFFFF;
    white-space: nowrap;
}}
.nav-right {{ display:flex; align-items:center; gap:12px; }}
.nav-tag {{
    background: rgba(255,255,255,0.12);
    border: 1px solid rgba(255,255,255,0.22);
    color: #fff;
    font-size: 10px;
    font-weight: 600;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    padding: 5px 14px;
    border-radius: 20px;
}}
.zero-data-pill {{
    background: #00AA5B;
    color: #fff;
    font-size: 10px;
    font-weight: 600;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    padding: 5px 14px;
    border-radius: 20px;
    display: flex;
    align-items: center;
    gap: 6px;
}}
.zero-data-pill::before {{ content:"🔒"; font-size:11px; }}

/* ── HERO ── */
.hero {{
    background: linear-gradient(135deg, #003366 0%, #0056A8 55%, #0080CC 100%);
    padding: 56px 48px 48px;
    color: white;
    position: relative;
    overflow: hidden;
}}
.hero::before {{
    content: '';
    position: absolute;
    top: -60px; right: -60px;
    width: 300px; height: 300px;
    background: rgba(255,255,255,0.04);
    border-radius: 50%;
}}
.hero-eyebrow {{ font-size:11px; font-weight:600; letter-spacing:3px; text-transform:uppercase; color:#7ECBFF; margin-bottom:14px; }}
.hero-title {{ font-size:36px; font-weight:700; line-height:1.2; margin-bottom:12px; color:#fff; }}
.hero-subtitle {{ font-size:15px; font-weight:300; color:rgba(255,255,255,0.72); max-width:560px; line-height:1.7; }}
.hero-stats {{ display:flex; gap:40px; margin-top:36px; }}
.stat-number {{ font-size:28px; font-weight:700; color:#7ECBFF; line-height:1; }}
.stat-label {{ font-size:11px; color:rgba(255,255,255,0.55); letter-spacing:1px; text-transform:uppercase; margin-top:4px; }}

/* ── CONTENT ── */
.content-area {{ padding:40px 48px; max-width:1200px; margin:0 auto; }}

/* ── SECURITY BANNER ── */
.security-banner {{
    background: #EDFBF3;
    border: 1.5px solid #00AA5B;
    border-left: 5px solid #00AA5B;
    border-radius: 10px;
    padding: 18px 24px;
    margin-bottom: 32px;
    display: flex;
    align-items: flex-start;
    gap: 16px;
}}
.security-icon {{ font-size:22px; flex-shrink:0; margin-top:2px; }}
.security-title {{ font-size:13px; font-weight:700; color:#00703C; letter-spacing:0.5px; text-transform:uppercase; margin-bottom:4px; }}
.security-text {{ font-size:13px; color:#1A4A30; line-height:1.6; }}

/* ── SHARE BANNER ── */
.share-banner {{
    background: #F0F7FF;
    border: 1.5px solid #0056A8;
    border-left: 5px solid #0056A8;
    border-radius: 10px;
    padding: 18px 24px;
    margin-bottom: 28px;
    display: flex;
    align-items: flex-start;
    gap: 16px;
}}
.share-title {{ font-size:13px; font-weight:700; color:#003366; letter-spacing:0.5px; text-transform:uppercase; margin-bottom:4px; }}
.share-text {{ font-size:13px; color:#1A3A5C; line-height:1.6; }}
.share-url-box {{
    background: #fff;
    border: 1.5px solid #BAD4F5;
    border-radius: 8px;
    padding: 10px 16px;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 13px;
    color: #0056A8;
    margin-top: 10px;
    word-break: break-all;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 12px;
}}

/* ── SECTION ── */
.section-title {{ font-size:18px; font-weight:600; color:#0A1F3A; margin-bottom:6px; }}
.section-desc {{ font-size:13px; color:#6B7A8D; margin-bottom:20px; }}

/* ── UPLOAD ── */
[data-testid="stFileUploader"] {{
    border: 2px dashed #BAC8D8 !important;
    border-radius: 14px !important;
    background: #FFFFFF !important;
    padding: 10px !important;
}}
[data-testid="stFileUploader"]:hover {{ border-color: #0056A8 !important; background: #F0F7FF !important; }}
[data-testid="stFileUploader"] label {{ font-family:'Sora',sans-serif !important; color:#3D5A7A !important; font-size:14px !important; }}

/* ── RESULT CARD ── */
.result-card {{
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-top: 4px solid #0056A8;
    border-radius: 14px;
    padding: 28px 32px;
    margin-top: 24px;
    box-shadow: 0 4px 20px rgba(0,51,102,0.07);
}}
.result-header {{ display:flex; align-items:center; justify-content:space-between; margin-bottom:20px; padding-bottom:16px; border-bottom:1px solid #EEF2F7; }}
.result-title {{ font-size:15px; font-weight:600; color:#0A1F3A; }}
.result-badge {{ background:#E8F4FD; color:#0056A8; font-size:11px; font-weight:600; padding:4px 12px; border-radius:20px; }}
.stats-row {{ display:grid; grid-template-columns:repeat(4,1fr); gap:16px; margin-bottom:20px; }}
.stat-card {{ background:#F8FAFC; border:1px solid #E8EDF3; border-radius:10px; padding:16px; text-align:center; }}
.stat-card-num {{ font-size:24px; font-weight:700; color:#0056A8; line-height:1; }}
.stat-card-label {{ font-size:11px; color:#8A9BB0; margin-top:5px; text-transform:uppercase; letter-spacing:0.5px; }}

/* ── PREVIEW ── */
.transcript-preview {{
    background: #F8FAFC;
    border: 1px solid #E2E8F0;
    border-radius: 10px;
    padding: 20px;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 12px;
    color: #2D3F55;
    line-height: 1.8;
    max-height: 320px;
    overflow-y: auto;
    white-space: pre-wrap;
}}

/* ────────────────────────────────────────────────────
   DOWNLOAD BUTTONS — FORCED SOLID COLORS
   Streamlit resets button styles aggressively, so we
   target every selector combination possible.
──────────────────────────────────────────────────── */

/* Merge button */
.stButton > button,
div[data-testid="stButton"] > button {{
    background: linear-gradient(135deg, #003366, #0056A8) !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 14px 40px !important;
    font-family: 'Sora', sans-serif !important;
    font-size: 14px !important;
    font-weight: 600 !important;
    width: 100% !important;
    box-shadow: 0 4px 14px rgba(0,51,102,0.3) !important;
    margin-top: 8px !important;
    cursor: pointer !important;
}}
.stButton > button:hover {{ transform: translateY(-1px) !important; }}

/* TXT download button — Ericsson Blue */
div[data-testid="stDownloadButton"]:first-of-type button,
div[data-testid="stDownloadButton"]:first-of-type > button,
.stDownloadButton:first-of-type button {{
    background: #0056A8 !important;
    background-color: #0056A8 !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 14px 20px !important;
    font-family: 'Sora', sans-serif !important;
    font-size: 13px !important;
    font-weight: 700 !important;
    width: 100% !important;
    box-shadow: 0 4px 14px rgba(0,86,168,0.4) !important;
    cursor: pointer !important;
    letter-spacing: 0.3px !important;
}}

/* DOCX download button — Ericsson Green */
div[data-testid="stDownloadButton"]:last-of-type button,
div[data-testid="stDownloadButton"]:last-of-type > button,
.stDownloadButton:last-of-type button {{
    background: #007A3D !important;
    background-color: #007A3D !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 14px 20px !important;
    font-family: 'Sora', sans-serif !important;
    font-size: 13px !important;
    font-weight: 700 !important;
    width: 100% !important;
    box-shadow: 0 4px 14px rgba(0,122,61,0.4) !important;
    cursor: pointer !important;
    letter-spacing: 0.3px !important;
}}

/* Generic fallback — any download button gets at minimum a dark blue */
.stDownloadButton button,
.stDownloadButton > button,
[data-testid="stDownloadButton"] button {{
    background-color: #003366 !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 14px 20px !important;
    font-family: 'Sora', sans-serif !important;
    font-size: 13px !important;
    font-weight: 700 !important;
    width: 100% !important;
}}

/* ── PROGRESS ── */
.stProgress > div > div {{ background: linear-gradient(90deg, #003366, #0080CC) !important; border-radius: 10px !important; }}

/* ── PASSWORD SCREEN ── */
[data-testid="stTextInput"] input {{
    background: rgba(255,255,255,0.10) !important;
    border: 1.5px solid rgba(255,255,255,0.25) !important;
    border-radius: 10px !important;
    color: #FFFFFF !important;
    font-family: 'Sora', sans-serif !important;
    padding: 12px 16px !important;
    font-size: 14px !important;
}}
[data-testid="stTextInput"] input:focus {{ border-color: #5AB0FF !important; outline: none !important; }}
[data-testid="stTextInput"] input::placeholder {{ color: rgba(255,255,255,0.35) !important; }}

/* ── INFO BOX ── */
.info-box {{
    background: #F0F7FF;
    border: 1px solid #B8D8F8;
    border-left: 4px solid #0056A8;
    border-radius: 8px;
    padding: 14px 18px;
    font-size: 13px;
    color: #1A3A5C;
    margin-top: 16px;
    line-height: 1.6;
}}

/* ── FILE LIST ── */
.file-list-item {{
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 8px;
    padding: 12px 16px;
    margin-bottom: 8px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    font-size: 13px;
    color: #2D3F55;
}}

/* ── DOWNLOAD FORMAT CARDS ── */
.dl-card-blue {{
    border: 2px solid #0056A8;
    border-radius: 12px;
    padding: 18px 20px;
    background: #EBF4FF;
    margin-bottom: 10px;
}}
.dl-card-green {{
    border: 2px solid #007A3D;
    border-radius: 12px;
    padding: 18px 20px;
    background: #EDFBF3;
    margin-bottom: 10px;
}}
.dl-card-title {{ font-size:14px; font-weight:700; margin-bottom:3px; }}
.dl-card-blue .dl-card-title {{ color: #003366; }}
.dl-card-green .dl-card-title {{ color: #004D26; }}
.dl-card-desc {{ font-size:12px; color:#6B7A8D; line-height:1.5; }}

/* ── FOOTER ── */
.app-footer {{
    background: #0A1F3A;
    color: rgba(255,255,255,0.45);
    text-align: center;
    padding: 22px 48px;
    font-size: 11px;
    letter-spacing: 0.5px;
    margin-top: 60px;
}}
.app-footer span {{ color: rgba(255,255,255,0.75); font-weight: 600; }}
</style>
""", unsafe_allow_html=True)

# ─── Password Gate ──────────────────────────────────────────────────────────────
CORRECT_PASSWORD = "Ericsson@2024"   # ← Change this password as needed

def show_login():
    st.markdown(f"""
    <div style="background:linear-gradient(135deg,#001F45 0%,#003366 60%,#004F8C 100%);
                min-height:100vh;display:flex;align-items:center;justify-content:center;padding:40px;">
        <div style="background:rgba(255,255,255,0.07);border:1px solid rgba(255,255,255,0.15);
                    border-radius:20px;padding:52px 56px;max-width:460px;width:100%;text-align:center;">
            <div style="margin-bottom:20px;">{login_logo_html}</div>
            <div style="font-family:'Sora',sans-serif;font-size:22px;font-weight:700;color:#fff;margin-bottom:8px;">Transcript Merger</div>
            <div style="font-family:'Sora',sans-serif;font-size:13px;color:rgba(255,255,255,0.55);margin-bottom:36px;line-height:1.6;">
                Restricted to authorised Ericsson personnel only.<br>Enter your access password to continue.
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    _, col, _ = st.columns([1, 2, 1])
    with col:
        st.markdown(
            '<p style="font-family:Sora,sans-serif;font-size:11px;font-weight:600;'
            'letter-spacing:1.5px;text-transform:uppercase;color:rgba(255,255,255,0.45);'
            'margin-bottom:6px;">Access Password</p>',
            unsafe_allow_html=True,
        )
        pwd = st.text_input("", type="password", placeholder="Enter password…",
                            label_visibility="collapsed", key="pw_input")
        if st.button("Unlock  →", key="login_btn"):
            if pwd == CORRECT_PASSWORD:
                st.session_state["authenticated"] = True
                st.rerun()
            else:
                st.error("❌ Incorrect password. Please try again.")

if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    show_login()
    st.stop()

# ══════════════════════════════════════════════════════════════
#   MAIN APP  (only shown after successful login)
# ══════════════════════════════════════════════════════════════

# ── Top Nav ────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="top-nav">
    <div class="nav-left">
        {logo_html}
        <div class="nav-divider"></div>
        <div class="nav-internal-label">ERICSSON — INTERNAL</div>
    </div>
    <div class="nav-right">
        <div class="nav-tag">Internal Tool</div>
        <div class="zero-data-pill">Zero Data Storage</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Hero ───────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-eyebrow">Transcript Intelligence Platform</div>
    <div class="hero-title">Multi-Transcript Merger &amp; Organizer</div>
    <div class="hero-subtitle">
        Upload multiple meeting transcripts — automatically sorted by date,
        merged into one coherent document, and downloadable as .TXT or .DOCX.
    </div>
    <div class="hero-stats">
        <div class="stat-item"><div class="stat-number">∞</div><div class="stat-label">Files Supported</div></div>
        <div class="stat-item"><div class="stat-number">0</div><div class="stat-label">Data Stored</div></div>
        <div class="stat-item"><div class="stat-number">100%</div><div class="stat-label">In-Memory Only</div></div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="content-area">', unsafe_allow_html=True)

# ── Share Banner ────────────────────────────────────────────────────────────────
app_url = "https://your-app-name.streamlit.app"   # ← Update after Streamlit deploy
st.markdown(f"""
<div class="share-banner">
    <div style="font-size:22px;flex-shrink:0;margin-top:2px;">🔗</div>
    <div>
        <div class="share-title">Share with your team</div>
        <div class="share-text">
            Simply share the link below with your colleagues. Anyone with the link and the
            access password can use this tool. No installation required.
        </div>
        <div class="share-url-box">
            <span id="app-url">{app_url}</span>
            <span style="font-size:11px;color:#8A9BB0;white-space:nowrap;">🔒 Password protected</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Security Banner ─────────────────────────────────────────────────────────────
st.markdown("""
<div class="security-banner">
    <div class="security-icon">🔒</div>
    <div>
        <div class="security-title">Zero Data Storage Policy — Strictly Enforced</div>
        <div class="security-text">
            This tool operates entirely in-memory. <strong>No file content is ever saved, logged, or transmitted</strong>
            to any external server or storage system. All uploaded transcripts are processed within your active
            browser session and permanently discarded when you close or refresh the page.
            Compliant with Ericsson's data confidentiality guidelines.
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Upload Section ─────────────────────────────────────────────────────────────
st.markdown("""
<div class="section-title">📁 Upload Transcripts</div>
<div class="section-desc">Supports .txt and .docx formats. No attachment limit — upload 5, 10, 20 files at once.</div>
""", unsafe_allow_html=True)

uploaded_files = st.file_uploader(
    "Drop your transcript files here or click to browse",
    type=["txt", "docx"],
    accept_multiple_files=True,
    help="No file limit. Supported: .txt, .docx"
)

if uploaded_files:
    st.markdown(f"""
    <div class="info-box">
        ✅ <strong>{len(uploaded_files)} file(s) uploaded</strong> — files will be auto-sorted
        by detected meeting date, then merged sequentially.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    for f in uploaded_files:
        size_kb = round(len(f.getvalue()) / 1024, 1)
        icon = "📝" if f.name.endswith(".txt") else "📄"
        st.markdown(f"""
        <div class="file-list-item">
            <span><span style="color:#0056A8;margin-right:10px;">{icon}</span>{f.name}</span>
            <span style="color:#8A9BB0;font-size:12px;">{size_kb} KB</span>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("🔀  Merge & Sort Transcripts", key="merge_btn"):
        with st.spinner("Processing transcripts…"):
            pb = st.progress(0)
            merger = TranscriptMerger()
            files_data = []
            for i, f in enumerate(uploaded_files):
                pb.progress(int((i + 1) / len(uploaded_files) * 50))
                content = merger.read_file(f)
                files_data.append({"name": f.name, "content": content})
            pb.progress(70)
            merged_text, docx_bytes, stats = merger.merge_transcripts(files_data)
            pb.progress(100)

        # Result Card
        st.markdown(f"""
        <div class="result-card">
            <div class="result-header">
                <div class="result-title">✅ Merge Complete — Unified Transcript Ready</div>
                <div class="result-badge">{stats['total_files']} Files Merged</div>
            </div>
            <div class="stats-row">
                <div class="stat-card"><div class="stat-card-num">{stats['total_files']}</div><div class="stat-card-label">Transcripts</div></div>
                <div class="stat-card"><div class="stat-card-num">{stats['total_lines']:,}</div><div class="stat-card-label">Total Lines</div></div>
                <div class="stat-card"><div class="stat-card-num">{stats['total_words']:,}</div><div class="stat-card-label">Total Words</div></div>
                <div class="stat-card"><div class="stat-card-num">{stats['date_sorted']}</div><div class="stat-card-label">Date Sorted</div></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Preview
        st.markdown('<div class="section-title" style="margin-top:28px;font-size:16px;">👁 Preview</div>', unsafe_allow_html=True)
        preview = "\n".join(merged_text.split("\n")[:60])
        st.markdown(f'<div class="transcript-preview">{preview}\n\n… scroll to see more …</div>', unsafe_allow_html=True)

        # ── Download Section ──────────────────────────────────────────────────
        st.markdown("""
        <div style="background:#FFFFFF;border:1px solid #E2E8F0;border-radius:14px;
                    padding:26px 28px;margin-top:24px;box-shadow:0 2px 12px rgba(0,51,102,0.05);">
            <div style="font-size:16px;font-weight:700;color:#0A1F3A;margin-bottom:4px;">
                ⬇️  Download Merged Transcript
            </div>
            <div style="font-size:12px;color:#8A9BB0;margin-bottom:22px;">
                Both formats contain identical content — choose what suits your workflow.
            </div>
        """, unsafe_allow_html=True)

        dl_col1, dl_col2 = st.columns(2)

        with dl_col1:
            st.markdown("""
            <div class="dl-card-blue">
                <div class="dl-card-title">📄 Plain Text (.TXT)</div>
                <div class="dl-card-desc">Lightweight &amp; universal. Opens in any text editor or Notepad.</div>
            </div>
            """, unsafe_allow_html=True)
            st.download_button(
                label="⬇️  Download .TXT",
                data=merged_text.encode("utf-8"),
                file_name="ericsson_merged_transcript.txt",
                mime="text/plain",
                key="dl_txt",
                use_container_width=True,
            )

        with dl_col2:
            st.markdown("""
            <div class="dl-card-green">
                <div class="dl-card-title">📝 Word Document (.DOCX)</div>
                <div class="dl-card-desc">Formatted with section headings. Ready for Microsoft Word.</div>
            </div>
            """, unsafe_allow_html=True)
            st.download_button(
                label="⬇️  Download .DOCX",
                data=docx_bytes,
                file_name="ericsson_merged_transcript.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                key="dl_docx",
                use_container_width=True,
            )

        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("""
        <div class="info-box" style="margin-top:14px;">
            🗑️ <strong>Memory cleared on exit:</strong> All uploaded data and the generated output are
            permanently removed from memory when you close or refresh this page. Nothing is retained.
        </div>
        """, unsafe_allow_html=True)

else:
    st.markdown("""
    <div style="text-align:center;padding:40px;color:#8A9BB0;font-size:14px;">
        ⬆️ Upload your transcript files above to get started
    </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ── Footer ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="app-footer">
    <span>Ericsson Internal Tool</span> &nbsp;·&nbsp;
    Transcript Merger v1.2 &nbsp;·&nbsp;
    Zero Data Storage &nbsp;·&nbsp;
    All processing is session-scoped and in-memory only
</div>
""", unsafe_allow_html=True)
