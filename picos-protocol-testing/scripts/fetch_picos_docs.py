#!/usr/bin/env python3
"""
Fetch PicOS configuration guides from Pica8 Wiki and save locally.

Usage:
    python fetch_picos_docs.py --protocol ospf --version 4.6
    python fetch_picos_docs.py --protocol bgp --version 4.6
    python fetch_picos_docs.py --all --version 4.6
"""

import argparse
import os
import sys
from urllib.request import urlopen, Request
from urllib.error import URLError
from html.parser import HTMLParser

PICOS_WIKI_BASE = "https://docs.pica8.com/display/PicOS46"

PROTOCOL_PAGES = {
    "ospf": [
        "/Configuring+OSPF",
        "/OSPF+Overview",
        "/Configuring+Basic+OSPF+Tasks",
        "/Configuring+OSPF+Area+Types",
        "/Configuring+OSPF+Route+Redistribution",
        "/Configuring+OSPF+Route+Summarization",
        "/Configuring+OSPF+Graceful+Restart",
    ],
    "bgp": [
        "/Configuring+BGP",
        "/BGP+Overview",
        "/Configuring+Basic+BGP+Tasks",
        "/Configuring+BGP+Route+Policies",
        "/Configuring+BGP+Communities",
        "/Configuring+BGP+Route+Reflector",
    ],
    "stp": [
        "/Configuring+STP",
        "/STP+Overview",
        "/Configuring+RSTP",
        "/Configuring+MSTP",
    ],
    "vxlan": [
        "/Configuring+VXLAN",
        "/VXLAN+Overview",
    ],
    "static-routing": [
        "/Configuring+Static+Routing",
    ],
}


class HTMLTextExtractor(HTMLParser):
    """Simple HTML to text converter."""

    def __init__(self):
        super().__init__()
        self.result = []
        self._skip = False

    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style", "nav", "header", "footer"):
            self._skip = True
        if tag in ("p", "br", "div", "h1", "h2", "h3", "h4", "li", "tr"):
            self.result.append("\n")
        if tag == "td":
            self.result.append("\t")

    def handle_endtag(self, tag):
        if tag in ("script", "style", "nav", "header", "footer"):
            self._skip = False
        if tag in ("h1", "h2", "h3", "h4"):
            self.result.append("\n")

    def handle_data(self, data):
        if not self._skip:
            self.result.append(data)

    def get_text(self):
        return "".join(self.result).strip()


def fetch_page(url: str) -> str:
    """Fetch a single page and return its text content."""
    req = Request(url, headers={"User-Agent": "PicOS-Doc-Fetcher/1.0"})
    try:
        with urlopen(req, timeout=30) as resp:
            html = resp.read().decode("utf-8", errors="replace")
        parser = HTMLTextExtractor()
        parser.feed(html)
        return parser.get_text()
    except URLError as e:
        print(f"  WARNING: Failed to fetch {url}: {e}")
        return ""


def fetch_protocol_docs(protocol: str, version: str, output_dir: str):
    """Fetch all pages for a protocol and save as a single markdown file."""
    pages = PROTOCOL_PAGES.get(protocol)
    if not pages:
        print(f"ERROR: Unknown protocol '{protocol}'. Available: {list(PROTOCOL_PAGES.keys())}")
        sys.exit(1)

    print(f"Fetching PicOS {version} {protocol.upper()} documentation...")
    output_path = os.path.join(output_dir, f"{protocol}-config-guide.md")

    content_parts = [
        f"# PicOS {version} {protocol.upper()} Configuration Guide\n",
        f"Source: Pica8 Wiki ({PICOS_WIKI_BASE})\n",
        f"Auto-fetched by fetch_picos_docs.py\n\n---\n",
    ]

    for page_path in pages:
        url = PICOS_WIKI_BASE + page_path
        page_title = page_path.replace("/", "").replace("+", " ")
        print(f"  Fetching: {page_title}...")
        text = fetch_page(url)
        if text:
            content_parts.append(f"\n## {page_title}\n\n{text}\n\n---\n")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(content_parts))

    print(f"Saved to: {output_path}")


def main():
    parser = argparse.ArgumentParser(description="Fetch PicOS configuration guides from Pica8 Wiki")
    parser.add_argument("--protocol", type=str, help="Protocol to fetch (ospf, bgp, stp, vxlan)")
    parser.add_argument("--all", action="store_true", help="Fetch all protocols")
    parser.add_argument("--version", type=str, default="4.6", help="PicOS version (default: 4.6)")
    parser.add_argument("--output-dir", type=str, default=None, help="Output directory")
    args = parser.parse_args()

    if args.output_dir:
        output_dir = args.output_dir
    else:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        output_dir = os.path.join(os.path.dirname(script_dir), "docs", "picos")

    os.makedirs(output_dir, exist_ok=True)

    if args.all:
        for proto in PROTOCOL_PAGES:
            fetch_protocol_docs(proto, args.version, output_dir)
    elif args.protocol:
        fetch_protocol_docs(args.protocol, args.version, output_dir)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
