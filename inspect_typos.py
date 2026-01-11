import pdfplumber
import re

pdf_path = "bản thành phần dinh dưỡng.pdf"

# Codes to inspect:
# 1012 Bánh mý
# 1013 Bánh phỡ (Fixed? User said "Bánh phở", list says "Bánh phở" now? No list says "Bánh phở" in my check_names output? Let me check carefully.)
# List says: "Bánh phở". OK.
# List says: "Bánh mý". Wrong.
# 1045 Bột dong lồc (guessed code, need to find it by name)
# 1047 Bột khoai tây (lồc)
# 1022 Mý sợi
# 6006 Rau giền cơm
# 6007 Rau giền trắng
# 6008 Rau giền đỏ
# 6019 Rau sà lách
# 11005 Mắc coồc
# 5035 Nho ngồt
# 7050 Lạp xường (guessed)
# 6038 Mộc nhỉ (guessed)


target_codes = ["1012", "1022", "2016", "2019", "4025", "4026", "4044", "4064", "4072", "4090", "4121", "5026", "5037", "7071"]

pdf_path = "bản thành phần dinh dưỡng.pdf"

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

