// js/app.js
// -*- coding: utf-8 -*-
/**
 * Application Coordinator for "சொல்லாடல்" (Solladal) Tamil Word Game PWA.
 * Bootstraps modules, binds event listeners, handles keyboard input, and registers Service Worker.
 */

import { WordBank } from './wordBank.js';
import { StorageManager } from './storage.js';
import { GameEngine } from './gameEngine.js';
import { UIController } from './uiController.js';
import { ModalManager } from './modals.js';

class App {
  constructor() {
    this.wordBank = new WordBank();
    this.storage = StorageManager;
    this.engine = null;
    this.ui = null;
    this.modals = null;
  }

  async init() {
    console.log('Initializing சொல்லாடல் (Solladal) Tamil Word Game PWA...');

    try {
      // 1. Load dataset
      await this.wordBank.load();

      // 2. Initialize Game Engine & UI
      this.engine = new GameEngine(this.wordBank, this.storage);
      this.ui = new UIController(this.engine);
      this.modals = new ModalManager(this.wordBank, this.storage, () => this.startNewGame());

      // 3. Subscribe UI to Engine state changes
      this.engine.onStateChange((state) => {
        this.ui.renderGrid(state);
        this.ui.updateClues(state);
      });

      // 4. Bind Action Buttons
      this.bindActions();

      // 5. Restore user preferences and start first game
      const settings = this.storage.getSettings();
      if (settings.lengthPreference) {
        this.ui.lengthSelect.value = settings.lengthPreference;
      }
      if (settings.complexityPreference) {
        this.ui.complexitySelect.value = settings.complexityPreference;
      }

      this.startNewGame();

      // 6. Register PWA Service Worker for offline capability
      this.registerServiceWorker();

    } catch (err) {
      console.error('Initialization error:', err);
    }
  }

  startNewGame() {
    const lengthFilter = this.ui.lengthSelect.value;
    const complexityFilter = this.ui.complexitySelect.value;
    
    // Save settings
    this.storage.saveSettings({
      lengthPreference: lengthFilter,
      complexityPreference: complexityFilter
    });

    this.ui.clearKeypadSelection();
    this.engine.startNewGame(lengthFilter, complexityFilter);
  }

  bindActions() {
    // 1. Next Word Button
    document.getElementById('btn-next-word').addEventListener('click', () => {
      this.startNewGame();
    });

    // 2. Filter changes
    this.ui.lengthSelect.addEventListener('change', () => this.startNewGame());
    this.ui.complexitySelect.addEventListener('change', () => this.startNewGame());

    // 3. Select letter button
    document.getElementById('btn-select-letter').addEventListener('click', () => {
      const synthesized = this.ui.getCurrentSynthesizedLetter();
      if (synthesized) {
        this.engine.insertLetter(synthesized);
        this.ui.clearKeypadSelection();
      } else {
        this.ui.showToast('எழுத்தைத் தேர்ந்தெடுக்கவும் (Select Mei + Uyir)');
      }
    });

    // 4. Navigation Buttons
    document.getElementById('btn-nav-left').addEventListener('click', () => {
      this.engine.moveCursorLeft();
    });

    document.getElementById('btn-nav-right').addEventListener('click', () => {
      this.engine.moveCursorRight();
    });

    // 5. Check Row
    document.getElementById('btn-check-row').addEventListener('click', () => {
      const result = this.engine.checkCurrentRow();
      
      if (!result.success && result.reason === 'INCOMPLETE_ROW') {
        this.ui.shakeActiveRow(this.engine.currentTry);
        this.ui.showToast('அனைத்து கட்டங்களையும் நிரப்பவும்!');
        return;
      }

      if (result.success) {
        const evalRow = this.engine.currentTry - (result.isGameOver ? 0 : 1);
        this.ui.animateRowEvaluation(evalRow, result.evaluations, () => {
          if (result.isGameOver) {
            this.modals.showGameOverModal(result.isWin, this.engine.targetWordEntry);
          }
        });
      }
    });

    // 6. Utility Modal Buttons
    document.getElementById('btn-wordbank-modal').addEventListener('click', () => {
      this.modals.openModal('modal-wordbank');
    });

    document.getElementById('btn-help-modal').addEventListener('click', () => {
      this.modals.openModal('modal-help');
    });

    // 7. Hardware Keyboard Event Listener (for Desktop users)
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Backspace') {
        this.engine.backspace();
      } else if (e.key === 'Enter') {
        document.getElementById('btn-check-row').click();
      } else if (e.key === 'ArrowLeft') {
        this.engine.moveCursorLeft();
      } else if (e.key === 'ArrowRight') {
        this.engine.moveCursorRight();
      }
    });
  }

  registerServiceWorker() {
    if ('serviceWorker' in navigator) {
      window.addEventListener('load', () => {
        navigator.serviceWorker.register('sw.js')
          .then(reg => console.log('ServiceWorker registered with scope:', reg.scope))
          .catch(err => console.warn('ServiceWorker registration failed:', err));
      });
    }
  }
}

// Instantiate and bootstrap
const app = new App();
app.init();
