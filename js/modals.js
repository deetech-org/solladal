// js/modals.js
// -*- coding: utf-8 -*-
/**
 * Modals & Word Bank Explorer Controller.
 * Handles opening, closing, searching, and filtering of all interactive dialogs.
 */

export class ModalManager {
  constructor(wordBank, storageManager, onStartNewGame) {
    this.wordBank = wordBank;
    this.storage = storageManager;
    this.onStartNewGame = onStartNewGame;

    this.cacheDOMElements();
    this.bindEvents();
  }

  cacheDOMElements() {
    this.modalWordBank = document.getElementById('modal-wordbank');
    this.modalHelp = document.getElementById('modal-help');
    this.modalGameOver = document.getElementById('modal-gameover');

    this.wbSearchInput = document.getElementById('wb-search-input');
    this.wbLengthFilter = document.getElementById('wb-length-filter');
    this.wbResultsList = document.getElementById('wb-results-list');

    this.goTitle = document.getElementById('gameover-title');
    this.goSolvedWord = document.getElementById('go-solved-word');
    this.goMeaningTa = document.getElementById('go-meaning-ta');
    this.goMeaningEn = document.getElementById('go-meaning-en');
    this.statPlayed = document.getElementById('stat-played');
    this.statWins = document.getElementById('stat-wins');
    this.statStreak = document.getElementById('stat-streak');
    this.btnModalNext = document.getElementById('btn-modal-next-word');
    this.btnShareScore = document.getElementById('btn-share-score');
    this.currentGameOver = null;
  }

  bindEvents() {
    // Close buttons
    document.querySelectorAll('.modal-close-btn').forEach(btn => {
      btn.addEventListener('click', (e) => {
        const modalId = e.target.dataset.close;
        this.closeModal(modalId);
      });
    });

    // Close on backdrop click
    [this.modalWordBank, this.modalHelp, this.modalGameOver].forEach(modal => {
      modal.addEventListener('click', (e) => {
        if (e.target === modal) {
          this.closeModal(modal.id);
        }
      });
    });

    // Word bank search & filter
    this.wbSearchInput.addEventListener('input', () => this.filterWordBank());
    this.wbLengthFilter.addEventListener('change', () => this.filterWordBank());

    // Share Score
    if (this.btnShareScore) {
      this.btnShareScore.addEventListener('click', () => this.shareScore());
    }

    // Next game from modal
    this.btnModalNext.addEventListener('click', () => {
      this.closeModal('modal-gameover');
      if (this.onStartNewGame) {
        this.onStartNewGame();
      }
    });
  }

  openModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
      modal.classList.add('open');
      modal.setAttribute('aria-hidden', 'false');

      if (modalId === 'modal-wordbank') {
        this.filterWordBank();
      }
    }
  }

  closeModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
      modal.classList.remove('open');
      modal.setAttribute('aria-hidden', 'true');
    }
  }

  filterWordBank() {
    const query = this.wbSearchInput.value.trim().toLowerCase();
    const lengthFilter = this.wbLengthFilter.value;
    const allWords = this.wordBank.getAllWords();

    const filtered = allWords.filter(item => {
      // Filter by length
      if (lengthFilter !== 'All' && item.length !== parseInt(lengthFilter, 10)) {
        return false;
      }
      // Filter by query
      if (query) {
        const wordMatch = item.word.toLowerCase().includes(query);
        const taClueMatch = item.clues.clue1.ta.toLowerCase().includes(query) ||
                            item.clues.clue2.ta.toLowerCase().includes(query) ||
                            item.clues.clue3.ta.toLowerCase().includes(query);
        const enClueMatch = item.clues.clue1.en.toLowerCase().includes(query) ||
                            item.clues.clue2.en.toLowerCase().includes(query) ||
                            item.clues.clue3.en.toLowerCase().includes(query);
        return wordMatch || taClueMatch || enClueMatch;
      }
      return true;
    });

    this.renderWordBankResults(filtered.slice(0, 100)); // Render top 100 for fast responsiveness
  }

  renderWordBankResults(words) {
    this.wbResultsList.innerHTML = '';
    if (words.length === 0) {
      this.wbResultsList.innerHTML = `<div style="text-align: center; color: #64748B; padding: 20px;">சொற்கள் எதுவும் கிடைக்கவில்லை (No words found).</div>`;
      return;
    }

    words.forEach(item => {
      const card = document.createElement('div');
      card.className = 'wb-item-card';
      card.innerHTML = `
        <div class="wb-item-header">
          <span class="wb-item-word">${item.word}</span>
          <span class="wb-item-badge">${item.length} எழுத்து • ${item.complexity}</span>
        </div>
        <div class="wb-item-meaning-ta">${item.clues.clue1.ta}</div>
        <div class="wb-item-meaning-en">${item.clues.clue1.en}</div>
      `;
      this.wbResultsList.appendChild(card);
    });
  }

  isAnyModalOpen() {
    const openModal = document.querySelector('.modal-overlay.open');
    return !!openModal;
  }

  closeActiveModal() {
    const openModal = document.querySelector('.modal-overlay.open');
    if (openModal) {
      this.closeModal(openModal.id);
      return true;
    }
    return false;
  }

  showGameOverModal(isWin, targetEntry) {
    const stats = this.storage.getStats();
    this.currentGameOver = { isWin, targetEntry, stats };
    
    if (isWin) {
      this.goTitle.textContent = '🎉 அருமை! வெற்றி பெற்றீர்கள்!';
    } else {
      this.goTitle.textContent = '💡 விடை: ' + targetEntry.word;
    }

    this.goSolvedWord.textContent = targetEntry.word;
    this.goMeaningTa.textContent = targetEntry.clues.clue1.ta;
    this.goMeaningEn.textContent = targetEntry.clues.clue1.en;

    this.statPlayed.textContent = stats.gamesPlayed;
    this.statWins.textContent = stats.gamesWon;
    this.statStreak.textContent = stats.currentStreak;

    this.openModal('modal-gameover');
  }

  async shareScore() {
    if (!this.currentGameOver) return;
    const { isWin, targetEntry, stats } = this.currentGameOver;
    const outcome = isWin ? 'வெற்றி (Solved!)' : 'விடை (Solution)';
    const text = `சொல்லாடல் (Solladal) — தமிழ் சொல் விளையாட்டு\n` +
      `🎯 சொல்: ${targetEntry.word} — ${outcome}\n` +
      `🔥 தொடர் வெற்றி: ${stats.currentStreak} | ஆடியவை: ${stats.gamesPlayed}\n` +
      `விளையாட: https://deetech.org/solladal`;

    try {
      const Share = window.Capacitor?.Plugins?.Share;
      if (Share) {
        await Share.share({
          title: 'சொல்லாடல் (Solladal)',
          text: text,
          dialogTitle: 'Share your Solladal score'
        });
        return;
      }
    } catch (e) {
      // Fall through to web share or clipboard
    }

    if (navigator.share) {
      try {
        await navigator.share({
          title: 'சொல்லாடல் (Solladal)',
          text: text
        });
        return;
      } catch (e) {}
    }

    if (navigator.clipboard) {
      try {
        await navigator.clipboard.writeText(text);
        const toast = document.getElementById('toast-message');
        if (toast) {
          toast.textContent = 'முடிவுகள் நகலெடுக்கப்பட்டன! (Copied)';
          toast.style.opacity = '1';
          setTimeout(() => { toast.style.opacity = '0'; }, 2000);
        }
      } catch (e) {}
    }
  }
}
