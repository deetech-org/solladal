import sys, json, re, unicodedata

def get_tamil_letters(word):
    word = unicodedata.normalize('NFC', word.strip())
    pattern = r'(?:ஸ்ரீ|\u0BB8\u0BCD\u0BB0\u0BC0|\u0BB6\u0BCD\u0BB0\u0BC0)|[\u0B85-\u0B94\u0B83]|(?:[\u0B95-\u0BB9\u0B82][\u0BBE-\u0BCD\u0BD7]*)'
    return re.findall(pattern, word)

with open('data/words.json', 'r', encoding='utf-8') as f:
    words_data = json.load(f)
existing_words = set(item['word'] for item in words_data.get('all', []))

with open('words-to-be-added.md', 'r', encoding='utf-8') as f:
    lines = f.readlines()

parsed_words = []
errors = []
len_dist = {}
section_counts = {}
current_sec = "None"

for line_num, line in enumerate(lines, 1):
    if line.startswith('## Section'):
        current_sec = line.strip('# \n')
        section_counts[current_sec] = 0
        continue
        
    parts = [p.strip() for p in line.split('|')]
    if len(parts) >= 10 and parts[1].isdigit():
        sno = int(parts[1])
        w = re.sub(r'[*`_]', '', parts[2]).strip()
        stated_letters = [x.strip('` ') for x in parts[3].split('+')]
        stated_len = int(re.sub(r'[*`_]', '', parts[4]).strip())
        source = parts[5].strip()
        comp = re.sub(r'[*`_]', '', parts[6]).strip()
        c1 = parts[7].strip()
        c2 = parts[8].strip()
        c3 = parts[9].strip()

        actual_letters = get_tamil_letters(w)
        actual_len = len(actual_letters)

        # 1. Duplicate check with active database (skipped if verifying promoted words)
        if "--allow-promoted" not in sys.argv and w in existing_words:
            errors.append(f"Line {line_num}: '{w}' already exists in data/words.json")

        # 2. Length check
        if actual_len != stated_len:
            errors.append(f"Line {line_num}: '{w}' stated length {stated_len} != actual {actual_len}")

        # 3. Grapheme cluster sequence check
        if stated_letters != actual_letters:
            errors.append(f"Line {line_num}: '{w}' stated letters {stated_letters} != actual {actual_letters}")

        # 4. Complexity rating check
        if comp not in ['Beginner', 'Intermediate', 'Advanced']:
            errors.append(f"Line {line_num}: '{w}' invalid complexity '{comp}'")

        # 5. Clues completeness, bilingual structure, and LEAK GATE
        for c_idx, c_text in enumerate([c1, c2, c3], 1):
            if not c_text:
                errors.append(f"Line {line_num}: '{w}' Clue {c_idx} is empty")
            elif '<br>*' not in c_text and '<i>' not in c_text and not ('*' in c_text):
                errors.append(f"Line {line_num}: '{w}' Clue {c_idx} missing English translation formatting")
            
            # LEAK GATE: Target word must NEVER appear verbatim in any clue!
            if w in c_text:
                errors.append(f"Line {line_num}: LEAK DETECTED! Word '{w}' appears verbatim in Clue {c_idx}: \"{c_text[:70]}...\"")

        parsed_words.append(w)
        len_dist[actual_len] = len_dist.get(actual_len, 0) + 1
        section_counts[current_sec] = section_counts.get(current_sec, 0) + 1

# 6. Internal duplicate check
internal_dups = [w for w in parsed_words if parsed_words.count(w) > 1]
if internal_dups:
    errors.append(f"Internal duplicate words found: {set(internal_dups)}")

print("============================================================")
print("WORDS-TO-BE-ADDED.MD AUDIT REPORT")
print("============================================================")
print(f"Total candidate words parsed: {len(parsed_words)}")
print(f"Total errors/warnings found:  {len(errors)}")
print("\nBreakdown by Letter Length:")
for l, count in sorted(len_dist.items()):
    print(f"  - {l}-letter words: {count}")

print("\nBreakdown by Source Section:")
for sec, count in section_counts.items():
    print(f"  - {sec}: {count} words")

if errors:
    print(f"\n❌ LEAK GATE / AUDIT FAILED with {len(errors)} error(s):")
    for e in errors:
        print(f"  ❌ {e}")
    sys.exit(1)
else:
    print("\n✅ LEAK GATE PASSED: Zero clue leaks detected across all candidate clues!")
    print(f"✅ ALL {len(parsed_words)} candidate entries PASSED validation perfectly (0 errors)!")
    sys.exit(0)
print("============================================================")
