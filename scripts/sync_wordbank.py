# scripts/sync_wordbank.py
# -*- coding: utf-8 -*-
"""
One-click Tamil Word Bank synchronizer for "சொல்லாடல்" (Solladal).

Run (Windows PowerShell):
    $env:PYTHONIOENCODING="utf-8"; python scripts/sync_wordbank.py

What it does:
  1. Parses & validates `tamilwordbank.md` — the single source of truth:
       - every word splits into exactly the section's grapheme-length (1..5)
       - complexity is one of Beginner / Intermediate / Advanced
       - all three clues are present with both Tamil and English halves
       - the `Letters` column matches the word's actual grapheme clusters
       - zero duplicate words across the whole bank
  2. Rebuilds `data/words.json` (the indexed dataset the PWA loads).
  3. Auto-bumps the cache version in `sw.js` (patch +1) and stamps the same
     version into words.json, so offline clients drop their stale cache.
  4. Runs the integration test suite if present.

Flags:
  --check       Validate only. Make no changes (no json rebuild, no version bump).
  --no-bump     Rebuild json but keep the current version (don't touch sw.js).
  --no-test     Skip running scripts/test_pwa_integration.py at the end.

Exit code is non-zero if validation fails, so it is safe to use in a hook/CI.
"""
import sys
import os
import re
import json
import unicodedata
import subprocess

# ----- UTF-8 stdout on Windows consoles -------------------------------------
try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORDBANK = os.path.join(REPO_ROOT, "tamilwordbank.md")
WORDS_JSON = os.path.join(REPO_ROOT, "data", "words.json")
SW_JS = os.path.join(REPO_ROOT, "sw.js")
TEST_SCRIPT = os.path.join(REPO_ROOT, "scripts", "test_pwa_integration.py")

VALID_COMPLEXITY = ("Beginner", "Intermediate", "Advanced")

# Tamil grapheme tokenizer — mirrors getTamilLetters() in js/tamilUtils.js:
#   an independent vowel / aytham, OR a consonant followed by any vowel signs.
_GRAPHEME_RE = re.compile(
    r"[அ-ஔஃ]|(?:[க-ஹஂ][ா-்ௗ]*)"
)

_SECTION_RE = re.compile(r"^##\s*(\d)\.\s")
_DATA_ROW_RE = re.compile(r"^\|\s*\d+\s*\|")
_BACKTICK_RE = re.compile(r"`([^`]*)`")


def split_graphemes(word):
    """Split a Tamil word into grapheme-cluster letters (NFC-normalized)."""
    normalized = unicodedata.normalize("NFC", str(word)).strip()
    return _GRAPHEME_RE.findall(normalized)


def _parse_clue(cell):
    """A clue cell is 'Tamil text<br>*English text*'. Return (ta, en)."""
    cell = cell.strip()
    if "<br>" in cell:
        ta, en = cell.split("<br>", 1)
    else:
        ta, en = cell, ""
    ta = ta.strip()
    en = en.strip()
    en = re.sub(r"^\*+", "", en)
    en = re.sub(r"\*+$", "", en).strip()
    return ta, en


def parse_wordbank(path):
    """Parse the markdown into a list of row dicts and return (rows, errors)."""
    with open(path, encoding="utf-8") as fh:
        lines = fh.read().split("\n")

    rows = []
    errors = []
    section = None
    for lineno, line in enumerate(lines, 1):
        m = _SECTION_RE.match(line)
        if m:
            section = int(m.group(1))
            continue
        if section is None or not _DATA_ROW_RE.match(line):
            continue

        cells = line.split("|")
        # cells: ['', sno, word, letters, complexity, c1, c2, c3, ('')]
        if len(cells) < 8:
            errors.append(f"line {lineno}: malformed row (only {len(cells) - 1} columns)")
            continue

        sno = cells[1].strip()
        word = cells[2].strip().strip("*").strip()
        letters_cell = cells[3]
        complexity = cells[4].strip().strip("`").strip()
        clue_cells = cells[5:8]

        letters_in_md = _BACKTICK_RE.findall(letters_cell)
        graphemes = split_graphemes(word)
        clues = [_parse_clue(c) for c in clue_cells]

        rows.append({
            "lineno": lineno,
            "section": section,
            "sno": sno,
            "word": word,
            "letters_md": letters_in_md,
            "graphemes": graphemes,
            "complexity": complexity,
            "clues": clues,
        })
    return rows, errors


def validate(rows):
    """Return a list of human-readable validation error strings."""
    errors = []
    counts = {}
    for r in rows:
        loc = f"S{r['section']} #{r['sno']} '{r['word']}' (line {r['lineno']})"

        if len(r["graphemes"]) != r["section"]:
            errors.append(
                f"{loc}: has {len(r['graphemes'])} letters {r['graphemes']}, "
                f"expected {r['section']}"
            )
        if r["complexity"] not in VALID_COMPLEXITY:
            errors.append(f"{loc}: invalid complexity '{r['complexity']}'")
        if r["letters_md"] != r["graphemes"]:
            expected = ", ".join(f"`{g}`" for g in r["graphemes"])
            errors.append(
                f"{loc}: Letters column {r['letters_md']} does not match the word; "
                f"expected: {expected}"
            )
        for i, (ta, en) in enumerate(r["clues"], 1):
            if not ta or not en:
                errors.append(f"{loc}: clue {i} missing Tamil and/or English text")

        counts.setdefault(r["word"], []).append(loc)

    for word, locs in counts.items():
        if len(locs) > 1:
            errors.append(f"DUPLICATE word '{word}' at: {', '.join(locs)}")

    return errors


def build_payload(rows, version):
    by_length = {1: [], 2: [], 3: [], 4: [], 5: []}
    by_complexity = {c: [] for c in VALID_COMPLEXITY}
    all_words = []
    for r in rows:
        entry = {
            "word": r["word"],
            "length": r["section"],
            "letters": r["graphemes"],
            "complexity": r["complexity"],
            "clues": {
                "clue1": {"ta": r["clues"][0][0], "en": r["clues"][0][1]},
                "clue2": {"ta": r["clues"][1][0], "en": r["clues"][1][1]},
                "clue3": {"ta": r["clues"][2][0], "en": r["clues"][2][1]},
            },
        }
        by_length[r["section"]].append(entry)
        by_complexity[r["complexity"]].append(entry)
        all_words.append(entry)

    return {
        "metadata": {
            "title": "சொல்லாடல் (Solladal) — Tamil Word Bank",
            "version": version,
            "totalWords": len(all_words),
            "countsByLength": {k: len(v) for k, v in by_length.items()},
            "countsByComplexity": {k: len(v) for k, v in by_complexity.items()},
        },
        "byLength": by_length,
        "byComplexity": by_complexity,
        "all": all_words,
    }


def read_current_version():
    """Read 'solladal-vX.Y.Z' from sw.js -> return (X, Y, Z) or None."""
    try:
        with open(SW_JS, encoding="utf-8") as fh:
            text = fh.read()
    except FileNotFoundError:
        return None
    m = re.search(r"solladal-v(\d+)\.(\d+)\.(\d+)", text)
    if not m:
        return None
    return tuple(int(g) for g in m.groups())


def bump_service_worker(new_version):
    """Rewrite the CACHE_NAME version in sw.js to solladal-v{new_version}."""
    with open(SW_JS, encoding="utf-8") as fh:
        text = fh.read()
    new_text, n = re.subn(
        r"solladal-v\d+\.\d+\.\d+",
        f"solladal-v{new_version}",
        text,
    )
    if n == 0:
        return False
    with open(SW_JS, "w", encoding="utf-8") as fh:
        fh.write(new_text)
    return True


def run_tests():
    if not os.path.exists(TEST_SCRIPT):
        print("  (integration test script not found; skipping)")
        return True
    env = dict(os.environ, PYTHONIOENCODING="utf-8")
    proc = subprocess.run(
        [sys.executable, TEST_SCRIPT],
        cwd=REPO_ROOT, env=env,
        capture_output=True, text=True, encoding="utf-8",
    )
    passed = proc.returncode == 0 and "ALL INTEGRATION TESTS PASSED" in (proc.stdout or "")
    tail = [l for l in (proc.stdout or "").splitlines() if l.strip()][-3:]
    for l in tail:
        print("  " + l)
    if proc.returncode != 0 and proc.stderr:
        print(proc.stderr.strip())
    return passed


def main(argv):
    check_only = "--check" in argv
    no_bump = "--no-bump" in argv
    no_test = "--no-test" in argv

    print("=" * 60)
    print("SOLLADAL — Tamil Word Bank Sync")
    print("=" * 60)

    if not os.path.exists(WORDBANK):
        print(f"[FAIL] Source not found: {WORDBANK}")
        return 1

    print("\n[1/4] Parsing & validating tamilwordbank.md ...")
    rows, parse_errors = parse_wordbank(WORDBANK)
    errors = parse_errors + validate(rows)
    if errors:
        print(f"  [FAIL] {len(errors)} problem(s) found:")
        for e in errors[:60]:
            print("    - " + e)
        if len(errors) > 60:
            print(f"    ... and {len(errors) - 60} more")
        return 1
    counts_by_len = {}
    for r in rows:
        counts_by_len[r["section"]] = counts_by_len.get(r["section"], 0) + 1
    print(f"  [PASS] {len(rows)} words valid — by length "
          f"{dict(sorted(counts_by_len.items()))}, 0 duplicates.")

    if check_only:
        print("\n--check: validation only, no files written. Done.")
        return 0

    # ----- version handling --------------------------------------------------
    cur = read_current_version()
    if no_bump:
        version = "%d.%d.%d" % (cur if cur else (1, 0, 0))
        print(f"\n[2/4] Version kept at {version} (--no-bump).")
    else:
        if cur is None:
            new = (1, 0, 0)
            print("\n[2/4] No existing version in sw.js; starting at 1.0.0.")
        else:
            new = (cur[0], cur[1], cur[2] + 1)
        version = "%d.%d.%d" % new

    print("\n[3/4] Rebuilding data/words.json ...")
    payload = build_payload(rows, version)
    os.makedirs(os.path.dirname(WORDS_JSON), exist_ok=True)
    with open(WORDS_JSON, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, ensure_ascii=False, indent=2)
    print(f"  [OK] Wrote {len(payload['all'])} words -> data/words.json "
          f"(version {version})")

    if not no_bump:
        if bump_service_worker(version):
            print(f"  [OK] Bumped sw.js cache -> solladal-v{version}")
        else:
            print("  [WARN] Could not find CACHE_NAME pattern in sw.js; "
                  "version not bumped there.")

    print("\n[4/4] Running integration tests ...")
    if no_test:
        print("  (skipped: --no-test)")
    elif not run_tests():
        print("  [WARN] Integration tests did not report success.")
        return 1

    print("\n" + "=" * 60)
    print(f"SYNC COMPLETE — {len(rows)} words, version {version}.")
    print("=" * 60)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
