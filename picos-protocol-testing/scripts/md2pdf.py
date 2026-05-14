#!/usr/bin/env python3
"""
Convert markdown test case documents to styled PDF.

Usage:
    python md2pdf.py <input.md> [output.pdf]
    python md2pdf.py test-cases/ospf/ospf-functional-test-cases-mod1-3.md

Requirements:
    pip install markdown weasyprint
    brew install pango glib  (macOS)
"""

import sys
import os

try:
    import markdown
    from weasyprint import HTML
except ImportError:
    print("Missing dependencies. Install with:")
    print("  pip install markdown weasyprint")
    print("  brew install pango glib  (macOS)")
    sys.exit(1)

CSS = """
@page {
    size: A4 landscape;
    margin: 1.5cm;
    @bottom-center {
        content: "Page " counter(page) " of " counter(pages);
        font-size: 8pt;
        color: #888;
    }
}
body {
    font-family: "Helvetica Neue", Arial, sans-serif;
    font-size: 9pt;
    line-height: 1.4;
    color: #333;
}
h1 {
    font-size: 18pt;
    color: #1a1a1a;
    border-bottom: 2px solid #2c5aa0;
    padding-bottom: 6px;
}
h2 { font-size: 14pt; color: #2c5aa0; margin-top: 18px; }
h3 { font-size: 12pt; color: #333; margin-top: 14px; }
h4 { font-size: 11pt; color: #444; margin-top: 10px; }
h5 {
    font-size: 10pt;
    color: #2c5aa0;
    margin-top: 12px;
    margin-bottom: 4px;
    page-break-after: avoid;
}
table {
    border-collapse: collapse;
    width: 100%;
    margin: 6px 0 16px 0;
    font-size: 8.5pt;
    page-break-inside: avoid;
}
th {
    background-color: #2c5aa0;
    color: white;
    padding: 6px 8px;
    text-align: left;
    font-weight: bold;
    border: 1px solid #2c5aa0;
}
td {
    padding: 5px 8px;
    border: 1px solid #ccc;
    vertical-align: top;
    word-wrap: break-word;
}
tr:nth-child(even) { background-color: #f8f9fa; }
td:first-child {
    width: 18%;
    font-weight: bold;
    white-space: nowrap;
    background-color: #eef2f7;
}
code {
    font-family: "SF Mono", "Courier New", monospace;
    font-size: 8pt;
    background-color: #f0f0f0;
    padding: 1px 3px;
    border-radius: 2px;
    word-break: break-all;
}
pre {
    background-color: #f5f5f5;
    padding: 8px;
    border-radius: 4px;
    font-size: 8pt;
    overflow-wrap: break-word;
    white-space: pre-wrap;
}
hr { border: none; border-top: 1px solid #ddd; margin: 12px 0; }
ul { padding-left: 20px; }
li { margin-bottom: 2px; }
"""


def convert(md_path: str, pdf_path: str = None):
    if not pdf_path:
        pdf_path = os.path.splitext(md_path)[0] + ".pdf"

    with open(md_path, "r", encoding="utf-8") as f:
        md_content = f.read()

    html_body = markdown.markdown(
        md_content,
        extensions=["tables", "fenced_code", "toc"]
    )

    html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><style>{CSS}</style></head>
<body>{html_body}</body></html>"""

    HTML(string=html).write_pdf(pdf_path)
    size_kb = os.path.getsize(pdf_path) / 1024
    print(f"PDF generated: {pdf_path} ({size_kb:.0f} KB)")


def main():
    if len(sys.argv) < 2:
        print("Usage: python md2pdf.py <input.md> [output.pdf]")
        sys.exit(1)

    md_path = sys.argv[1]
    pdf_path = sys.argv[2] if len(sys.argv) > 2 else None

    if not os.path.exists(md_path):
        print(f"ERROR: File not found: {md_path}")
        sys.exit(1)

    convert(md_path, pdf_path)


if __name__ == "__main__":
    main()
