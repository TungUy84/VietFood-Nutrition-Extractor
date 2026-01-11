import pdfplumber
import re

pdf_path = "bản thành phần dinh dưỡng.pdf"

target_codes = ["1012"]

print("Scanning for codes:", target_codes)

with pdfplumber.open(pdf_path) as pdf:
    for i, page in enumerate(pdf.pages):
        text = page.extract_text()
        if not text: continue
        
        match = re.search(r'M.\s*s.:\s*(\d+)', text)
        if match:
            code = match.group(1)
            if code in target_codes:
                print(f"--- Found Code {code} on Page {i} ---")
                name_match = re.search(r'T.n\s*th.c\s*ph.m\s*\(Vietnamese\):\s*(.+?)\s*STT', text)
                if name_match:
                    raw_name = name_match.group(1).strip()
                    print(f"Code {code} Raw Name Repr: {repr(raw_name)}")
                    hex_str = " ".join([hex(ord(c)) for c in raw_name])
                    print(f"Hex: {hex_str}")
