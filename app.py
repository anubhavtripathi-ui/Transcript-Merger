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

# ─── Load Logo ─────────────────────────────────────────────────────────────────
def get_logo_base64():
    logo_path = os.path.join(os.path.dirname(__file__), "ericsson_logo.jpg")
    if os.path.exists(logo_path):
        with open(logo_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return None

logo_b64 = get_logo_base64()
logo_html = (
    f'<img src="data:image/jpeg;base64,{logo_b64}" class="ericsson-logo" alt="Ericsson" />'
    if logo_b64
    else '<div class="ericsson-wordmark">ERICSSON</div>'
)

# ─── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;500;600;700&family=IBM+Plex+Mono:wght@400;500&display=swap');

/* ── Reset & Base ── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [data-testid="stAppViewContainer"] {
    background-color: #F5F6F8 !important;
    font-family: 'Sora', sans-serif;
}

[data-testid="stAppViewContainer"] > .main {
    background: transparent !important;
    padding: 0 !important;
}

.main .block-container {
    padding: 0 !important;
    max-width: 100% !important;
}

/* Hide Streamlit branding */
#MainMenu, footer, header { visibility: hidden; }

/* ── Top Navigation Bar ── */
.top-nav {
    background: #003366;
    padding: 0 48px;
    height: 68px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    position: sticky;
    top: 0;
    z-index: 999;
    box-shadow: 0 2px 12px rgba(0,0,0,0.18);
}

.ericsson-logo {
    height: 40px;
    width: auto;
    object-fit: contain;
    filter: brightness(0) invert(1);
}

.ericsson-wordmark {
    font-family: 'Sora', sans-serif;
    font-weight: 700;
    font-size: 22px;
    letter-spacing: 4px;
    color: #FFFFFF;
}

.nav-right {
    display: flex;
    align-items: center;
    gap: 24px;
}

.nav-tag {
    background: rgba(255,255,255,0.12);
    border: 1px solid rgba(255,255,255,0.2);
    color: #ffffff;
    font-size: 11px;
    font-weight: 500;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    padding: 5px 14px;
    border-radius: 20px;
}

.zero-data-pill {
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
}

.zero-data-pill::before {
    content: "🔒";
    font-size: 11px;
}

/* ── Hero Section ── */
.hero {
    background: linear-gradient(135deg, #003366 0%, #0056A8 55%, #0080CC 100%);
    padding: 56px 48px 48px;
    color: white;
    position: relative;
    overflow: hidden;
}

.hero::before {
    content: '';
    position: absolute;
    top: -60px; right: -60px;
    width: 300px; height: 300px;
    background: rgba(255,255,255,0.04);
    border-radius: 50%;
}

.hero::after {
    content: '';
    position: absolute;
    bottom: -80px; left: 30%;
    width: 200px; height: 200px;
    background: rgba(255,255,255,0.03);
    border-radius: 50%;
}

.hero-eyebrow {
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: #7ECBFF;
    margin-bottom: 14px;
}

.hero-title {
    font-size: 36px;
    font-weight: 700;
    line-height: 1.2;
    margin-bottom: 12px;
    color: #FFFFFF;
}

.hero-subtitle {
    font-size: 15px;
    font-weight: 300;
    color: rgba(255,255,255,0.72);
    max-width: 540px;
    line-height: 1.7;
}

.hero-stats {
    display: flex;
    gap: 40px;
    margin-top: 36px;
}

.stat-item {
    text-align: left;
}

.stat-number {
    font-size: 28px;
    font-weight: 700;
    color: #7ECBFF;
    line-height: 1;
}

.stat-label {
    font-size: 11px;
    color: rgba(255,255,255,0.55);
    letter-spacing: 1px;
    text-transform: uppercase;
    margin-top: 4px;
}

/* ── Content Area ── */
.content-area {
    padding: 40px 48px;
    max-width: 1200px;
    margin: 0 auto;
}

/* ── Security Banner ── */
.security-banner {
    background: #EDFBF3;
    border: 1.5px solid #00AA5B;
    border-left: 5px solid #00AA5B;
    border-radius: 10px;
    padding: 18px 24px;
    margin-bottom: 32px;
    display: flex;
    align-items: flex-start;
    gap: 16px;
}

.security-icon { font-size: 22px; flex-shrink: 0; margin-top: 2px; }

.security-title {
    font-size: 13px;
    font-weight: 700;
    color: #00703C;
    letter-spacing: 0.5px;
    text-transform: uppercase;
    margin-bottom: 4px;
}

.security-text {
    font-size: 13px;
    color: #1A4A30;
    line-height: 1.6;
}

/* ── Section Title ── */
.section-title {
    font-size: 18px;
    font-weight: 600;
    color: #0A1F3A;
    margin-bottom: 6px;
    display: flex;
    align-items: center;
    gap: 10px;
}

.section-desc {
    font-size: 13px;
    color: #6B7A8D;
    margin-bottom: 20px;
}

/* ── Upload Zone ── */
[data-testid="stFileUploader"] {
    border: 2px dashed #BAC8D8 !important;
    border-radius: 14px !important;
    background: #FFFFFF !important;
    padding: 10px !important;
    transition: all 0.2s ease;
}

[data-testid="stFileUploader"]:hover {
    border-color: #0056A8 !important;
    background: #F0F7FF !important;
}

[data-testid="stFileUploader"] label {
    font-family: 'Sora', sans-serif !important;
    color: #3D5A7A !important;
    font-size: 14px !important;
}

/* ── Results Card ── */
.result-card {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-top: 4px solid #0056A8;
    border-radius: 14px;
    padding: 28px 32px;
    margin-top: 24px;
    box-shadow: 0 4px 20px rgba(0,51,102,0.07);
}

.result-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 20px;
    padding-bottom: 16px;
    border-bottom: 1px solid #EEF2F7;
}

.result-title {
    font-size: 15px;
    font-weight: 600;
    color: #0A1F3A;
}

.result-badge {
    background: #E8F4FD;
    color: #0056A8;
    font-size: 11px;
    font-weight: 600;
    padding: 4px 12px;
    border-radius: 20px;
    letter-spacing: 0.5px;
}

/* ── Stats Row ── */
.stats-row {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 16px;
    margin-bottom: 20px;
}

.stat-card {
    background: #F8FAFC;
    border: 1px solid #E8EDF3;
    border-radius: 10px;
    padding: 16px;
    text-align: center;
}

.stat-card-num {
    font-size: 24px;
    font-weight: 700;
    color: #0056A8;
    line-height: 1;
}

.stat-card-label {
    font-size: 11px;
    color: #8A9BB0;
    margin-top: 5px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

/* ── Transcript Preview ── */
.transcript-preview {
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
}

/* ── Process Button ── */
.stButton > button {
    background: linear-gradient(135deg, #003366, #0056A8) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 14px 40px !important;
    font-family: 'Sora', sans-serif !important;
    font-size: 14px !important;
    font-weight: 600 !important;
    letter-spacing: 0.5px !important;
    width: 100% !important;
    cursor: pointer !important;
    transition: all 0.25s ease !important;
    box-shadow: 0 4px 14px rgba(0,51,102,0.25) !important;
    margin-top: 8px !important;
}

.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 20px rgba(0,51,102,0.35) !important;
    background: linear-gradient(135deg, #002855, #004A92) !important;
}

/* ── Download Button ── */
.stDownloadButton > button {
    background: #00AA5B !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 12px 32px !important;
    font-family: 'Sora', sans-serif !important;
    font-size: 13px !important;
    font-weight: 600 !important;
    width: 100% !important;
    box-shadow: 0 4px 12px rgba(0,170,91,0.25) !important;
}

.stDownloadButton > button:hover {
    background: #008F4C !important;
    transform: translateY(-1px) !important;
}

/* ── Progress ── */
.stProgress > div > div {
    background: linear-gradient(90deg, #003366, #0080CC) !important;
    border-radius: 10px !important;
}

/* ── File List ── */
.file-list-item {
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
}

.file-icon { color: #0056A8; margin-right: 10px; }

/* ── Info Box ── */
.info-box {
    background: #F0F7FF;
    border: 1px solid #B8D8F8;
    border-left: 4px solid #0056A8;
    border-radius: 8px;
    padding: 14px 18px;
    font-size: 13px;
    color: #1A3A5C;
    margin-top: 16px;
    line-height: 1.6;
}

/* ── Footer ── */
.app-footer {
    background: #0A1F3A;
    color: rgba(255,255,255,0.45);
    text-align: center;
    padding: 20px 48px;
    font-size: 11px;
    letter-spacing: 0.5px;
    margin-top: 60px;
}

.app-footer span {
    color: rgba(255,255,255,0.7);
    font-weight: 500;
}
</style>
""", unsafe_allow_html=True)

# ─── Top Navigation ─────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="top-nav">
    {logo_html}
    <div class="nav-right">
        <div class="nav-tag">Internal Tool</div>
        <div class="zero-data-pill">Zero Data Storage</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ─── Hero ───────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-eyebrow">Transcript Intelligence Platform</div>
    <div class="hero-title">Multi-Transcript Merger &amp; Organizer</div>
    <div class="hero-subtitle">
        Upload multiple meeting transcripts — they will be automatically sorted by date,
        merged into a single coherent document, and made available for download.
    </div>
    <div class="hero-stats">
        <div class="stat-item">
            <div class="stat-number">∞</div>
            <div class="stat-label">Files Supported</div>
        </div>
        <div class="stat-item">
            <div class="stat-number">0</div>
            <div class="stat-label">Data Stored</div>
        </div>
        <div class="stat-item">
            <div class="stat-number">100%</div>
            <div class="stat-label">In-Memory Only</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ─── Content ────────────────────────────────────────────────────────────────────
st.markdown('<div class="content-area">', unsafe_allow_html=True)

# Security Banner
st.markdown("""
<div class="security-banner">
    <div class="security-icon">🔒</div>
    <div>
        <div class="security-title">Zero Data Storage Policy — Strictly Enforced</div>
        <div class="security-text">
            This tool operates entirely in-memory. <strong>No file content is ever saved, logged, or transmitted</strong>
            to any external server or storage system. All uploaded transcripts are processed locally within your
            active browser session and are permanently discarded the moment you close or refresh the page.
            This tool complies with Ericsson's data confidentiality guidelines.
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Upload Section
st.markdown("""
<div class="section-title">📁 Upload Transcripts</div>
<div class="section-desc">Supports .txt and .docx formats. Upload as many files as needed — no attachment limit.</div>
""", unsafe_allow_html=True)

uploaded_files = st.file_uploader(
    "Drop your transcript files here or click to browse",
    type=["txt", "docx"],
    accept_multiple_files=True,
    help="No file limit. Supported formats: .txt, .docx"
)

if uploaded_files:
    st.markdown(f"""
    <div class="info-box">
        ✅ <strong>{len(uploaded_files)} file(s) uploaded</strong> — ready to merge. 
        Files will be sorted by date extracted from content or filename, then merged sequentially.
    </div>
    """, unsafe_allow_html=True)

    # Show uploaded file list
    st.markdown("<br>", unsafe_allow_html=True)
    for f in uploaded_files:
        size_kb = round(len(f.getvalue()) / 1024, 1)
        icon = "📝" if f.name.endswith(".txt") else "📄"
        st.markdown(f"""
        <div class="file-list-item">
            <span><span class="file-icon">{icon}</span>{f.name}</span>
            <span style="color:#8A9BB0;font-size:12px;">{size_kb} KB</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Process Button
    if st.button("🔀  Merge & Sort Transcripts", key="merge_btn"):
        with st.spinner("Processing transcripts..."):
            progress_bar = st.progress(0)
            merger = TranscriptMerger()

            files_data = []
            for i, f in enumerate(uploaded_files):
                progress_bar.progress(int((i + 1) / len(uploaded_files) * 50))
                content = merger.read_file(f)
                files_data.append({"name": f.name, "content": content})

            progress_bar.progress(70)
            merged_output, stats = merger.merge_transcripts(files_data)
            progress_bar.progress(100)

        # Results Card
        st.markdown(f"""
        <div class="result-card">
            <div class="result-header">
                <div class="result-title">✅ Merge Complete — Unified Transcript Ready</div>
                <div class="result-badge">{stats['total_files']} Files Merged</div>
            </div>
            <div class="stats-row">
                <div class="stat-card">
                    <div class="stat-card-num">{stats['total_files']}</div>
                    <div class="stat-card-label">Transcripts</div>
                </div>
                <div class="stat-card">
                    <div class="stat-card-num">{stats['total_lines']:,}</div>
                    <div class="stat-card-label">Total Lines</div>
                </div>
                <div class="stat-card">
                    <div class="stat-card-num">{stats['total_words']:,}</div>
                    <div class="stat-card-label">Total Words</div>
                </div>
                <div class="stat-card">
                    <div class="stat-card-num">{stats['date_sorted']}</div>
                    <div class="stat-card-label">Date Sorted</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Preview
        st.markdown('<div class="section-title" style="margin-top:24px;">👁 Preview</div>', unsafe_allow_html=True)
        preview_lines = "\n".join(merged_output.split("\n")[:60])
        st.markdown(f'<div class="transcript-preview">{preview_lines}\n\n... [scroll to see more] ...</div>',
                    unsafe_allow_html=True)

        # Download
        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.download_button(
                label="⬇️  Download Merged Transcript (.txt)",
                data=merged_output.encode("utf-8"),
                file_name="ericsson_merged_transcript.txt",
                mime="text/plain",
                key="download_btn"
            )

        st.markdown("""
        <div class="info-box" style="margin-top:16px;">
            🗑️ <strong>Memory cleared on exit:</strong> Once you close this tab or refresh the page,
            all uploaded data and the generated output are permanently removed from memory. Nothing is stored.
        </div>
        """, unsafe_allow_html=True)

else:
    st.markdown("""
    <div style="text-align:center; padding: 40px; color: #8A9BB0; font-size:14px;">
        ⬆️ Upload your transcript files above to get started
    </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ─── Footer ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="app-footer">
    <span>Ericsson Internal Tool</span> &nbsp;·&nbsp; Transcript Merger v1.0 &nbsp;·&nbsp;
    Zero Data Storage &nbsp;·&nbsp; All processing is session-scoped and in-memory only
</div>
""", unsafe_allow_html=True)
