# scripts/tamil_utils.py
import re
import unicodedata

def get_tamil_letters(word):
    """
    Extracts Tamil grapheme clusters (letters) accurately according to Tamil orthography.
    Handles Uyir, Ayutham, Mei, Uyirmei, and Grantha characters.
    """
    word = unicodedata.normalize('NFC', word.strip())
    # Regex to match Tamil grapheme clusters
    # 1. Ayutham / independent vowels
    # 2. Base consonants + combining signs (pulli, vowel signs, length marks)
    pattern = r'[\u0B85-\u0B94\u0B83]|(?:[\u0B95-\u0BB9\u0B82][\u0BBE-\u0BCD\u0BD7]*)'
    letters = re.findall(pattern, word)
    return letters

def validate_word_entry(entry, expected_len):
    word = entry['word']
    letters = get_tamil_letters(word)
    if len(letters) != expected_len:
        raise ValueError(f"Word '{word}' has {len(letters)} letters ({letters}), expected {expected_len}")
    if not entry.get('complexity') in ['Beginner', 'Intermediate', 'Advanced']:
        raise ValueError(f"Invalid complexity for '{word}': {entry.get('complexity')}")
    if len(entry.get('clues', [])) < 3:
        raise ValueError(f"Word '{word}' must have at least 3 clues")
    return True
