"""
transcript_merger.py
────────────────────────────────────────────────────────────────
Ericsson Transcript Merger — Core Processing Engine
Zero Data Storage: all operations are purely in-memory.
No file is written to disk. No data is logged or transmitted.
────────────────────────────────────────────────────────────────
"""

import re
import io
from datetime import datetime, date
from typing import Optional


class TranscriptMerger:
    """
    Reads, parses, date-sorts, and merges multiple transcript files
    into a single coherent chronological document.

    Zero-storage guarantee:
        - All input is consumed from in-memory file objects.
        - All output is returned as a Python string.
        - No disk I/O, no logging, no external calls.
    """

    # ── Date patterns to extract from content or filename ──────────────────────
    DATE_PATTERNS = [
        # ISO:  2024-03-15  /  2024/03/15
        (r'(\d{4})[\/\-](\d{1,2})[\/\-](\d{1,2})', '%Y%m%d'),
        # DD-Mon-YYYY:  15-Mar-2024  /  15 Mar 2024  /  15/Mar/2024
        (r'(\d{1,2})[\s\-\/]([A-Za-z]{3,9})[\s\-\/](\d{4})', 'dmy_word'),
        # Mon DD, YYYY:  March 15, 2024
        (r'([A-Za-z]{3,9})\s+(\d{1,2}),?\s+(\d{4})', 'mdy_word'),
        # DD/MM/YYYY  or  MM/DD/YYYY (ambiguous — treated as DD/MM)
        (r'(\d{1,2})[\/\-](\d{1,2})[\/\-](\d{4})', 'ddmmyyyy'),
        # YYYYMMDD
        (r'\b(\d{8})\b', 'compact'),
    ]

    MONTH_MAP = {
        'jan': 1, 'feb': 2, 'mar': 3, 'apr': 4, 'may': 5, 'jun': 6,
        'jul': 7, 'aug': 8, 'sep': 9, 'oct': 10, 'nov': 11, 'dec': 12,
        'january': 1, 'february': 2, 'march': 3, 'april': 4,
        'june': 6, 'july': 7, 'august': 8, 'september': 9,
        'october': 10, 'november': 11, 'december': 12,
    }

    # ── Public API ──────────────────────────────────────────────────────────────

    def read_file(self, uploaded_file) -> str:
        """
        Read a Streamlit UploadedFile object.
        Supports .txt (any encoding) and .docx.
        Returns plain text content as a string.
        """
        name = uploaded_file.name.lower()
        raw_bytes = uploaded_file.getvalue()

        if name.endswith(".docx"):
            return self._read_docx_bytes(raw_bytes)
        else:
            # Try UTF-8 first, fall back to latin-1
            for enc in ("utf-8", "utf-8-sig", "latin-1", "cp1252"):
                try:
                    return raw_bytes.decode(enc)
                except (UnicodeDecodeError, LookupError):
                    continue
            return raw_bytes.decode("utf-8", errors="replace")

    def merge_transcripts(
        self,
        files_data: list[dict],
    ) -> tuple[str, dict]:
        """
        Parameters
        ----------
        files_data : list of dicts with keys 'name' (str) and 'content' (str)

        Returns
        -------
        (merged_text: str, stats: dict)
            merged_text  — the fully combined, date-sorted transcript
            stats        — summary metadata dict
        """
        # 1. Extract dates and attach to each file record
        for record in files_data:
            record["date"] = self._extract_date(record["name"], record["content"])

        # 2. Sort: files with a known date come first (ascending), unknowns last
        def sort_key(r):
            d = r["date"]
            return (0, d) if d else (1, date.max)

        sorted_records = sorted(files_data, key=sort_key)

        # 3. Build merged document
        sections = []
        for idx, record in enumerate(sorted_records, start=1):
            date_str = (
                record["date"].strftime("%d %B %Y")
                if record["date"]
                else "Date Not Detected"
            )
            divider = "═" * 72
            header = (
                f"\n{divider}\n"
                f"  TRANSCRIPT {idx} OF {len(sorted_records)}\n"
                f"  Source File : {record['name']}\n"
                f"  Meeting Date: {date_str}\n"
                f"{divider}\n\n"
            )
            sections.append(header + record["content"].strip())

        # 4. Document envelope
        now_str = datetime.now().strftime("%d %B %Y, %H:%M")
        doc_header = (
            "╔══════════════════════════════════════════════════════════════════════╗\n"
            "║           ERICSSON — MERGED TRANSCRIPT DOCUMENT                     ║\n"
            "║           Generated: {:<44}║\n"
            "║           Zero Data Storage | In-Memory Processing Only             ║\n"
            "╚══════════════════════════════════════════════════════════════════════╝\n\n"
            "SUMMARY\n"
            "───────\n"
            "  Total transcripts merged : {}\n"
            "  Date range               : {} → {}\n"
            "  Sort order               : Chronological (oldest first)\n\n"
        ).format(
            now_str,
            len(sorted_records),
            sorted_records[0]["date"].strftime("%d %b %Y") if sorted_records[0]["date"] else "Unknown",
            sorted_records[-1]["date"].strftime("%d %b %Y") if sorted_records[-1]["date"] else "Unknown",
        )

        merged_text = doc_header + "\n\n".join(sections)

        # 5. Compute stats
        total_lines = sum(len(r["content"].splitlines()) for r in sorted_records)
        total_words = sum(len(r["content"].split()) for r in sorted_records)
        dated_count = sum(1 for r in sorted_records if r["date"])

        stats = {
            "total_files": len(sorted_records),
            "total_lines": total_lines,
            "total_words": total_words,
            "date_sorted": f"{dated_count}/{len(sorted_records)}",
        }

        return merged_text, stats

    # ── Private helpers ─────────────────────────────────────────────────────────

    def _read_docx_bytes(self, raw_bytes: bytes) -> str:
        """Extract plain text from a .docx file given as raw bytes."""
        try:
            import docx  # python-docx
            doc = docx.Document(io.BytesIO(raw_bytes))
            return "\n".join(p.text for p in doc.paragraphs if p.text.strip())
        except ImportError:
            return (
                "[⚠️ python-docx not installed. "
                "Run: pip install python-docx]\n"
                "Raw content could not be extracted."
            )
        except Exception as e:
            return f"[⚠️ Could not parse .docx file: {e}]"

    def _extract_date(self, filename: str, content: str) -> Optional[date]:
        """
        Try to extract a meeting date from the filename first, then the
        first 50 lines of content. Returns a date object or None.
        """
        # Search filename + first 50 lines of content
        search_text = filename + "\n" + "\n".join(content.splitlines()[:50])

        for pattern, fmt in self.DATE_PATTERNS:
            match = re.search(pattern, search_text, re.IGNORECASE)
            if match:
                parsed = self._parse_match(match, fmt)
                if parsed:
                    return parsed
        return None

    def _parse_match(self, match: re.Match, fmt: str) -> Optional[date]:
        """Convert a regex match to a date object."""
        try:
            g = match.groups()

            if fmt == '%Y%m%d':
                return date(int(g[0]), int(g[1]), int(g[2]))

            if fmt == 'compact':
                s = g[0]
                return date(int(s[:4]), int(s[4:6]), int(s[6:8]))

            if fmt == 'dmy_word':
                # day month_name year
                d, m_str, y = int(g[0]), g[1].lower()[:3], int(g[2])
                m = self.MONTH_MAP.get(m_str)
                return date(y, m, d) if m else None

            if fmt == 'mdy_word':
                # month_name day year
                m_str, d, y = g[0].lower()[:3], int(g[1]), int(g[2])
                m = self.MONTH_MAP.get(m_str)
                return date(y, m, d) if m else None

            if fmt == 'ddmmyyyy':
                d, m, y = int(g[0]), int(g[1]), int(g[2])
                # Basic sanity: if day > 12, it must be DD/MM
                if d > 12:
                    return date(y, m, d)
                return date(y, m, d)  # Treat as DD/MM/YYYY

        except (ValueError, TypeError):
            return None

        return None
