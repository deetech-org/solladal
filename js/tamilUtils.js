// js/tamilUtils.js
// -*- coding: utf-8 -*-
/**
 * Tamil Grapheme Cluster Engine & Mei+Uyir Combination Synthesizer.
 * Provides accurate Unicode-normalized grapheme tokenization and 
 * composite letter synthesis for the 2-step Tamil keypad.
 */

// 23 Mei (மெய் & கிரந்தம்) Consonants with pulli
export const MEI_LETTERS = [
  'க்', 'ச்', 'ட்', 'த்', 'ப்', 'ற்',
  'ங்', 'ஞ்', 'ண்', 'ந்', 'ம்', 'ன்',
  'ய்', 'ர்', 'ல்', 'வ்', 'ழ்', 'ள்',
  'க்ஷ்', 'ஜ்', 'ஸ்', 'ஷ்', 'ஹ்'
];

// 13 Uyir (உயிர் & ஆய்தம்) Vowels
export const UYIR_LETTERS = [
  'அ', 'ஆ', 'இ', 'ஈ', 'உ', 'ஊ',
  'எ', 'ஏ', 'ஐ', 'ஒ', 'ஓ', 'ஔ',
  'ஃ'
];

// Base pure consonants mapping (stripping pulli)
const MEI_BASE_MAP = {
  'க்': 'க', 'ச்': 'ச', 'ட்': 'ட', 'த்': 'த', 'ப்': 'ப', 'ற்': 'ற',
  'ங்': 'ங', 'ஞ்': 'ஞ', 'ண்': 'ண', 'ந்': 'ந', 'ம்': 'ம', 'ன்': 'ன',
  'ய்': 'ய', 'ர்': 'ர', 'ல்': 'ல', 'வ்': 'வ', 'ழ்': 'ழ', 'ள்': 'ள',
  'க்ஷ்': 'க்ஷ', 'ஜ்': 'ஜ', 'ஸ்': 'ஸ', 'ஷ்': 'ஷ', 'ஹ்': 'ஹ'
};

// Vowel diacritic sign markers
const VOWEL_DIACRITICS = {
  'அ': '',        // Base consonant itself (e.g. க)
  'ஆ': '\u0BBE',  // ா (e.g. கா)
  'இ': '\u0BBF',  // ி (e.g. கி)
  'ஈ': '\u0BC0',  // ீ (e.g. கீ)
  'உ': '\u0BC1',  // ு (e.g. கு)
  'ஊ': '\u0BC2',  // ூ (e.g. கூ)
  'எ': '\u0BC6',  // ெ (e.g. கெ)
  'ஏ': '\u0BC7',  // ே (e.g. கே)
  'ஐ': '\u0BC8',  // ை (e.g. கை)
  'ஒ': '\u0BCA',  // ொ (e.g. கொ)
  'ஓ': '\u0BCB',  // ோ (e.g. கோ)
  'ஔ': '\u0BCC',  // ௌ (e.g. கௌ)
  'ஃ': 'ஃ'        // Standalone Ayutha Ezhuthu
};

/**
 * Splits a Tamil word into discrete grapheme clusters.
 * Handles NFC normalization and multi-code-point composite glyphs.
 * @param {string} word 
 * @returns {string[]} Array of distinct Tamil letters
 */
export function getTamilLetters(word) {
  if (!word) return [];
  const normalized = String(word).normalize('NFC').trim();
  const regex = /[\u0B85-\u0B94\u0B83]|(?:[\u0B95-\u0BB9\u0B82][\u0BBE-\u0BCD\u0BD7]*)/g;
  return normalized.match(regex) || [];
}

/**
 * Combines a Mei consonant and an Uyir vowel into a single UyirMei grapheme.
 * @param {string|null} mei - Selected consonant (e.g. 'க்', 'த்') or null
 * @param {string|null} uyir - Selected vowel (e.g. 'ஆ', 'ஐ') or null
 * @returns {string} Synthesized Tamil grapheme (e.g. 'கா', 'தை', 'க்', 'ஆ')
 */
export function combineMeiUyir(mei, uyir) {
  // If Ayutham is selected, return standalone Ayutha Ezhuthu
  if (uyir === 'ஃ' || mei === 'ஃ') {
    return 'ஃ';
  }

  // Case 1: Both Mei and Uyir selected -> Synthesize UyirMei
  if (mei && uyir) {
    const baseConsonant = MEI_BASE_MAP[mei] || mei;
    const diacritic = VOWEL_DIACRITICS[uyir];
    
    if (diacritic === undefined) {
      return (baseConsonant + uyir).normalize('NFC');
    }
    
    return (baseConsonant + diacritic).normalize('NFC');
  }

  // Case 2: Only Mei selected -> Output pure consonant with pulli
  if (mei && !uyir) {
    return mei.normalize('NFC');
  }

  // Case 3: Only Uyir selected -> Output standalone independent vowel
  if (!mei && uyir) {
    return uyir.normalize('NFC');
  }

  return '';
}

/**
 * Triggers native haptic feedback on supported mobile devices with web vibration fallback.
 * @param {'light'|'medium'|'heavy'|'success'|'error'} style 
 */
export async function playHaptic(style = 'light') {
  try {
    const Haptics = window.Capacitor?.Plugins?.Haptics;
    if (Haptics) {
      if (style === 'light') {
        await Haptics.impact({ style: 'LIGHT' });
      } else if (style === 'medium') {
        await Haptics.impact({ style: 'MEDIUM' });
      } else if (style === 'heavy') {
        await Haptics.impact({ style: 'HEAVY' });
      } else if (style === 'success') {
        await Haptics.notification({ type: 'SUCCESS' });
      } else if (style === 'error') {
        await Haptics.notification({ type: 'ERROR' });
      }
      return;
    }
  } catch (e) {
    // Fall through to web vibrate
  }

  if (typeof navigator !== 'undefined' && navigator.vibrate) {
    try {
      if (style === 'light') navigator.vibrate(12);
      else if (style === 'medium') navigator.vibrate(25);
      else if (style === 'heavy') navigator.vibrate(40);
      else if (style === 'success') navigator.vibrate([20, 40, 30]);
      else if (style === 'error') navigator.vibrate([40, 30, 40]);
    } catch (e) {}
  }
}
