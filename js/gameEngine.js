// js/gameEngine.js
// -*- coding: utf-8 -*-
/**
 * Game Engine for "சொல்லாடல்" (Solladal) Tamil Word Game.
 * Handles game state, turn flow, color evaluation, clue unlock conditions, and events.
 */

import { getTamilLetters } from './tamilUtils.js';

export const GAME_STATUS = {
  PLAYING: 'PLAYING',
  WON: 'WON',
  LOST: 'LOST'
};

export const MAX_TRIES = 6;

export class GameEngine {
  constructor(wordBank, storageManager) {
    this.wordBank = wordBank;
    this.storage = storageManager;
    
    this.targetWordEntry = null;
    this.targetLetters = [];
    this.wordLength = 3;
    
    this.currentTry = 0; // 0 to 5 (Row 1 to 6)
    this.currentCol = 0; // 0 to wordLength - 1
    
    // 6 rows x wordLength grid array of strings
    this.grid = [];
    // 6 rows x wordLength evaluation array ('green', 'orange', 'grey', null)
    this.evaluations = [];
    
    this.status = GAME_STATUS.PLAYING;
    this.unlockedClues = { 1: true, 2: false, 3: false };
    
    this.listeners = [];
  }

  onStateChange(fn) {
    this.listeners.push(fn);
  }

  notifyStateChange() {
    this.listeners.forEach(fn => fn(this.getState()));
  }

  /**
   * Starts a new game with the given filters.
   */
  startNewGame(lengthFilter = 'Random', complexityFilter = 'Beginner') {
    this.targetWordEntry = this.wordBank.getRandomWord(lengthFilter, complexityFilter);
    this.targetLetters = this.targetWordEntry.letters;
    this.wordLength = this.targetLetters.length;

    this.currentTry = 0;
    this.currentCol = 0;
    this.status = GAME_STATUS.PLAYING;

    // Initialize 6 rows grid
    this.grid = Array.from({ length: MAX_TRIES }, () => Array(this.wordLength).fill(''));
    this.evaluations = Array.from({ length: MAX_TRIES }, () => Array(this.wordLength).fill(null));

    // Clue 1 is always unlocked; Clues 2 & 3 unlocked before tries 4 & 5 respectively
    this.unlockedClues = {
      1: true,
      2: false,
      3: false
    };

    this.notifyStateChange();
  }

  /**
   * Inserts a letter into the currently active grid cell.
   * @param {string} letter 
   */
  insertLetter(letter) {
    if (this.status !== GAME_STATUS.PLAYING) return;
    if (this.currentTry >= MAX_TRIES) return;

    this.grid[this.currentTry][this.currentCol] = letter;

    // Auto-advance column if not at the last column of current row
    if (this.currentCol < this.wordLength - 1) {
      this.currentCol += 1;
    }

    this.notifyStateChange();
  }

  /**
   * Clears the current cell or moves back.
   */
  backspace() {
    if (this.status !== GAME_STATUS.PLAYING) return;

    if (this.grid[this.currentTry][this.currentCol] !== '') {
      this.grid[this.currentTry][this.currentCol] = '';
    } else if (this.currentCol > 0) {
      this.currentCol -= 1;
      this.grid[this.currentTry][this.currentCol] = '';
    }

    this.notifyStateChange();
  }

  /**
   * Moves column cursor left within active row.
   */
  moveCursorLeft() {
    if (this.currentCol > 0) {
      this.currentCol -= 1;
      this.notifyStateChange();
    }
  }

  /**
   * Moves column cursor right within active row.
   */
  moveCursorRight() {
    if (this.currentCol < this.wordLength - 1) {
      this.currentCol += 1;
      this.notifyStateChange();
    }
  }

  /**
   * Sets active column directly (e.g. on tile click in current row).
   */
  selectCol(colIndex) {
    if (colIndex >= 0 && colIndex < this.wordLength) {
      this.currentCol = colIndex;
      this.notifyStateChange();
    }
  }

  /**
   * Validates and evaluates the current completed row.
   * Returns evaluation result or error message if row is incomplete.
   */
  checkCurrentRow() {
    if (this.status !== GAME_STATUS.PLAYING) return { success: false, reason: 'GAME_OVER' };

    const rowLetters = this.grid[this.currentTry];
    const isComplete = rowLetters.every(cell => cell && cell.trim() !== '');

    if (!isComplete) {
      return { success: false, reason: 'INCOMPLETE_ROW' };
    }

    // Evaluate row with multi-letter safe logic
    const rowEval = this.evaluateGuess(rowLetters, this.targetLetters);
    this.evaluations[this.currentTry] = rowEval;

    const isWin = rowEval.every(status => status === 'green');

    if (isWin) {
      this.status = GAME_STATUS.WON;
      this.unlockedClues = { 1: true, 2: true, 3: true };
      this.storage.recordGameResult(true, this.currentTry + 1, this.targetWordEntry);
    } else if (this.currentTry === MAX_TRIES - 1) {
      this.status = GAME_STATUS.LOST;
      this.unlockedClues = { 1: true, 2: true, 3: true };
      this.storage.recordGameResult(false, MAX_TRIES, this.targetWordEntry);
    } else {
      // Advance to next row
      this.currentTry += 1;
      this.currentCol = 0;

      // Check progressive clue unlock triggers:
      // Clue 2: Unlocked before 4th try (currentTry >= 3)
      if (this.currentTry >= 3) {
        this.unlockedClues[2] = true;
      }
      // Clue 3: Unlocked before 5th try (currentTry >= 4)
      if (this.currentTry >= 4) {
        this.unlockedClues[3] = true;
      }
    }

    this.notifyStateChange();
    return { success: true, isWin, isGameOver: this.status !== GAME_STATUS.PLAYING, evaluations: rowEval };
  }

  /**
   * Multi-letter safe color evaluation algorithm:
   * 🟩 Green: Correct letter & position
   * 🟧 Orange: Correct letter, wrong position
   * ⬛ Grey: Absent letter
   */
  evaluateGuess(guessLetters, targetLetters) {
    const n = targetLetters.length;
    const result = new Array(n).fill('grey');
    const targetCounts = {};

    // Pass 1: Green matches
    for (let i = 0; i < n; i++) {
      const g = guessLetters[i];
      const t = targetLetters[i];
      if (g === t) {
        result[i] = 'green';
      } else {
        targetCounts[t] = (targetCounts[t] || 0) + 1;
      }
    }

    // Pass 2: Orange matches
    for (let i = 0; i < n; i++) {
      if (result[i] !== 'green') {
        const g = guessLetters[i];
        if (targetCounts[g] && targetCounts[g] > 0) {
          result[i] = 'orange';
          targetCounts[g] -= 1;
        }
      }
    }

    return result;
  }

  getState() {
    return {
      targetWord: this.targetWordEntry ? this.targetWordEntry.word : '',
      targetEntry: this.targetWordEntry,
      wordLength: this.wordLength,
      currentTry: this.currentTry,
      currentCol: this.currentCol,
      grid: this.grid,
      evaluations: this.evaluations,
      status: this.status,
      unlockedClues: this.unlockedClues
    };
  }
}
