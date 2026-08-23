// js/storage.js
// -*- coding: utf-8 -*-
/**
 * Persistence layer for Solladal Tamil Word Game PWA & Mobile App.
 * Stores statistics, streaks, and user preferences durably using @capacitor/preferences
 * when running natively, with seamless localStorage fallback.
 */

const STATS_KEY = 'solladal_stats_v1';
const SETTINGS_KEY = 'solladal_settings_v1';

const DEFAULT_STATS = {
  gamesPlayed: 0,
  gamesWon: 0,
  currentStreak: 0,
  maxStreak: 0,
  guessDistribution: { 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0 },
  discoveredWords: [] // list of words discovered
};

const DEFAULT_SETTINGS = {
  soundEnabled: true,
  lengthPreference: '3', // 'Random', '1', '2', '3', '4', '5'
  complexityPreference: 'Beginner' // 'Beginner', 'Intermediate', 'Advanced'
};

let cachedStats = null;
let cachedSettings = null;

export class StorageManager {
  static async init() {
    try {
      const Prefs = window.Capacitor?.Plugins?.Preferences;
      if (Prefs) {
        const statsRes = await Prefs.get({ key: STATS_KEY });
        if (statsRes && statsRes.value) {
          cachedStats = { ...DEFAULT_STATS, ...JSON.parse(statsRes.value) };
          try { localStorage.setItem(STATS_KEY, statsRes.value); } catch (e) {}
        }
        const settingsRes = await Prefs.get({ key: SETTINGS_KEY });
        if (settingsRes && settingsRes.value) {
          cachedSettings = { ...DEFAULT_SETTINGS, ...JSON.parse(settingsRes.value) };
          try { localStorage.setItem(SETTINGS_KEY, settingsRes.value); } catch (e) {}
        }
      }
    } catch (e) {
      console.warn('Capacitor Preferences init warning:', e);
    }
  }

  static getStats() {
    if (cachedStats) return { ...cachedStats };
    try {
      const data = localStorage.getItem(STATS_KEY);
      cachedStats = data ? { ...DEFAULT_STATS, ...JSON.parse(data) } : { ...DEFAULT_STATS };
      return { ...cachedStats };
    } catch (e) {
      console.warn('LocalStorage unavailable:', e);
      return { ...DEFAULT_STATS };
    }
  }

  static saveStats(stats) {
    cachedStats = { ...stats };
    const json = JSON.stringify(stats);
    try {
      localStorage.setItem(STATS_KEY, json);
    } catch (e) {
      console.warn('Failed to save stats to localStorage:', e);
    }

    try {
      const Prefs = window.Capacitor?.Plugins?.Preferences;
      if (Prefs) {
        Prefs.set({ key: STATS_KEY, value: json }).catch(err => {
          console.warn('Failed to write stats to Capacitor Preferences:', err);
        });
      }
    } catch (e) {}
  }

  static recordGameResult(won, triesCount, wordObj) {
    const stats = this.getStats();
    stats.gamesPlayed += 1;

    if (won) {
      stats.gamesWon += 1;
      stats.currentStreak += 1;
      if (stats.currentStreak > stats.maxStreak) {
        stats.maxStreak = stats.currentStreak;
      }
      if (stats.guessDistribution[triesCount] !== undefined) {
        stats.guessDistribution[triesCount] += 1;
      }
    } else {
      stats.currentStreak = 0;
    }

    if (wordObj && wordObj.word && !stats.discoveredWords.includes(wordObj.word)) {
      stats.discoveredWords.push(wordObj.word);
    }

    this.saveStats(stats);
    return stats;
  }

  static getSettings() {
    if (cachedSettings) return { ...cachedSettings };
    try {
      const data = localStorage.getItem(SETTINGS_KEY);
      cachedSettings = data ? { ...DEFAULT_SETTINGS, ...JSON.parse(data) } : { ...DEFAULT_SETTINGS };
      return { ...cachedSettings };
    } catch (e) {
      return { ...DEFAULT_SETTINGS };
    }
  }

  static saveSettings(settings) {
    cachedSettings = { ...settings };
    const json = JSON.stringify(settings);
    try {
      localStorage.setItem(SETTINGS_KEY, json);
    } catch (e) {
      console.warn('Failed to save settings:', e);
    }

    try {
      const Prefs = window.Capacitor?.Plugins?.Preferences;
      if (Prefs) {
        Prefs.set({ key: SETTINGS_KEY, value: json }).catch(err => {
          console.warn('Failed to write settings to Capacitor Preferences:', err);
        });
      }
    } catch (e) {}
  }
}
