// js/wordBank.js
// -*- coding: utf-8 -*-
/**
 * Word Bank Manager.
 * Loads data/words.json and provides filtering by length and complexity.
 */

export class WordBank {
  constructor() {
    this.data = null;
    this.isLoaded = false;
  }

  async load() {
    if (this.isLoaded) return;
    try {
      const response = await fetch('data/words.json');
      if (!response.ok) {
        throw new Error(`Failed to load word bank: HTTP ${response.status}`);
      }
      this.data = await response.json();
      this.isLoaded = true;
      console.log(`WordBank loaded with ${this.data.metadata.totalWords} words.`);
    } catch (err) {
      console.error('Error loading WordBank:', err);
      throw err;
    }
  }

  /**
   * Selects a random word entry based on length and complexity filters.
   * @param {string|number} lengthFilter - 'Random' or 1..5
   * @param {string} complexityFilter - 'Beginner', 'Intermediate', 'Advanced', or 'All'
   * @returns {object} Word entry object
   */
  getRandomWord(lengthFilter = 'Random', complexityFilter = 'Beginner') {
    if (!this.isLoaded || !this.data) {
      throw new Error('WordBank not loaded yet.');
    }

    let candidates = [];

    // Filter by length
    if (lengthFilter === 'Random' || !lengthFilter) {
      candidates = this.data.all;
    } else {
      const lenNum = parseInt(lengthFilter, 10);
      candidates = this.data.byLength[lenNum] || this.data.all;
    }

    // Filter by complexity if specified
    if (complexityFilter && complexityFilter !== 'All') {
      const filteredByComp = candidates.filter(w => w.complexity.toLowerCase() === complexityFilter.toLowerCase());
      if (filteredByComp.length > 0) {
        candidates = filteredByComp;
      }
    }

    if (candidates.length === 0) {
      candidates = this.data.all;
    }

    const randomIndex = Math.floor(Math.random() * candidates.length);
    return candidates[randomIndex];
  }

  getAllWords() {
    return this.data ? this.data.all : [];
  }

  getMetadata() {
    return this.data ? this.data.metadata : null;
  }
}
