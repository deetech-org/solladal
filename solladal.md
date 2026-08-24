# சொல்லாடல் (Solladal) — Tamil Word Game PWA

## Comprehensive Design Specification & Technical Architecture Document

## 1. Executive Summary & Vision

**"சொல்லாடல்" (Solladal)** is an educational, elegant, culturally grounded Tamil word-guessing game, designed specifically for Tamil learners in **Grades 1 through 5** (as well as global Tamil enthusiasts). Built on the familiar word-guessing puzzle format, Solladal simplifies Tamil letter input through an intuitive two-step **Mei + Uyir** combination builder while providing progressive bilingual hints from classical literature and contemporary language.

### Core Objectives:

1. **Pedagogical Excellence**: Empower young students (Grades 1–5) to understand Tamil grapheme phonology (உயிர், மெய், உயிர்மெய், ஆய்தம்) naturally through gameplay.

2. **Fluid & Kid-Friendly UX**: Highly responsive, mobile-first touch interface with soft tactile buttons, distinct color coding, and accessible animations.

3. **PWA & 100% Offline Capability**: Instant loading, installable on Android/iOS/Desktop, zero external network dependencies for offline play.

4. **Rich Word Bank Integration**: Backed by `tamilwordbank.md` featuring 1,500 curated words across 5 length categories (1, 2, 3, 4, and 5 letters) and 3 difficulty tiers (Beginner, Intermediate, Advanced).


```
சொல்லாடல் (Solladal) — தமிழ் மொழி ஆர்வலர்களுக்கும், பள்ளி மாணவர்களுக்கும் ஏற்ற முழுமையான தமிழ் சொல் புதிர் விளையாட்டு!      
      
Solladal is an elegant, authentic, and educational Tamil Word Guessing Game crafted for Grade 1 through Grade 5 learners, families, and Tamil enthusiasts worldwide.      
      
🌟 சிறப்பு அம்சங்கள் (Key Features):      
      
• 1,500 தரப்படுத்தப்பட்ட தமிழ் சொற்கள் (1,500 Curated Words):      
  - 1-எழுத்து ஓரெழுத்து ஒருமொழி (100 சொற்கள்)      
  - 2-எழுத்து சொற்கள் (200 சொற்கள்)      
  - 3-எழுத்து சொற்கள் (300 சொற்கள்)      
  - 4-எழுத்து சொற்கள் (400 சொற்கள்)      
  - 5-எழுத்து சொற்கள் (500 சொற்கள்)       
      
• புதுமையான 2-படி தமிழ் விசைப்பலகை (Innovative 2-Step Keypad):      
  மெய் எழுத்து + உயிர் எழுத்து = உயிர்மெய் எழுத்து (எ.கா: \\\\\\\[க்\\\\\\\] + \\\\\\\[ஆ\\\\\\\] = \\\\\\\[கா\\\\\\\]). தமிழ் எழுத்துக்களை எளிதாக உருவாக்கலாம்.      
      
• 3 அடுக்கு பயனுள்ள குறிப்புகள் (3 Progressive Educational Clues):      
  1. பொருள் குறிப்பு (Definition & Meaning - உடனே திறக்கும்)      
  2. இலக்கியக் குறிப்பு (Thirukkural, Aathichoodi, Sangam context - 4வது முயற்சியில்)      
  3. விடுகதை / பயன்பாட்டுக் குறிப்பு (Riddle & Usage - 5வது முயற்சியில்)      
      
• 100% ஆஃப்லைன் வசதி (Fully Offline):      
  இணைய இணைப்பு இல்லாமலும் எங்கும் எப்போதும் விளையாடலாம்.      
      
• முழுமையான பாதுகாப்பு & தனியுரிமை (Private & Child-Safe):      
  விளம்பரங்கள் இல்லை, தனிநபர் தரவு சேகரிப்பு இல்லை, கணக்கு தொடங்க வேண்டிய அவசியமில்லை.      
      
Learn vocabulary, solve cultural riddles, and master Tamil letters daily with சொல்லாடல் (Solladal)!
```

## 2. Information Architecture & UI Layout

The application viewport is split into **three distinct, fixed-flow sections** optimized for single-screen mobile devices (no awkward vertical scrolling required during active gameplay):

```
+-------------------------------------------------------------------+      
| TOP SECTION: Persistent Game Header & Controls                    |      
| - Subsection 1: \\\\\\\[அன்பே இறை\\\\\\\]  சொல்லாடல் / Tamil Word Game  \\\\\\\[அறமே வழி\\\\\\\]   |      
| - Subsection 2: \\\\\\\[Word Length\\\\\\\]        \\\\\\\[Next ❯\\\\\\\]        \\\\\\\[Complexity\\\\\\\]  |      
+-------------------------------------------------------------------+      
| MIDDLE SECTION: Game Board & Progressive Clues                    |      
| +-------------------------------+ +-----------------------------+ |      
| | Left: 6xN Interactive Grid    | | Right: Progressive Clues    | |      
| | Row 1: \\\\\\\[ ? \\\\\\\]\\\\\\\[ ? \\\\\\\]\\\\\\\[ ? \\\\\\\]        | | \\\\\\\[Clue 1: Definition (Open)\\\\\\\] | |      
| | Row 2: \\\\\\\[ ? \\\\\\\]\\\\\\\[ ? \\\\\\\]\\\\\\\[ ? \\\\\\\]        | | \\\\\\\[Clue 2: Lit/Context (4th)\\\\\\\] | |      
| | Row 3: \\\\\\\[ ? \\\\\\\]\\\\\\\[ ? \\\\\\\]\\\\\\\[ ? \\\\\\\]        | | \\\\\\\[Clue 3: Riddle (5th)\\\\\\\]      | |      
| | Row 4 to 6 ...                | |                             | |      
| +-------------------------------+ +-----------------------------+ |      
+-------------------------------------------------------------------+      
| BOTTOM SECTION: UyirMei Grapheme Builder & Keypad Controls        |      
| - Subsection 1: \\\\\\\[Preview Box\\\\\\\] \\\\\\\[Select\\\\\\\] \\\\\\\[ ⬅ \\\\\\\] \\\\\\\[ ➡ \\\\\\\] \\\\\\\[ Check Row ⏎ \\\\\\\]|      
| - Subsection 2: \\\\\\\[Mei Keypad (23)\\\\\\\]   +   \\\\\\\[Uyir Keypad (13)\\\\\\\]        |      
| - Subsection 3: \\\\\\\[ ழ் Word Bank Modal \\\\\\\]     \\\\\\\[ ? How To Play Modal \\\\\\\]|      
+-------------------------------------------------------------------+
```

## 3. Detailed Component Specifications

### 3.1. Top Section: Game Banner & Controls

#### Top-Subsection 1 (Header Banner)

- **Left Item**: Classical Tamil invocation: `அன்பே இறை` with English subtitle `Love is Divine`.

- **Center Title**:

  - Primary: `சொல்லாடல்` (Bold Tamil display typeface).

  - Secondary / Subtitle: `Tamil Word Game` (Clean English subtitle).

- **Right Item**: Ethical Tamil motto: `அறமே வழி` with English subtitle `Virtue is the Path`.

- **Style**: Elevated card aesthetic with gold/amber trim (`\\\\\\\#D97706`), deep temple maroon/navy accents (`\\\\\\\#1E293B`), and crisp typography.

#### Top-Subsection 2 (Session Control Bar)

- **Left: Word-Length Selector (`Random | 1 | 2 | 3 | 4 | 5`)**:

  - Dropdown/segmented pill selector allowing students to practice specific word lengths:

    - `1` — 1-Letter Monosyllabic / Vowel Roots (100 words).

    - `2` — 2-Letter Basic Vocabulary (200 words).

    - `3` — 3-Letter Core Words (300 words).

    - `4` — 4-Letter Compound Words (400 words).

    - `5` — 5-Letter Advanced Words (500 words).

    - `Random` — Automatically picks across all active categories.

- **Middle: `Next` (அடுத்த சொல்) Button**:

  - Fetches a fresh random word matching current filter settings.

  - Pulses gently when a game concludes (Win or Loss state) to prompt the user to continue.

- **Right: Complexity Level Selector (`Beginner | Intermediate | Advanced`)**:

  - Filters vocabulary difficulty tailored for early learners (`Beginner` for Grades 1–2, `Intermediate` for Grades 3–4, `Advanced` for Grade 5+).

### 3.2. Middle Section: Game Grid & Progressive Clues Panel

#### Middle-Left: Dynamic Letter Grid (6 Tries × N Columns)

- **Dimensions**: 6 Rows (fixed 6 attempts) × $N$ Columns ($N \\in \{1, 2, 3, 4, 5\}$ matching the chosen word length).

- **Grapheme Standard**: Exactly 1 square represents 1 complete Tamil grapheme cluster (e.g. `க்`, `கா`, `கை`, `கௌ`, `ஔ`).

- **Active State & Navigation**:

  - Active square is highlighted with an animated focus ring and glow.

  - Start position: Row 1, Col 1 `\\\\\\\[1, 1\\\\\\\]`.

  - Auto-advance: When a letter is inserted via `\\\\\\\[Select\\\\\\\]`, cursor automatically moves to the next square in the current row.

  - Manual navigation: Users can tap any square in the current active row or use the `\\\\\\\[ ⬅ \\\\\\\]` / `\\\\\\\[ ➡ \\\\\\\]` navigation buttons.

- **Color Feedback Rules (Evaluated upon clicking \[Check\])**:

  - 🟩 **Green (`\\\\\\\#16A34A` / `Correct`)**: Letter is present in the target word and in the exact correct position.

  - 🟧 **Orange (`\\\\\\\#EA580C` / `Present Elsewhere`)**: Letter exists in the target word but in a different position.

  - ⬛ **Grey (`\\\\\\\#64748B` / `Absent`)**: Letter does not exist anywhere in the target word.

- **Game End States**:

  - **Win State (வெற்றி)**: All letters in the row turn Green. Confetti celebration triggers, victory banner appears with full word meaning, and the `Next` button highlights.

  - **Loss / Reveal State (விடை)**: If all 6 attempts are exhausted without matching, the actual target word is revealed with full Tamil & English definitions and literary context.

#### Middle-Right: Progressive Clue Panel (மூன்று குறிப்புகள்)

Kids are guided through 3 educational bilingual clues unlocked progressively:

1. **Clue 1 (பொருள் / Definition & Etymology)**:

   - **Always Visible** from the start of Try 1.

   - Gives a clear, child-friendly definition in Tamil and English (e.g. *"மழையினால் பூமியில் ஓடும் நன்னீர் / Freshwater stream"*).

2. **Clue 2 (இலக்கியம் & பயன் / Literary Reference & Context)**:

   - **Locked until Try 4** (Unlocked automatically before attempt 4 starts).

   - Displays Thirukkural, Aathichoodi, or Bharathiyar reference verses.

3. **Clue 3 (விடுகதை & வாக்கியம் / Riddle & Usage Clue)**:

   - **Locked until Try 5** (Unlocked automatically before attempt 5 starts).

   - Displays a fun riddle or contextual fill-in-the-blank sentence.

### 3.3. Bottom Section: Two-Step Tamil Letter Builder Keypad

To eliminate the difficulty of typing complex Tamil compound letters on standard keyboards, Solladal uses a modular **Mei + Uyir** synthesis engine:

#### Bottom-Subsection 1: Synthesis Preview & Row Submission Bar

- **3-Box Grapheme Preview (`\\\\\\\[Mei\\\\\\\] + \\\\\\\[Uyir\\\\\\\] = \\\\\\\[UyirMei\\\\\\\]`)**:

  - Shows 3 educational preview boxes: `\\\\\\\[க்\\\\\\\]` + `\\\\\\\[ஆ\\\\\\\]` = `\\\\\\\[கா\\\\\\\]`, clearly demonstrating to young learners how consonant and vowel combine into a compound letter.

  - If only Mei is pressed $\\rightarrow$ `\\\\\\\[க்\\\\\\\]` + `\\\\\\\[-\\\\\\\]` = `\\\\\\\[க்\\\\\\\]`.

  - If only Uyir is pressed $\\rightarrow$ `\\\\\\\[-\\\\\\\]` + `\\\\\\\[ஆ\\\\\\\]` = `\\\\\\\[ஆ\\\\\\\]`.

  - If both are pressed $\\rightarrow$ `\\\\\\\[க்\\\\\\\]` + `\\\\\\\[ஆ\\\\\\\]` = `\\\\\\\[கா\\\\\\\]`.

- **`\\\\\\\[ Select / தேர்ந்தெடு \\\\\\\]` Action Button**:

  - Commits the previewed letter into the active grid cell.

  - Advances active cell index by +1.

- **Navigation Buttons (`\\\\\\\[ ⬅ \\\\\\\]` and `\\\\\\\[ ➡ \\\\\\\]`)**:

  - Moves active cell selector left or right within the active row to edit previous entries.

- **`\\\\\\\[ Check / சரிபார் \\\\\\\]` Submission Button**:

  - Validates whether all $N$ cells in the active row are filled.

  - If complete: Executes color evaluation, plays feedback animations, and unlocks subsequent clues if conditions are met.

  - If incomplete: Shakes row gently with a helpful tooltip (*"அனைத்து எழுத்துக்களையும் நிரப்பவும்"*).

#### Bottom-Subsection 2: Two-Tier Composite Keyboards with Vertical Divider

- **Left Sub-Panel: 23 Mei (மெய்) Consonants**:

  - Keys: `\\\\\\\[ க், ச், ட், த், ப், ற், ங், ஞ், ண், ந், ம், ன், ய், ர், ல், வ், ழ், ள், க்ஷ், ஜ், ஸ், ஷ், ஹ் \\\\\\\]`

- **Vertical Divider Line**:

  - Crisp vertical divider separating the Mei and Uyir keypad columns.

- **Right Sub-Panel: 13 Uyir (உயிர் & ஆய்தம்) Vowels**:

  - Keys: `\\\\\\\[ அ, ஆ, இ, ஈ, உ, ஊ, எ, ஏ, ஐ, ஒ, ஓ, ஔ, ஃ \\\\\\\]`

- **Combination Logic Matrix**: $$\\text\{Target Grapheme\} = \\text\{Combine\}(\\text\{Selected Mei\}, \\text\{Selected Uyir\})$$

  - Example 1: Tap `த்` + Tap `ஐ` $\\rightarrow$ Preview: `தை`.

  - Example 2: Tap `ம்` + Tap `அ` $\\rightarrow$ Preview: `ம`.

  - Example 3: Tap `ன்` (no vowel) $\\rightarrow$ Preview: `ன்` (Mei consonant with pulli).

  - Example 4: Tap `ஈ` (no consonant) $\\rightarrow$ Preview: `ஈ` (Independent vowel).

#### Bottom-Subsection 3: Utility & Learning Modals

- **Left Button (`\\\\\\\[ ழ் \\\\\\\]` சொல் வங்கி / Word Bank Browser)**:

  - Opens a search-enabled dictionary modal showcasing words from `tamilwordbank.md` categorized by letter length and complexity with audio/visual flashcard previews.

- **Right Button (`\\\\\\\[ ? \\\\\\\]` விளையாடும் முறை / How To Play)**:

  - Opens a child-friendly visual modal with step-by-step instructions in Tamil and English, explaining the green/orange/grey color codes and clue unlocks.

## 4. Grapheme Cluster Engine & Word Logic

### 4.1. Unicode Normalization & Regex Tokenizer

Tamil letters can be represented either as composed or decomposed Unicode sequences. Solladal uses NFC canonical decomposition matching:

```
/\\\\\\\*\\\\\\\*      
 \\\\\\\* Splits a Tamil word into discrete grapheme cluster letters.      
 \\\\\\\* Correctly treats UyirMei (e.g. 'கொ', 'தை', 'கௌ') and pure Mei ('க்', 'ம்')      
 \\\\\\\* as exactly 1 letter unit.      
 \\\\\\\*/      
export function getTamilLetters(word) \\\\\\\{      
  if (!word) return \\\\\\\[\\\\\\\];      
  const normalized = word.normalize('NFC').trim();      
  const regex = /\\\\\\\[\\\\\\\\u0B85-\\\\\\\\u0B94\\\\\\\\u0B83\\\\\\\]|(?:\\\\\\\[\\\\\\\\u0B95-\\\\\\\\u0BB9\\\\\\\\u0B82\\\\\\\]\\\\\\\[\\\\\\\\u0BBE-\\\\\\\\u0BCD\\\\\\\\u0BD7\\\\\\\]\\\\\\\*)/g;      
  return normalized.match(regex) || \\\\\\\[\\\\\\\];      
\\\\\\\}
```

### 4.2. Exact Evaluation Algorithm (Multi-Letter Safe)

To avoid false double-yellow flags on words with duplicate letters:

```
export function evaluateGuess(guessLetters, targetLetters) \\\\\\\{      
  const n = targetLetters.length;      
  const result = new Array(n).fill('grey');      
  const targetLetterCounts = \\\\\\\{\\\\\\\};      
      
  // Pass 1: Identify all exact Green matches      
  for (let i = 0; i \\\\\\\< n; i++) \\\\\\\{      
    const g = guessLetters\\\\\\\[i\\\\\\\];      
    const t = targetLetters\\\\\\\[i\\\\\\\];      
    if (g === t) \\\\\\\{      
      result\\\\\\\[i\\\\\\\] = 'green';      
    \\\\\\\} else \\\\\\\{      
      targetLetterCounts\\\\\\\[t\\\\\\\] = (targetLetterCounts\\\\\\\[t\\\\\\\] || 0) + 1;      
    \\\\\\\}      
  \\\\\\\}      
      
  // Pass 2: Identify Orange (present elsewhere) without exceeding remaining counts      
  for (let i = 0; i \\\\\\\< n; i++) \\\\\\\{      
    if (result\\\\\\\[i\\\\\\\] !== 'green') \\\\\\\{      
      const g = guessLetters\\\\\\\[i\\\\\\\];      
      if (targetLetterCounts\\\\\\\[g\\\\\\\] && targetLetterCounts\\\\\\\[g\\\\\\\] \\\\\\\> 0) \\\\\\\{      
        result\\\\\\\[i\\\\\\\] = 'orange';      
        targetLetterCounts\\\\\\\[g\\\\\\\]--;      
      \\\\\\\}      
    \\\\\\\}      
  \\\\\\\}      
      
  return result;      
\\\\\\\}
```

## 5. Design System Standards

To ensure **Solladal** achieves world-class visual craftsmanship tailored for young Tamil learners (Grades 1–5), the user interface strictly implements a **refined, elegant design system**:

### 5.1. Cultural & Educational Color Palette

- **Theme Identity**: Warm, sacred temple stone and radiant sunshine tones avoiding generic AI neon gradients.

- **Color Tokens**:

  - **Primary Gold / Amber**: `\\\\\\\#D97706` / `\\\\\\\#B45309` (Active highlights, title crest, badges).

  - **Temple Deep Maroon / Navy**: `\\\\\\\#0F172A` / `\\\\\\\#1E293B` (Header backgrounds, high contrast text).

  - **Canvas Background**: `\\\\\\\#FAF7F2` (Warm sandstone parchment, low eye-strain for kids).

  - **Correct Tile (Green)**: `\\\\\\\#16A34A` / Border `\\\\\\\#15803D` (Accessible emerald green).

  - **Present Tile (Orange)**: `\\\\\\\#EA580C` / Border `\\\\\\\#C2410C` (Warm vibrant marigold orange).

  - **Absent Tile (Slate)**: `\\\\\\\#64748B` / Border `\\\\\\\#475569` (Neutral legible slate grey).

  - **Tile Default State**: Background `\\\\\\\#FFFFFF`, Border `\\\\\\\#CBD5E1` (2px solid rounded-lg).

### 5.2. Typographic Scale & Tamil Diacritic Clearance

- **Primary Tamil Typefaces**: Google Fonts `Noto Sans Tamil` and `Mukta Malar` / `Anek Tamil`.

- **Vertical Rhythm & Anti-Clipping**:

  - Tamil diacritics (pulli dots `க்`, comb markers `கொ`, vowel signs `கௌ`) are allotted a `1.35` minimum line-height and generous tile padding to eliminate glyph clipping.

  - Tile font sizing is fluidly mapped with `font-size: clamp(1.25rem, 4.5vw, 2rem)`.

### 5.3. 3D Tactile Affordances for Young Learners

- **Kid-Friendly Touch Targets**:

  - Minimum button height: `44px` (Mei/Uyir keys), `48px` (Action buttons).

  - 3D tactile elevation using multi-layer shadows: `box-shadow: 0 4px 0 var(--btn-shadow)`.

  - Active pressed state: `transform: translateY(3px); box-shadow: 0 1px 0 var(--btn-shadow)` with instant visual feedback.

### 5.4. Strict Single-Screen Mobile Viewport Discipline (`100dvh`)

- **Zero-Scroll Architecture**:

  - Fixed container height: `height: 100dvh; max-height: 100dvh; overflow: hidden;`.

  - CSS Grid distributes space proportionally: Header (`~12%`), Game Grid & Clues (`~42%`), Keypad & Controls (`~46%`).

  - Seamless responsiveness across small phones (iPhone SE 375px), modern flagships (iPhone 14/Galaxy S24), and school iPads/tablets.

### 5.5. Micro-Interactions & Animation Physics

- **Tile Flip Animation**: 3D card rotation `transform: rotateX(180deg)` with a staggered `120ms` delay per column.

- **Row Error Shake**: Snappy horizontal vibration (`@keyframes shake`) when checking incomplete rows.

- **Confetti Celebration**: Lightweight canvas-based particle bursts upon winning a puzzle.

## 6. Technical Architecture & Tech Stack

### 6.1. Tech Stack Selection

- **Architecture**: Single Page Progressive Web App (Vanilla modern ES Modules + HTML5 + CSS Custom Properties).

- **Styles**: Modular CSS (CSS Grid + Flexbox) adhering to the design system's tokens.

- **State Management**: Reactive local state store with `localStorage` persistence:

  - `streak`: Consecutive daily/practice wins.

  - `gamesPlayed`, `winCount`: Win percentages.

  - `guessDistribution`: Histogram of winning rows (1 through 6).

  - `discoveredWords`: Educational glossary of previously solved words.

- **PWA Service Worker**: Cache-First strategy with automatic background update checks.

## 7. Project Structure

```
./solladal      
├── index.html                   \\\\\\\# Main HTML5 Entry with meta tags & PWA manifest link      
├── manifest.json                \\\\\\\# PWA Web App Manifest (icons, standalone display, theme color)      
├── sw.js                        \\\\\\\# Service Worker for 100% offline gameplay caching      
├── css/      
|   ├── style.css                \\\\\\\# Fluid layout, typography, animations & color scheme      
|   └── components.css           \\\\\\\# Grid tiles, keypad keys, modals, clue cards      
├── js/      
|   ├── app.js                   \\\\\\\# Application coordinator & event wiring      
|   ├── gameEngine.js            \\\\\\\# Turn management, state transitions, win/loss evaluator      
|   ├── tamilUtils.js            \\\\\\\# Grapheme tokenizer & Uyir+Mei combination matrix      
|   ├── wordBank.js              \\\\\\\# In-memory indexed dataset parsed from tamilwordbank.md      
|   ├── uiController.js          \\\\\\\# DOM rendering, animations, clue reveal triggers      
|   └── storage.js               \\\\\\\# Statistics, streak, and preferences persistence      
├── assets/      
|   ├── icons/                   \\\\\\\# PWA app icons (192x192, 512x512, maskable)      
|   └── sounds/                  \\\\\\\# Gentle audio feedback (tile\\\\\\\_click, row\\\\\\\_check, win\\\\\\\_cheer)      
├── scripts/      
|   └── build\\\\\\\_pwa\\\\\\\_dataset.js     \\\\\\\# Script converting tamilwordbank.md to optimized words.json      
├── tamilwordbank.md             \\\\\\\# Master word dataset source (1,500 words)      
├── solladal.md                  \\\\\\\# This Master Design Specification      
└── README.md                    \\\\\\\# Project documentation & setup instructions
```

## 8. Implementation Roadmap & Milestones

| Phase | Description | Deliverables |
| - | - | - |
| **Phase 1** | **Data Pipeline & JSON Optimization** | Python/JS script parsing `tamilwordbank.md` into high-performance `words.json`. |
| **Phase 2** | **Core Game Engine & Tamil Keypad Matrix** | `tamilUtils.js`, `gameEngine.js`, and composite Mei+Uyir combination synthesizer. |
| **Phase 3** | **Responsive UI & 3-Section Layout** | Fluid single-screen CSS layout (`100dvh`), grid animations, and clue card unlocks. |
| **Phase 4** | **Modals, Word Bank Browser & Help** | "How to Play" tutorial modal & full searchable Tamil Word Bank viewer. |
| **Phase 5** | **PWA Offline Installation & Audio** | `manifest.json`, `sw.js` Service Worker, tactile audio effects, local storage stats. |
| **Phase 6** | **E2E Testing & Kid-Friendly Validation** | Cross-device testing (Mobile, Tablet, Desktop) across all 5 word lengths. |


