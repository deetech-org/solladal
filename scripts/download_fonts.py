# scripts/download_fonts.py
# -*- coding: utf-8 -*-
import urllib.request
import re
import os

def main():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    url = 'https://fonts.googleapis.com/css2?family=Mukta+Malar:wght@400;600;700;800&family=Noto+Sans+Tamil:wght@400;500;600;700;800&display=swap'

    print(f"Fetching font CSS from: {url}")
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req) as resp:
        css = resp.read().decode('utf-8')

    os.makedirs('assets/fonts', exist_ok=True)

    blocks = re.findall(r'/\*.*?\*/\s*@font-face\s*\{[^}]+\}', css, re.DOTALL)
    print(f"Parsed {len(blocks)} @font-face blocks from Google Fonts.")

    downloaded = {}
    font_css_lines = []

    for block in blocks:
        family_match = re.search(r'font-family:\s*[\'"]([^\'"]+)[\'"]', block)
        style_match = re.search(r'font-style:\s*([^;]+);', block)
        weight_match = re.search(r'font-weight:\s*([^;]+);', block)
        src_match = re.search(r'url\((https://[^\)]+\.woff2)\)', block)
        subset_match = re.search(r'/\*\s*([^*]+)\s*\*/', block)
        range_match = re.search(r'unicode-range:\s*([^;]+);', block)

        if family_match and src_match:
            family = family_match.group(1)
            weight = weight_match.group(1).strip() if weight_match else '400'
            style = style_match.group(1).strip() if style_match else 'normal'
            src_url = src_match.group(1)
            subset = subset_match.group(1).strip() if subset_match else 'all'

            clean_fam = family.replace(' ', '')
            clean_subset = re.sub(r'[^a-zA-Z0-9]', '', subset)
            filename = f"{clean_fam}-{weight}-{clean_subset}.woff2"
            filepath = os.path.join('assets', 'fonts', filename)

            if src_url not in downloaded:
                print(f"Downloading {filename} from {src_url}...")
                file_req = urllib.request.Request(src_url, headers=headers)
                with urllib.request.urlopen(file_req) as fresp:
                    with open(filepath, 'wb') as out_f:
                        out_f.write(fresp.read())
                downloaded[src_url] = filename

            local_file = downloaded[src_url]
            rule = f"/* {subset} */\n@font-face {{\n  font-family: '{family}';\n  font-style: {style};\n  font-weight: {weight};\n  font-display: swap;\n  src: url('./{local_file}') format('woff2');"
            if range_match:
                rule += f"\n  unicode-range: {range_match.group(1).strip()};"
            rule += "\n}"
            font_css_lines.append(rule)

    css_path = os.path.join('assets', 'fonts', 'fonts.css')
    with open(css_path, 'w', encoding='utf-8') as f:
        f.write("/* Local Self-Hosted Fonts for சொல்லாடல் (Solladal) */\n\n" + '\n\n'.join(font_css_lines) + '\n')

    print(f"\nSuccessfully downloaded {len(downloaded)} font files into assets/fonts/ and created {css_path}")

if __name__ == '__main__':
    main()
