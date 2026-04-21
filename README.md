# Ericsson — Multi-Transcript Merger

A Streamlit web app that merges multiple meeting transcripts into one
chronologically-sorted document. Built for Ericsson internal use.

## 🔒 Zero Data Storage Policy

- All processing is **100% in-memory** — no files are saved, logged, or transmitted
- Data is permanently discarded when the browser session ends
- Compliant with Ericsson data confidentiality guidelines

## Features

- Upload **unlimited** `.txt` or `.docx` transcript files
- **Auto-detects meeting dates** from filenames or file content
- **Chronologically sorts** all transcripts (oldest → newest)
- Merges into a **single clean document** with clear section headers
- One-click **download** of the merged output

## Supported Date Formats (Auto-detected)

| Format | Example |
|--------|---------|
| ISO | `2024-03-15` or `2024/03/15` |
| Compact | `20240315` |
| Long text | `15 March 2024` or `March 15, 2024` |
| DD/MM/YYYY | `15/03/2024` |

## Quick Start

```bash
# 1. Clone the repo
git clone https://github.com/your-org/ericsson-transcript-merger.git
cd ericsson-transcript-merger

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the app
streamlit run app.py
```

Then open **http://localhost:8501** in your browser.

## Deploy on Streamlit Cloud

1. Push this repo to GitHub (include `ericsson_logo.jpg`)
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repo → set **Main file**: `app.py`
4. Click **Deploy**

## Project Structure

```
ericsson-transcript-merger/
├── app.py                  # Streamlit UI
├── transcript_merger.py    # Core merge & sort logic
├── ericsson_logo.jpg       # Ericsson logo
├── requirements.txt        # Python dependencies
└── README.md
```

## Usage Tips

- **Date in filename**: Name files like `2024-03-15_standup.txt` for reliable sorting
- **Date in content**: The tool scans the first 50 lines for any recognisable date
- Files **without a detectable date** are appended at the end of the merged document

---

*Ericsson Internal Tool — v1.0 — Zero Data Storage*
