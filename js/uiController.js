// js/uiController.js
// -*- coding: utf-8 -*-
/**
 * UI Controller for "சொல்லாடல்" (Solladal).
 * Coordinates DOM rendering, grid updates, keypad matrix interactions,
 * clue animations, and toast notifications.
 */

import { MEI_LETTERS, UYIR_LETTERS, combineMeiUyir } from './tamilUtils.js';

export class UIController {
  constructor(gameEngine) {
    this.engine = gameEngine;
    
    // Keypad state
    this.selectedMei = null;
    this.selectedUyir = null;

    this.cacheDOMElements();
    this.renderKeypads();
  }

  cacheDOMElements() {
    this.gridContainer = document.getElementById('grid-container');
    this.previewMei = document.getElementById('preview-mei');
    this.previewUyir = document.getElementById('preview-uyir');
    this.previewResult = document.getElementById('preview-result');
    
    this.clueCard1 = document.getElementById('clue-card-1');
    this.clueCard2 = document.getElementById('clue-card-2');
    this.clueCard3 = document.getElementById('clue-card-3');
    
    this.clueText1 = document.getElementById('clue-text-1');
    this.clueText2 = document.getElementById('clue-text-2');
    this.clueText3 = document.getElementById('clue-text-3');

    this.meiKeypad = document.getElementById('mei-keypad');
    this.uyirKeypad = document.getElementById('uyir-keypad');

    this.toastEl = document.getElementById('toast-message');
    this.lengthSelect = document.getElementById('length-select');
    this.complexitySelect = document.getElementById('complexity-select');
  }

  renderKeypads() {
    // 1. Render 23 Mei Consonants
    this.meiKeypad.innerHTML = '';
    MEI_LETTERS.forEach(mei => {
      const btn = document.createElement('button');
      btn.className = 'key-btn mei-key';
      btn.textContent = mei;
      btn.dataset.mei = mei;
      btn.addEventListener('click', () => this.handleMeiClick(mei));
      this.meiKeypad.appendChild(btn);
    });

    // 2. Render 13 Uyir Vowels
    this.uyirKeypad.innerHTML = '';
    UYIR_LETTERS.forEach(uyir => {
      const btn = document.createElement('button');
      btn.className = 'key-btn uyir-key';
      btn.textContent = uyir;
      btn.dataset.uyir = uyir;
      btn.addEventListener('click', () => this.handleUyirClick(uyir));
      this.uyirKeypad.appendChild(btn);
    });
  }

  handleMeiClick(mei) {
    // Toggle Mei selection
    if (this.selectedMei === mei) {
      this.selectedMei = null;
    } else {
      this.selectedMei = mei;
    }
    this.updateKeypadHighlights();
    this.updatePreview();
  }

  handleUyirClick(uyir) {
    // Toggle Uyir selection
    if (this.selectedUyir === uyir) {
      this.selectedUyir = null;
    } else {
      this.selectedUyir = uyir;
    }
    this.updateKeypadHighlights();
    this.updatePreview();
  }

  updateKeypadHighlights() {
    // Update Mei active state
    this.meiKeypad.querySelectorAll('.mei-key').forEach(btn => {
      btn.classList.toggle('selected', btn.dataset.mei === this.selectedMei);
    });

    // Update Uyir active state
    this.uyirKeypad.querySelectorAll('.uyir-key').forEach(btn => {
      btn.classList.toggle('selected', btn.dataset.uyir === this.selectedUyir);
    });
  }

  updatePreview() {
    const combined = combineMeiUyir(this.selectedMei, this.selectedUyir);
    if (this.previewMei) {
      this.previewMei.textContent = this.selectedMei || '-';
    }
    if (this.previewUyir) {
      this.previewUyir.textContent = this.selectedUyir || '-';
    }
    if (this.previewResult) {
      this.previewResult.textContent = combined || '?';
    }
  }

  getCurrentSynthesizedLetter() {
    return combineMeiUyir(this.selectedMei, this.selectedUyir);
  }

  clearKeypadSelection() {
    this.selectedMei = null;
    this.selectedUyir = null;
    this.updateKeypadHighlights();
    this.updatePreview();
  }

  /**
   * Re-renders the 6-row grid based on current game state.
   */
  renderGrid(state) {
    this.gridContainer.innerHTML = '';
    const { grid, evaluations, currentTry, currentCol, wordLength, status } = state;

    for (let r = 0; r < 6; r++) {
      const rowDiv = document.createElement('div');
      rowDiv.className = `grid-row row-${r}`;
      rowDiv.dataset.row = r;

      for (let c = 0; c < wordLength; c++) {
        const tile = document.createElement('div');
        tile.className = 'grid-tile';
        tile.dataset.row = r;
        tile.dataset.col = c;

        const letter = grid[r][c] || '';
        tile.textContent = letter;

        if (letter) {
          tile.classList.add('filled');
        }

        // Active highlighted cell (in active playing row)
        if (status === 'PLAYING' && r === currentTry && c === currentCol) {
          tile.classList.add('active-cell');
        }

        // Evaluation colors for checked rows
        const evalColor = evaluations[r][c];
        if (evalColor) {
          tile.classList.add(evalColor);
        }

        // Click to navigate within active row
        tile.addEventListener('click', () => {
          if (r === this.engine.currentTry && status === 'PLAYING') {
            this.engine.selectCol(c);
          }
        });

        rowDiv.appendChild(tile);
      }

      this.gridContainer.appendChild(rowDiv);
    }
  }

  /**
   * Animates row check flip effects.
   */
  animateRowEvaluation(rowIndex, evaluations, callback) {
    const rowEl = this.gridContainer.querySelector(`.row-${rowIndex}`);
    if (!rowEl) return;

    const tiles = rowEl.querySelectorAll('.grid-tile');
    tiles.forEach((tile, colIdx) => {
      setTimeout(() => {
        tile.classList.add('flip');
        tile.classList.add(evaluations[colIdx]);
        if (colIdx === tiles.length - 1 && callback) {
          setTimeout(callback, 300);
        }
      }, colIdx * 120);
    });
  }

  /**
   * Shakes the current row on incomplete submission.
   */
  shakeActiveRow(rowIndex) {
    const rowEl = this.gridContainer.querySelector(`.row-${rowIndex}`);
    if (rowEl) {
      rowEl.classList.remove('shake');
      void rowEl.offsetWidth; // Reflow trigger
      rowEl.classList.add('shake');
    }
  }

  /**
   * Updates the progressive clue cards.
   */
  updateClues(state) {
    const { targetEntry, unlockedClues } = state;
    if (!targetEntry || !targetEntry.clues) return;

    const { clue1, clue2, clue3 } = targetEntry.clues;

    // Clue 1: Always Active
    this.clueCard1.classList.add('active');
    this.clueCard1.classList.remove('locked');
    this.clueText1.innerHTML = `
      <div class="clue-ta">${clue1.ta}</div>
      <div class="clue-en">${clue1.en}</div>
    `;

    // Clue 2: Unlocks before 4th try
    if (unlockedClues[2]) {
      this.clueCard2.classList.add('active');
      this.clueCard2.classList.remove('locked');
      this.clueText2.innerHTML = `
        <div class="clue-ta">${clue2.ta}</div>
        <div class="clue-en">${clue2.en}</div>
      `;
    } else {
      this.clueCard2.classList.remove('active');
      this.clueCard2.classList.add('locked');
      this.clueText2.innerHTML = `<div class="clue-locked-notice">🔒 4-வது முயற்சியில் திறக்கும்</div>`;
    }

    // Clue 3: Unlocks before 5th try
    if (unlockedClues[3]) {
      this.clueCard3.classList.add('active');
      this.clueCard3.classList.remove('locked');
      this.clueText3.innerHTML = `
        <div class="clue-ta">${clue3.ta}</div>
        <div class="clue-en">${clue3.en}</div>
      `;
    } else {
      this.clueCard3.classList.remove('active');
      this.clueCard3.classList.add('locked');
      this.clueText3.innerHTML = `<div class="clue-locked-notice">🔒 5-வது முயற்சியில் திறக்கும்</div>`;
    }
  }

  showToast(message, duration = 2500) {
    if (!this.toastEl) return;
    this.toastEl.textContent = message;
    this.toastEl.style.opacity = '1';
    
    if (this.toastTimeout) clearTimeout(this.toastTimeout);
    this.toastTimeout = setTimeout(() => {
      this.toastEl.style.opacity = '0';
    }, duration);
  }
}
