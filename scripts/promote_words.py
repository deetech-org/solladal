# -*- coding: utf-8 -*-
"""
Promotion script: Promotes the 43 candidate words from words-to-be-added.md
into tamilwordbank-v2.md, matching its exact 9-column schema, and updates
section headers and numbering.
"""
import io, os, re, unicodedata, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
try:
    from build_wordbank import split_graphemes, final_translit
except ImportError:
    from scripts.build_wordbank import split_graphemes, final_translit

CANDIDATES_FILE = 'words-to-be-added.md'
WORDBANK_FILE = 'tamilwordbank-v2.md'

CONCISE_GLOSSES = {
    'நுண்மை': 'Subtlety',
    'ஒழுங்கு': 'Orderliness',
    'நிறைவு': 'Fulfillment',
    'ஒளிர்வு': 'Radiance',
    'பாப்பா': 'Baby / Little child',
    'பாரதம்': 'Mother India',
    'சக்தி': 'Cosmic energy / Goddess',
    'காணி': 'Traditional land measure',
    'மாதர்': 'Women / Mothers',
    'வல்லமை': 'Competence / Mastery',
    'முழங்கு': 'Resound / Proclaim loudly',
    'வையம்': 'Earth / World',
    'இன்னா': 'Harmful deeds / Malice',
    'குடியுரிமை': 'Citizenship',
    'ஊழியம்': 'Dedicated service',
    'பொறை': 'Forbearance / Patience',
    'செங்கோல்': 'Righteous royal scepter',
    'நயன்': 'Justice / Fairness',
    'சிவம்': 'Supreme Goodness',
    'தெள்ளு': 'Clarify / Pure wisdom',
    'ஆனந்தம்': 'Supreme bliss',
    'மாணிக்கம்': 'Ruby gemstone',
    'தில்லை': 'Chidambaram city',
    'அம்மானை': "Women's singing game",
    'ஈசன்': 'The Supreme Lord',
    'யோகம்': 'Spiritual union / Meditation',
    'பிராணன்': 'Vital life-breath',
    'ஞானம்': 'Divine wisdom',
    'வாழ்க்கை': 'Life journey',
    'பயணம்': 'Journey / Travel',
    'பொதுமை': 'Social equality',
    'பாட்டாளி': 'Working-class laborer',
    'பூங்காற்று': 'Gentle scented breeze',
    'வசந்தம்': 'Spring season',
    'பொன்மகள்': 'Golden maiden',
    'நீரோடை': 'Freshwater stream',
    'தாயகம்': 'Motherland',
    'ஸ்ரீமான்': 'Mister (Mr.)',
    'ஸ்ரீமதி': 'Madam (Mrs.)',
    'ஸ்ரீவள்ளி': 'Goddess Valli',
    'ஸ்ரீபதம்': 'Holy divine feet',
    'ஸ்ரீபுரம்': 'Golden temple city',
    'ஸ்ரீரங்கம்': 'Srirangam holy town'
}

def parse_candidates():
    candidates_by_len = {2: [], 3: [], 4: [], 5: []}
    with io.open(CANDIDATES_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            m = re.match(r'^\|\s*(\d+)\s*\|\s*\*\*([^*]+)\*\*\s*\|', line)
            if not m:
                continue
            cells = [c.strip() for c in line.strip().strip('|').split('|')]
            word = m.group(2).strip()
            complexity = cells[5].strip('`').strip()
            c1, c2, c3 = cells[6], cells[7], cells[8]
            letters = split_graphemes(word)
            n_len = len(letters)
            translit = final_translit(word, letters)
            meaning = CONCISE_GLOSSES.get(word, 'Meaning')
            letters_col = ', '.join([f'`{g}`' for g in letters])
            
            row_dict = {
                'word': word,
                'letters_col': letters_col,
                'translit': translit,
                'meaning': meaning,
                'complexity': complexity,
                'c1': c1,
                'c2': c2,
                'c3': c3,
                'length': n_len
            }
            candidates_by_len[n_len].append(row_dict)
    return candidates_by_len

def promote():
    candidates = parse_candidates()
    total_new = sum(len(v) for v in candidates.values())
    print(f'Parsed {total_new} candidate words from {CANDIDATES_FILE}')
    
    with io.open(WORDBANK_FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    sec_pattern = re.compile(r'(^##\s+(?:One|Two|Three|Four|Five)-Letter[^\r\n]*)', re.MULTILINE)
    parts = sec_pattern.split(content)
    
    len_map = {
        'One-Letter': 1,
        'Two-Letter': 2,
        'Three-Letter': 3,
        'Four-Letter': 4,
        'Five-Letter': 5
    }
    
    out_parts = [parts[0]]
    for i in range(1, len(parts), 2):
        heading = parts[i]
        body = parts[i+1]
        
        sec_len = None
        for k, v in len_map.items():
            if k in heading:
                sec_len = v
                break
        
        lines = body.splitlines()
        existing_rows = []
        pre_table_lines = []
        table_started = False
        
        for line in lines:
            if line.startswith('|') and not line.startswith('| #') and not line.startswith('| :-'):
                table_started = True
                existing_rows.append(line)
            elif not table_started:
                pre_table_lines.append(line)
        
        new_words_for_sec = candidates.get(sec_len, [])
        for w in new_words_for_sec:
            new_row = f"| # | **{w['word']}** | {w['letters_col']} | {w['translit']} | {w['meaning']} | `{w['complexity']}` | {w['c1']} | {w['c2']} | {w['c3']} |"
            existing_rows.append(new_row)
        
        renumbered_rows = []
        for idx, r in enumerate(existing_rows, 1):
            cells = [c.strip() for c in r.strip().strip('|').split('|')]
            cells[0] = str(idx)
            renumbered_rows.append('| ' + ' | '.join(cells) + ' |')
            
        new_count = len(renumbered_rows)
        new_heading = re.sub(r'—\s*\d+\s*words', f'— {new_count} words', heading)
        print(f'Section {sec_len}-Letter: {len(existing_rows) - len(new_words_for_sec)} -> {new_count} words (+{len(new_words_for_sec)})')
        
        out_parts.append(new_heading)
        sec_body_lines = []
        if pre_table_lines:
            sec_body_lines.extend(pre_table_lines)
            sec_body_lines.append("")
        sec_body_lines.append("| # | Word | Letters | Transliteration | Meaning | Complexity | Clue 1 | Clue 2 | Clue 3 |")
        sec_body_lines.append("| :--: | :--: | :-- | :-- | :-- | :--: | :-- | :-- | :-- |")
        sec_body_lines.extend(renumbered_rows)
        sec_body_lines.append("")
        out_parts.append("\n".join(sec_body_lines) + "\n")

    updated_wordbank = ''.join(out_parts)
    with io.open(WORDBANK_FILE, 'w', encoding='utf-8') as f:
        f.write(updated_wordbank)
    print(f'[SUCCESS] Successfully promoted all {total_new} words into {WORDBANK_FILE}!')

if __name__ == '__main__':
    promote()
