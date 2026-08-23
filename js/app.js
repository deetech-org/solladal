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
import { playHaptic } from './tamilUtils.js';

class App {
  constructor() {
    this.wordBank = new WordBank();
    this.storage = StorageManager;
    this.engine = null;
    this.ui = null;
    this.modals = null;
  }

  async init() {
    console.log('Initializing சொல்லாடல் (Solladal) Tamil Word Game...');

    try {
      // 0. Initialize persistent storage (Capacitor Preferences / LocalStorage)
      await this.storage.init();

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

      // 5. Setup Capacitor Native Hooks (Back button, Splash Screen, Status Bar)
      this.setupCapacitorHooks();

      // 6. Restore user preferences and start first game
      const settings = this.storage.getSettings();
      if (settings.lengthPreference) {
        this.ui.setLength(settings.lengthPreference);
      }
      if (settings.complexityPreference) {
        this.ui.setComplexity(settings.complexityPreference);
      }

      this.startNewGame();

      // 7. Register PWA Service Worker for offline capability
      this.registerServiceWorker();

    } catch (err) {
      console.error('Initialization error:', err);
    }
  }

  startNewGame() {
    const lengthFilter = this.ui.getLength();
    const complexityFilter = this.ui.getComplexity();
    
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
      playHaptic('light');
      this.startNewGame();
    });

    // 2. Filter cycle changes (Zero OS Popups)
    if (this.ui.btnLengthToggle) {
      this.ui.btnLengthToggle.addEventListener('click', () => {
        playHaptic('light');
        this.ui.cycleLength();
        this.startNewGame();
      });
    }
    if (this.ui.btnComplexityToggle) {
      this.ui.btnComplexityToggle.addEventListener('click', () => {
        playHaptic('light');
        this.ui.cycleComplexity();
        this.startNewGame();
      });
    }

    // 3. Select letter button
    document.getElementById('btn-select-letter').addEventListener('click', () => {
      const synthesized = this.ui.getCurrentSynthesizedLetter();
      if (synthesized) {
        playHaptic('medium');
        this.engine.insertLetter(synthesized);
        this.ui.clearKeypadSelection();
      } else {
        playHaptic('error');
        this.ui.showToast('எழுத்தைத் தேர்ந்தெடுக்கவும் (Select Mei + Uyir)');
      }
    });

    // 4. Navigation Buttons
    document.getElementById('btn-nav-left').addEventListener('click', () => {
      playHaptic('light');
      this.engine.moveCursorLeft();
    });

    document.getElementById('btn-nav-right').addEventListener('click', () => {
      playHaptic('light');
      this.engine.moveCursorRight();
    });

    // 5. Check Row
    document.getElementById('btn-check-row').addEventListener('click', () => {
      const result = this.engine.checkCurrentRow();
      
      if (!result.success && result.reason === 'INCOMPLETE_ROW') {
        playHaptic('error');
        this.ui.shakeActiveRow(this.engine.currentTry);
        this.ui.showToast('அனைத்து கட்டங்களையும் நிரப்பவும்!');
        return;
      }

      if (result.success) {
        if (result.isGameOver) {
          playHaptic(result.isWin ? 'success' : 'medium');
        } else {
          playHaptic('light');
        }

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
      playHaptic('light');
      this.modals.openModal('modal-wordbank');
    });

    document.getElementById('btn-help-modal').addEventListener('click', () => {
      playHaptic('light');
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

  setupCapacitorHooks() {
    try {
      const AppPlugin = window.Capacitor?.Plugins?.App;
      if (AppPlugin) {
        AppPlugin.addListener('backButton', () => {
          if (this.modals && this.modals.isAnyModalOpen()) {
            this.modals.closeActiveModal();
          } else {
            AppPlugin.exitApp();
          }
        });
      }

      const SplashScreen = window.Capacitor?.Plugins?.SplashScreen;
      if (SplashScreen) {
        SplashScreen.hide().catch(() => {});
      }

      const StatusBar = window.Capacitor?.Plugins?.StatusBar;
      if (StatusBar) {
        StatusBar.setBackgroundColor({ color: '#D97706' }).catch(() => {});
      }
    } catch (e) {
      console.warn('Capacitor hooks setup warning:', e);
    }
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
