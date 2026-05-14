#!/usr/bin/env python3
"""
Merge multiple test case module files into a single document.

Usage:
    python merge_test_cases.py --protocol ospf
    python merge_test_cases.py --protocol ospf --output test-cases/ospf/ospf-complete.md
"""

import argparse
import glob
import os
import re
import sys
from datetime import date


def merge_protocol_files(protocol: str, test_cases_dir: str, output_path: str = None):
    proto_dir = os.path.join(test_cases_dir, protocol)
    if not os.path.isdir(proto_dir):
        print(f"ERROR: Directory not found: {proto_dir}")
        sys.exit(1)

    pattern = os.path.join(proto_dir, f"{protocol}-functional-test-cases-mod*.md")
    files = sorted(glob.glob(pattern))

    if not files:
        print(f"ERROR: No test case files found matching: {pattern}")
        sys.exit(1)

    if not output_path:
        output_path = os.path.join(proto_dir, f"{protocol}-functional-test-cases-complete.md")

    print(f"Merging {len(files)} files for {protocol.upper()}:")
    for f in files:
        print(f"  - {os.path.basename(f)}")

    header = f"""# PicOS {protocol.upper()} Functional Test Cases — Complete

**Platform**: PicOS 4.6
**Generated**: {date.today().isoformat()}
**Merged from**: {len(files)} module files

---

"""

    merged_content = [header]
    total_cases = 0

    for filepath in files:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        lines = content.split("\n")
        skip_header = True
        filtered_lines = []

        for line in lines:
            if skip_header:
                if line.startswith("## ") or line.startswith("### 1."):
                    skip_header = False
                    filtered_lines.append(line)
                continue
            if line.startswith("## Coverage Summary"):
                break
            filtered_lines.append(line)

        case_count = len(re.findall(r"\|\s*\*\*Test Name\*\*\s*\|", "\n".join(filtered_lines)))
        total_cases += case_count
        merged_content.append("\n".join(filtered_lines))
        merged_content.append("\n\n")

    merged_content.append(f"\n---\n\n## Merge Summary\n\n")
    merged_content.append(f"- **Total Test Cases**: {total_cases}\n")
    merged_content.append(f"- **Source Files**: {len(files)}\n")
    merged_content.append(f"- **Merge Date**: {date.today().isoformat()}\n")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("".join(merged_content))

    print(f"\nMerged {total_cases} test cases → {output_path}")


def main():
    parser = argparse.ArgumentParser(description="Merge test case module files into a single document")
    parser.add_argument("--protocol", type=str, required=True, help="Protocol name (ospf, bgp, etc.)")
    parser.add_argument("--output", type=str, default=None, help="Output file path")
    parser.add_argument("--test-dir", type=str, default=None, help="Test cases directory")
    args = parser.parse_args()

    if args.test_dir:
        test_dir = args.test_dir
    else:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        test_dir = os.path.join(os.path.dirname(script_dir), "test-cases")

    merge_protocol_files(args.protocol, test_dir, args.output)


if __name__ == "__main__":
    main()
