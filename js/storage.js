// js/storage.js
// -*- coding: utf-8 -*-
/**
 * Persistence layer for Solladal Tamil Word Game PWA.
 * Stores statistics, streaks, and user preferences in localStorage.
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

export class StorageManager {
  static getStats() {
    try {
      const data = localStorage.getItem(STATS_KEY);
      return data ? { ...DEFAULT_STATS, ...JSON.parse(data) } : { ...DEFAULT_STATS };
    } catch (e) {
      console.warn('LocalStorage unavailable:', e);
      return { ...DEFAULT_STATS };
    }
  }

  static saveStats(stats) {
    try {
      localStorage.setItem(STATS_KEY, JSON.stringify(stats));
    } catch (e) {
      console.warn('Failed to save stats to localStorage:', e);
    }
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
    try {
      const data = localStorage.getItem(SETTINGS_KEY);
      return data ? { ...DEFAULT_SETTINGS, ...JSON.parse(data) } : { ...DEFAULT_SETTINGS };
    } catch (e) {
      return { ...DEFAULT_SETTINGS };
    }
  }

  static saveSettings(settings) {
    try {
      localStorage.setItem(SETTINGS_KEY, JSON.stringify(settings));
    } catch (e) {
      console.warn('Failed to save settings:', e);
    }
  }
}
