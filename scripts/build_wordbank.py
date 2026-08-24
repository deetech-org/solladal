# -*- coding: utf-8 -*-
"""
Solladal word-bank generator (v2).

Source of truth : tamilwordbank-v2.md   (normalized, one row per word)
Output          : data/words.json       (denormalized: metadata / byLength / byComplexity / all)

Per word it derives `letters` and `transliteration` from the Word itself, reads
`meaning`, `complexity`, and the three clues from the table, and validates everything
before writing. Replaces the older sync_wordbank.py.

Run:  PYTHONIOENCODING=utf-8 python scripts/build_wordbank.py
"""
import json, io, re, sys, unicodedata

SRC = "tamilwordbank-v2.md"
OUT = "data/words.json"
TITLE = "சொல்லாடல் (Solladal) — Tamil Word Bank"
VERSION = "1.3.2"

# ---- Tamil grapheme tokenizer (mirrors getTamilLetters() in js/tamilUtils.js) ----
_GRAPHEME_RE = re.compile(r"[அ-ஔஃ]|(?:[க-ஹஂ][ா-்ௗ]*)")
def split_graphemes(word):
    return _GRAPHEME_RE.findall(unicodedata.normalize("NFC", word).strip())

# ---- Natural-pronunciation transliteration (position-aware voicing) ----
IND_VOWEL = {"அ":"a","ஆ":"aa","இ":"i","ஈ":"ee","உ":"u","ஊ":"oo","எ":"e","ஏ":"ae",
             "ஐ":"ai","ஒ":"o","ஓ":"oa","ஔ":"au"}
CONS = {"ங":"ng","ஞ":"nj","ண":"n","ந":"n","ம":"m","ய":"y","ர":"r","ல":"l","வ":"v",
        "ழ":"zh","ள":"l","ன":"n","ஜ":"j","ஷ":"sh","ஸ":"s","ஹ":"h","ஶ":"sh"}
PLOSIVE_HARD = {"க":"k","ச":"ch","ட":"t","த":"th","ப":"p","ற":"r"}
PLOSIVE_SOFT = {"க":"g","ச":"s","ட":"d","த":"dh","ப":"b","ற":"r"}
NASAL_OF = {"க":"ங","ச":"ஞ","ட":"ண","த":"ந","ப":"ம"}
SIGN = {"":"a","ா":"aa","ி":"i","ீ":"ee","ு":"u","ூ":"oo","ெ":"e","ே":"ae","ை":"ai",
        "ொ":"o","ோ":"oa","ௌ":"au","ௗ":"au"}
PULLI = "்"

def _vowel_part(g):
    rest = g[1:]
    if PULLI in rest: return ""
    return SIGN.get(rest, "a")

def transliterate(letters):
    letters = [unicodedata.normalize("NFC", l) for l in letters]
    out = []
    for i, g in enumerate(letters):
        if g in IND_VOWEL: out.append(IND_VOWEL[g]); continue
        if g == "ஃ": out.append("akh"); continue
        c0 = g[0]
        if c0 in PLOSIVE_HARD:
            if PULLI in g:            base = PLOSIVE_HARD[c0]      # bare/coda/geminate -> hard
            elif i == 0:              base = PLOSIVE_HARD[c0]      # word-initial -> hard
            else:
                prev = letters[i-1]
                if PULLI in prev:
                    pc = prev[0]
                    if pc == c0:                       base = PLOSIVE_HARD[c0]   # gemination
                    elif NASAL_OF.get(c0) == pc:       base = "" if pc == "ங" else PLOSIVE_SOFT[c0]
                    else:                              base = PLOSIVE_HARD[c0]
                else:                                  base = PLOSIVE_SOFT[c0]   # intervocalic
        else:
            base = CONS.get(c0, c0)
        out.append(base + _vowel_part(g))
    return "".join(out)

# ---- Markdown table parsing ----
_LEN_WORD = {"One":1,"Two":2,"Three":3,"Four":4,"Five":5}
_SEC_RE = re.compile(r"^##\s+(One|Two|Three|Four|Five)-Letter")
_BACKTICK_RE = re.compile(r"`([^`]+)`")

def split_row(line):
    """Split a markdown table row on unescaped pipes."""
    line = line.strip().strip("|")
    line = line.replace(r"\|", "\x00")
    return [c.replace("\x00", "|").strip() for c in line.split("|")]

def parse_clue(cell):
    cell = cell.strip()
    ta, en = (cell.split("<br>", 1) + [""])[:2] if "<br>" in cell else (cell, "")
    en = re.sub(r"^\*+", "", en.strip()); en = re.sub(r"\*+$", "", en).strip()
    return {"ta": ta.strip(), "en": en}

def parse(path):
    rows, errors = [], []
    section = None
    with io.open(path, encoding="utf-8") as fh:
        for lineno, line in enumerate(fh, 1):
            m = _SEC_RE.match(line)
            if m:
                section = _LEN_WORD[m.group(1)]; continue
            if not line.lstrip().startswith("|"):
                continue
            cells = split_row(line)
            # header / separator rows
            if not cells or cells[0] in ("#", "") or set(cells[0]) <= set(":- "):
                continue
            if not cells[0].isdigit():
                continue
            if len(cells) < 9:
                errors.append(f"line {lineno}: only {len(cells)} columns (need 9)"); continue
            sno, word_md, letters_md, translit_md, meaning, complexity_md, c1, c2, c3 = cells[:9]
            word = word_md.strip("*").strip()
            letters_col = _BACKTICK_RE.findall(letters_md)
            complexity = complexity_md.strip("`").strip()
            derived_letters = split_graphemes(word)
            derived_translit = transliterate(derived_letters)

            # ---- validation ----
            if section is None:
                errors.append(f"line {lineno} ({word}): row outside any length section")
            elif len(derived_letters) != section:
                errors.append(f"line {lineno} ({word}): splits into {len(derived_letters)} letters, section is {section}")
            if letters_col and letters_col != derived_letters:
                errors.append(f"line {lineno} ({word}): Letters column {letters_col} != tokenizer split {derived_letters}")
            if translit_md and translit_md != derived_translit:
                errors.append(f"line {lineno} ({word}): Transliteration '{translit_md}' != derived '{derived_translit}'")
            if not meaning or meaning == "—":
                errors.append(f"line {lineno} ({word}): empty Meaning")
            clues = {"clue1": parse_clue(c1), "clue2": parse_clue(c2), "clue3": parse_clue(c3)}
            for k, cl in clues.items():
                if not cl["ta"] or not cl["en"]:
                    errors.append(f"line {lineno} ({word}): {k} missing Tamil or English")

            rows.append({
                "word": word,
                "transliteration": derived_translit,
                "meaning": meaning,
                "length": len(derived_letters),
                "letters": derived_letters,
                "complexity": complexity,
                "clues": clues,
            })
    return rows, errors

def build(rows):
    by_length, by_complexity = {}, {}
    for e in rows:
        by_length.setdefault(str(e["length"]), []).append(e)
        by_complexity.setdefault(e["complexity"], []).append(e)
    metadata = {
        "title": TITLE, "version": VERSION, "totalWords": len(rows),
        "countsByLength": {k: len(v) for k, v in sorted(by_length.items())},
        "countsByComplexity": {k: len(v) for k, v in by_complexity.items()},
    }
    return {"metadata": metadata, "byLength": by_length, "byComplexity": by_complexity, "all": rows}

def main():
    print("Parsing", SRC, "...")
    rows, errors = parse(SRC)
    dups = {}
    for e in rows: dups[e["word"]] = dups.get(e["word"], 0) + 1
    for w, n in dups.items():
        if n > 1: errors.append(f"duplicate word '{w}' ({n}x)")
    if errors:
        print(f"[FAIL] {len(errors)} problem(s):")
        for e in errors[:40]: print("   -", e)
        if len(errors) > 40: print(f"   ... and {len(errors)-40} more")
        sys.exit(1)
    data = build(rows)
    io.open(OUT, "w", encoding="utf-8").write(json.dumps(data, ensure_ascii=False, indent=2) + "\n")
    m = data["metadata"]
    print(f"[OK] Wrote {OUT}: {m['totalWords']} words")
    print("   byLength:", m["countsByLength"])
    print("   byComplexity:", m["countsByComplexity"])

if __name__ == "__main__":
    main()
