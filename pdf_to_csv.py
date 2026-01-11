import pdfplumber
import pandas as pd
import re

pdf_path = "bản thành phần dinh dưỡng.pdf"
output_csv = "raw_food_converted.csv"

# Updated TCVN3 to Unicode Map based on inspection
tcvn3_map = {
    # Lowercase
    'a': 'a', 'b': 'b', 'c': 'c', 'd': 'd', 'e': 'e', 'f': 'f', 'g': 'g', 'h': 'h', 'i': 'i', 'j': 'j', 'k': 'k', 'l': 'l', 'm': 'm', 'n': 'n', 'o': 'o', 'p': 'p', 'q': 'q', 'r': 'r', 's': 's', 't': 't', 'u': 'u', 'v': 'v', 'w': 'w', 'x': 'x', 'y': 'y', 'z': 'z',
    
    # Standard & Observed Mappings
    '\xb5': 'à', 
    '\xb8': 'á', 
    '\xb6': 'ả', # '¶'
    '\xb7': 'ã', 
    '\xb9': 'ạ', # '¹'
    
    '\xa8': 'ă', # '¨'
    '\xbb': 'ằ', 
    '\xbe': 'ắ', # '¾'
    '\xbc': 'ẳ', 
    '\xbd': 'ẵ', 
    '\xc6': 'ặ', # Note: \xc6 in standard is ặ, but \xe6 (æ) is used for ổ/ỗ check below
    
    '\xa9': 'â', # '©'
    '\xc7': 'ầ', # 'Ç'
    '\xca': 'ấ', # 'Ê'
    '\xc8': 'ẩ', 
    '\xc9': 'ẫ', 
    '\xcb': 'ậ',
    
    '\xae': 'đ', # '®'
    
    '\xcc': 'è', 
    '\xd0': 'é', 
    '\xce': 'ẻ', 
    '\xcf': 'ẽ', 
    '\xd1': 'ẹ',
    
    '\xaa': 'ê', # 'ª'
    '\xd2': 'ề', 
    '\xd3': 'ể', 
    '\xd4': 'ễ', 
    '\xd5': 'ế', # 'Õ'
    '\xd6': 'ệ', 
    
    '\xdd': 'í', 
    '\xdb': 'í', 
    '\xdc': 'ỉ', 
    '\xfc': 'ĩ', # 'ü'
    '\xde': 'ị', # 'Þ'
    
    '\xdf': 'ò', # 'ß'
    '\xe3': 'ó', 
    '\xe0': 'ỏ',
    '\xe1': 'ỏ', # 'á' observed as 'ỏ' (thá -> thỏ)
    '\xe2': 'ọ',
    '\xe4': 'ọ', # 'ä' -> ọ (Däc -> Dọc, läc -> lọc)

    '\xab': 'ô', # '«'
    '\xe4': 'ồ', 
    '\xe5': 'ồ', # 'å' -> ồ (Dåi -> Dồi)
    '\xe6': 'ổ', # 'æ' -> ổ (Phæi -> Phổi)
    '\xe7': 'ỗ', # 'ç' -> ỗ (ngçng -> ngỗng)
    '\xe8': 'ố', # 'è' -> ố (sèng -> sống)
    
    '\xac': 'ơ', # '¬' is usually ơ. But in raw: ¬ is \u00ac. Map Unicode char below.
    '\xe9': 'ộ', # 'é' -> ộ (ruét -> ruột)
    '\xea': 'ờ', # 'ê' -> ờ (đường, sườn)
    '\xeb': 'ở', # 'ë' -> ở (phở)
    '\xec': 'ỡ', # 'ì' -> ỡ (mỡ)
    '\xed': 'ớ', # 'í' -> ớ (tào phớ, vớt, nước)
    '\xee': 'ợ', # 'î' -> ợ (lợn)
    
    '\xef': 'ù', # 'ï'
    '\xf3': 'ú', 
    '\xf1': 'ủ', # 'ñ'
    '\xf2': 'ũ', 
    '\xf4': 'ụ', # 'ô'
    
    '\xad': 'ư', # Soft hyphen? 
    '\xf5': 'ừ', # 'õ' -> ừ (cõu -> cừu) Wait. õ is \xf5.
    '\xf6': 'ử', # 'ö'
    '\xf7': 'ữ', 
    '\xf8': 'ứ', 
    '\xf9': 'ự',
    
    '\xfd': 'ỳ', 
    '\xfa': 'ý', 
    '\xfb': 'ỷ', 
    # '\xfc': 'ỹ', # Already mapped to ĩ? Check usages. (Cá chμy -> chay? No.)
    '\xfe': 'ỵ',
    '\xfa': 'ì', # 'ú' -> mì (Bánh mì - Code 1012: B¸nh mú \xfa)

    # Unicode chars from pdfplumber
    '\u03bc': 'à', # μ
    '\u00d7': 'ì', # ×
    '\u00a7': 'Đ', # §
    '\u2212': 'ư', # −
    '\u00ac': 'ơ', # ¬
    '\u00b0': '°', # °
    '\u00a9': 'â', # ©
    '\u00ae': 'đ', # ®
    '\u00aa': 'ê', # ª (Already covered by \xaa but safe to keep)
    '\u00b6': 'ả', # ¶
    '\u00b9': 'ạ', # ¹
    '\u00de': 'ị', # Þ
    '\u00be': 'ắ', # ¾
    '\u00c7': 'ầ', # Ç
    '\u00ca': 'ấ', # Ê
    '\u00d5': 'ế', # Õ
    
    '\u00dd': 'í',
    '\u00fa': 'ì', # Code 1012 B¸nh mú \xfa -> mì
    '\u00dc': 'ĩ', # \u00dc (Ü) -> ĩ (Mộc nhĩ \xdc)
    '\u00e4': 'ọ', # \u00e4 (ä) -> ọ (Däc, läc, coäc)

    # Uppercase etc
    'A': 'A', 'B': 'B', 'C': 'C', 'D': 'D', 'E': 'E', 'F': 'F', 
    'G': 'G', 'H': 'H', 'I': 'I', 'J': 'J', 'K': 'K', 'L': 'L', 
    'M': 'M', 'N': 'N', 'O': 'O', 'P': 'P', 'Q': 'Q', 'R': 'R', 
    'S': 'S', 'T': 'T', 'U': 'U', 'V': 'V', 'W': 'W', 'X': 'X', 
    'Y': 'Y', 'Z': 'Z',
    
    '-': '-',
}

keys_map = {
    'Energy': 'Energy_Kcal',
    'Protein': 'Protein_g',
    'Lipid': 'Fat_g',        
    'Carbohydrate': 'Carb_g',
    'Celluloza': 'Fiber_g', 
    'Calcium': 'Calcium_mg', 
    'Iron': 'Iron_mg',
    'Retinol': 'Vit_A_mcg',  
    'Ascorbic': 'Vit_C_mg',  
    'Thiamine': 'Vit_B1_mg', 
    'Riboflavin': 'Vit_B2_mg'
}

def convert_tcvn3(text):
    if not text: return ""
    chars = []
    for c in text:
        chars.append(tcvn3_map.get(c, c))
    
    res = "".join(chars)
    
    # Post-processing fixes
    res = res.replace(' sè:', ' số:').replace(' s.:', ' số:')
    
    # Specific dictionary fixes for ambiguous TCVN3 mappings
    replacements = {
        'Tiết lợn sộng': 'Tiết lợn sống', # sộng -> sống
        'lî n': 'lợn', # Space case
        'cừ u': 'cừu',
        'Rau giền': 'Rau dền', # giền -> dền
        'Rau sà lách': 'Rau xà lách', # sà -> xà
        'Lạp xường': 'Lạp xưởng', # xường -> xưởng
        'Hoa lỳ': 'Hoa lý', # lỳ -> lý
    }
    
    # Word boundary aware replacement or simple string replacement?
    # Simple is probably fine for these specific errors
    for k, v in replacements.items():
        res = res.replace(k, v)
        
    # Capitalize first letter?
    if res and res[0].islower():
        res = res[0].upper() + res[1:]
        
    return res

def safe_float(val):
    if not val: return 0.0
    val = str(val).strip()
    if val in ['-', '', '0', '0.0']: return 0.0
    try:
        return float(val.replace(',', '.'))
    except:
        return 0.0

data_rows = []

try:
    with pdfplumber.open(pdf_path) as pdf:
        print(f"Total pages: {len(pdf.pages)}")
        
        for i, page in enumerate(pdf.pages):
            text = page.extract_text()
            if not text: continue
            
            matched = False
            code = "0"
            name = "Unknown"
            
            code_match = re.search(r'M.\s*s.:\s*(\d+)', text)
            if code_match:
                code = code_match.group(1)
                matched = True
            
            name_match = re.search(r'T.n\s*th.c\s*ph.m\s*\(Vietnamese\):\s*(.+?)\s*STT', text)
            if name_match:
                name = name_match.group(1).strip()
                name = convert_tcvn3(name)
                matched = True
            
            if not matched: continue
            
            tables = page.extract_tables()
            if not tables: continue
            
            food_data = {
                'Code': code,
                'Name': name,
                'Unit': '100g'
            }
            # Init values
            for target in set(keys_map.values()):
                food_data[target] = 0.0
            
            found_nutrients = False
            
            for table in tables:
                for row in table:
                    check_cols = [(0, 1, 2), (4, 5, 6)]
                    
                    for name_idx, unit_idx, val_idx in check_cols:
                        if len(row) > val_idx and row[name_idx] and row[val_idx]:
                            names_list = row[name_idx].split('\n')
                            units_list = row[unit_idx].split('\n') if row[unit_idx] else []
                            vals_list = row[val_idx].split('\n')
                            
                            p = 0
                            limit = min(len(units_list), len(vals_list))
                            
                            for n_name in names_list:
                                if p >= limit: break
                                
                                curr_unit = units_list[p].strip()
                                curr_val = vals_list[p].strip()
                                
                                matched_key = None
                                for k_word, t_field in keys_map.items():
                                    if k_word in n_name:
                                        if k_word == 'Vitamin B1' and 'B12' in n_name: continue
                                        matched_key = t_field
                                        break
                                
                                if matched_key:
                                    f_val = safe_float(curr_val)
                                    food_data[matched_key] = f_val
                                    found_nutrients = True
                                
                                p += 1
                                
                                if 'Năng lượng' in n_name or 'Energy' in n_name:
                                    if p < limit:
                                        next_unit = units_list[p].strip()
                                        if next_unit == 'KJ':
                                            p += 1 

            if found_nutrients:
                data_rows.append(food_data)
        
        if i % 100 == 0:
            print(f"Processing... Page {i}")

    if data_rows:
        df = pd.DataFrame(data_rows)
        cols_order = ['Code', 'Name', 'Unit', 'Energy_Kcal', 'Protein_g', 'Fat_g', 
                      'Carb_g', 'Fiber_g', 'Calcium_mg', 'Iron_mg', 
                      'Vit_A_mcg', 'Vit_C_mg', 'Vit_B1_mg', 'Vit_B2_mg']
        for c in cols_order:
            if c not in df.columns: df[c] = 0.0
        df = df[cols_order]
        df.to_csv(output_csv, index=False, encoding='utf-8-sig')
        print(f"Success! Converted {len(df)} items to {output_csv}")
    else:
        print("No data found.")

except Exception as e:
    print(f"Failed: {e}")
