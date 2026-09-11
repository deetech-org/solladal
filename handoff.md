# "சொல்லாடல்" (Solladal) — Tamil Word Game (v1.3.3)

## Master Handoff & Project Delivery Document

**Publisher:** `deetech.org` • **App ID / Bundle ID:** `org.deetech.solladal`  
**Platforms:** Web (PWA), Cloudflare Pages (`solladal.app`), Android (Google Play Store), iOS (App Store)  
**Status:** 🚀 **Version 1.3.3 Built & Verified Across All 4 Targets** (Android Version Code `5`, iOS Build `7`, `1,714` Words)

---

## 1. Executive Summary & Architecture Overview

**"சொல்லாடல்" (Solladal)** is an educational, elegant, and culturally authentic Tamil word-guessing game designed for Grade 1 through Grade 5 students and Tamil learners worldwide.

The application uses a **vanilla HTML/CSS/JS PWA core** wrapped **1:1 with Capacitor** for native mobile app distribution and static hosting pipelines:

- **Zero UI Rewrite:** 100% reuse of the web game engine, styles, and 1,714-word offline dictionary.
- **Asset Staging (`./www`):** `npm run prep:mobile` stages only runtime assets into `www/`, isolating source files, markdown, and build caches from release bundles.
- **Keypad Matrix with `ஸ்ரீ` (Sri):** Full 6×4 matrix symmetry (24 Mei keys) with single-touch input for the auspicious grapheme cluster `ஸ்ரீ`.
- **Four Production Release Targets:**
  1. **Web PWA (`./www`)** — Prepped runtime bundle deployed to GitHub Pages via CI.
  2. **Cloudflare Pages (`solladal.app`)** — Dedicated web release with landing gate overlay and isolated Service Worker scope (`/play/`).
  3. **Android Target (`org.deetech.solladal`)** — Built locally on Windows using OpenJDK 21, Android SDK (API 35/36), and Gradle (`app-release.aab`).
  4. **iOS Target (`org.deetech.solladal`)** — Built in the cloud via GitHub Actions on `macos-latest` runners (Xcode, CocoaPods, automated signing & TestFlight upload).

```
                        ┌─────────────────────────────────────────────────────────┐    
                        │         சொல்லாடல் (Solladal) Word-Game Core            │    
                        │   (1,714 Words, 24 Mei Keys with ஸ்ரீ, 3 Clues, CSS)     │    
                        │   Vanilla HTML/CSS/JS PWA — served from repo root       │    
                        └────────────────────────────┬────────────────────────────┘    
                                                     │  npm run prep:mobile → ./www    
                                            ┌────────┴────────┐    
                                            │  Capacitor Core │  (100% code reuse)    
                                            └────────┬────────┘    
                   ┌────────────────────────┬────────┴────────┬────────────────────────┐
                   ▼                        ▼                 ▼                        ▼
        ┌──────────────────────┐ ┌──────────────────────┐ ┌──────────────────────┐ ┌──────────────────────┐
        │  1. WWW / GH Pages   │ │ 2. Cloudflare Pages  │ │     3. Android       │ │        4. iOS        │
        │    (GitHub Actions)  │ │   (solladal.app)     │ │    (Google Play)     │ │     (App Store)      │
        ├──────────────────────┤ ├──────────────────────┤ ├──────────────────────┤ ├──────────────────────┤
        │ Output: ./www        │ │ Output: cf/public/   │ │ Output: app-release  │ │ Output: App.ipa      │
        │ Cache: solladal-1.3.3│ │ Script: build.mjs    │ │ Gradle bundleRelease │ │ GitHub Actions macOS │
        │ Staged via prep      │ │ Cache: cf3 overlay   │ │ Target: v1.3.3 (4)   │ │ Target: v1.3.3 (7)   │
        └──────────────────────┘ └──────────────────────┘ └──────────────────────┘ └──────────────────────┘
```

---

## 2. Keypad Matrix & Input Synthesis Architecture (v1.3.3)

In Version 1.3.3, the virtual keyboard was upgraded to incorporate the auspicious Grantha grapheme **`ஸ்ரீ` (Sri)** as an atomic, single-letter button.

### Visual Symmetry (24 Mei Keys)
The Mei keypad layout is rendered as a 6-column grid (`grid-template-columns: repeat(6, 1fr)`). Appending `ஸ்ரீ` to the end of the 5 Grantha consonants creates a complete 4-row layout with zero orphan slots:
- **Row 1 (வல்லினம் - Hard Consonants, 6 keys):** `க்` `ச்` `ட்` `த்` `ப்` `ற்`
- **Row 2 (மெல்லினம் - Soft Consonants, 6 keys):** `ங்` `ஞ்` `ண்` `ந்` `ம்` `ன்`
- **Row 3 (இடையினம் - Medial Consonants, 6 keys):** `ய்` `ர்` `ல்` `வ்` `ழ்` `ள்`
- **Row 4 (கிரந்தம் & ஸ்ரீ, 6 keys):** `க்ஷ்` `ஜ்` `ஸ்` `ஷ்` `ஹ்` **`ஸ்ரீ`**

### Synthesis & Exclusivity Engine
- **`combineMeiUyir('ஸ்ரீ', uyir)`**: Always returns `'ஸ்ரீ'` directly.
- **Input Exclusivity**: Because `ஸ்ரீ` contains a built-in vowel diacritic, selecting `ஸ்ரீ` automatically resets any active Uyir vowel selection, and selecting an Uyir vowel resets `ஸ்ரீ`.
- **Grapheme Tokenizer**: `getTamilLetters()` in `js/tamilUtils.js` and `split_graphemes()` in Python recognize `(?:ஸ்ரீ|ஸ்ரீ|ஶ்ரீ)` as an indivisible 1-letter token.

---

## 3. Responsive Layout Architecture (`100dvh` Discipline)

The UI uses a **Zero-Scroll (`100dvh`)** layout with dynamic viewport height and safe-area insets (`env(safe-area-inset-*)`), preventing page overflow across phones and tablets:

```
+-----------------------------------------------------------------------------------------+  
| TOP SECTION: Persistent Cultural Banner & Tactile Cycle Controls                        |  
| - Subsection 1: [அன்பே இறை / Love is Divine]   சொல்லாடல்   [அறமே வழி / Virtue is the Path]|  
| - Subsection 2: [ 3 எழுத்து ▾ ] (Cycle)    [அடுத்த சொல் ❯]    [ Beginner ▾ ] (Cycle)       |  
|   * Zero OS modal pickers / dialogs on mobile; cycles directly in-place with haptics    |  
+-----------------------------------------------------------------------------------------+  
| MIDDLE SECTION: Game Board Grid (Top) + Progressive Clues (Bottom)                      |  
| - Middle-Top: 6 Rows x N Columns Dynamic Tiles [ ? ][ ? ][ ? ] (Full comfortable size)  |  
| - Middle-Bottom: Progressive Clues Panel (Snug below Grid with Custom Gold Scrollbar):   |  
|   • 💡 குறிப்பு 1 (பொருள்): சொல் பொருள் (English meaning)                                  |  
|   • 🔒 குறிப்பு 2 (இலக்கியம்): 4-வது முயற்சியில் திறக்கும்                                    |  
|   • 🔒 குறிப்பு 3 (விடுகதை): 5-வது முயற்சியில் திறக்கும்                                     |  
+-----------------------------------------------------------------------------------------+  
| BOTTOM SECTION: Grouped Synthesizer & Two-Tier Keypad Matrix                            |  
| - Subsection 1: [ [க்] + [ஆ] = [கா] [✓] ]         [ ‹ ] [ › ] (SVG)   [சரிபார் ⏎]        |  
|   * Tick [✓] attached next to synthesized tile; dedicated room for Nav & Check buttons  |  
| - Subsection 2: [ 24 Mei Keys (Left: 6x4) ]  | (Divider) |  [ 13 Uyir Keys (Right: 4x4) ]|  
|   * Perfectly symmetrical grid; ergonomic button height clamp(26px, 4.0vh, 32px)        |  
| - Subsection 3:          [ ழ் சொல் வங்கி ]      [ ? விளையாடும் முறை ] (Centered in Middle) |  
+-----------------------------------------------------------------------------------------+
```

---

## 4. Master Word Bank (1,714 Words)

The word bank was expanded in v1.3.3 by promoting all **43 candidate words** from [`words-to-be-added.md`](words-to-be-added.md) into the primary source of truth [`tamilwordbank-v2.md`](tamilwordbank-v2.md).

### Word Bank Distribution by Letter Length
- **1-Letter Words:** `100` words (e.g. `ஆ`, `ஈ`, `ஊ`, `கோ`, `தீ`, `பூ`, `தை`)
- **2-Letter Words:** `252` words (+2: `காணி`, `பொறை`)
- **3-Letter Words:** `394` words (+18: `நுண்மை`, `நிறைவு`, `பாப்பா`, `சக்தி`, `மாதர்`, `வையம்`, `இன்னா`, `நயன்`, `சிவம்`, `தெள்ளு`, `தில்லை`, `ஈசன்`, `யோகம்`, `ஞானம்`, `பொதுமை`, `நீரோடை`, `ஸ்ரீமான்`, `ஸ்ரீமதி`)
- **4-Letter Words:** `453` words (+16: `ஒழுங்கு`, `ஒளிர்வு`, `பாரதம்`, `வல்லமை`, `முழங்கு`, `ஊழியம்`, `செங்கோல்`, `அம்மானை`, `பிராணன்`, `வாழ்க்கை`, `பயணம்`, `பாட்டாளி`, `தாயகம்`, `ஸ்ரீவள்ளி`, `ஸ்ரீபதம்`, `ஸ்ரீபுரம்`)
- **5-Letter Words:** `515` words (+7: `குடியுரிமை`, `ஆனந்தம்`, `மாணிக்கம்`, `பூங்காற்று`, `வசந்தம்`, `பொன்மகள்`, `ஸ்ரீரங்கம்`)
- **TOTAL ACTIVE WORD BANK:** **`1,714 words`**

### Word Bank Generation & Validation Pipeline
```powershell
# 1. Rebuild data/words.json and auto-bump sw.js CACHE_NAME
$env:PYTHONIOENCODING="utf-8"; python scripts/build_wordbank.py

# 2. Run automated PWA integration tests (validates all 1,714 words & multi-letter logic)
$env:PYTHONIOENCODING="utf-8"; python scripts/test_pwa_integration.py

# 3. Audit candidate words staging queue (0 leaks, 0 collisions)
$env:PYTHONIOENCODING="utf-8"; python scripts/audit_words_to_be_added.py --allow-promoted
```

---

## 5. File Inventory & Repository Structure

```
./solladal/
├── index.html                   # HTML5 entry (v1.3.3 footer, 24 Mei keypad layout, strict CSP)
├── manifest.json                # Web App Manifest (v1.3.3)
├── sw.js                        # Service Worker caching all runtime assets (v1.3.3 content hash)
├── package.json                 # Node dependencies & staging scripts (v1.3.3)
├── package-lock.json            # Lockfile (v1.3.3)
├── capacitor.config.json        # Capacitor configuration (appId: org.deetech.solladal)
├── v-1-3-3-plan.md              # Master Build & Release Plan for v1.3.3
├── words-to-be-added.md         # Staged candidate words repository (43 words promoted in v1.3.3)
├── tamilwordbank-v2.md          # Master Source-of-Truth Markdown Table (1,714 words)
├── css/
│   └── style.css                # Polished CSS (100dvh viewport, 6-column Mei keypad, safe-area insets)
├── js/
│   ├── app.js                   # App coordinator, Capacitor back button, haptics, cycle actions
│   ├── gameEngine.js            # Turn manager, multi-letter evaluator, progressive clue triggers
│   ├── tamilUtils.js            # 24 Mei + 13 Uyir letters, ಶ್ರೀ synthesis, grapheme tokenizer
│   ├── wordBank.js              # In-memory dataset manager & random selector
│   ├── uiController.js          # DOM renderer, 3-box preview updater, ಶ್ರೀ exclusivity logic
│   ├── modals.js                # Searchable Word Bank explorer, Help modal & Game Over dialog
│   └── storage.js               # Durable persistence (@capacitor/preferences + localStorage)
├── data/
│   └── words.json               # 1,714 indexed Tamil words with 3 bilingual clues each
├── cloudflare/                  # Cloudflare Pages release pipeline (solladal.app)
│   ├── build.mjs                # Assembles play/ runtime and gate overlay
│   ├── overlay/                 # landing.html, privacy.html, license.html, overlay manifest & sw.js
│   └── public/                  # Deployable output directory (33 files)
├── android/                     # Local Android native project (compileSdkVersion 35)
│   ├── app/
│   │   ├── build.gradle         # Application gradle config (versionCode 4, versionName 1.3.3)
│   │   └── src/main/            # AndroidManifest.xml & native assets
│   └── build.gradle
├── ios/                         # iOS native project for Cloud CI
│   ├── App/
│   │   ├── App.xcodeproj/       # project.pbxproj (MARKETING_VERSION 1.3.3, CURRENT_PROJECT_VERSION 7)
│   │   ├── App/Info.plist       # Non-exempt encryption false & portrait lock
│   │   └── ExportOptions.plist  # App Store distribution export configuration
│   └── Podfile
├── .github/
│   └── workflows/
│       ├── ios-release.yml      # Automated macOS cloud build & TestFlight upload workflow
│       └── pages.yml            # Automated GitHub Pages web deployment workflow
├── scripts/
│   ├── build_wordbank.py        # Master v2 word bank compiler & sw.js cache bumper (v1.3.3)
│   ├── promote_words.py         # Candidate words promotion script
│   ├── audit_words_to_be_added.py # Leak gate and candidate validator
│   ├── test_pwa_integration.py  # Master test suite validating all PWA & asset components
│   └── tamil_utils.py           # Python Tamil grapheme regex tokenizer
├── PRIVACY.md                   # Family & COPPA compliant privacy policy
└── handoff.md                   # This Master Project Delivery Document
```

---

## 6. How to Build & Deploy All Four Release Targets

### Target 1: Web PWA (`./www`) & GitHub Pages
```powershell
# Stage web bundle into ./www
npm run prep:mobile

# Pushing to main branch automatically triggers .github/workflows/pages.yml
git push origin main
```

### Target 2: Cloudflare Pages (`solladal.app`)
```powershell
# Assemble site in cloudflare/public/
node cloudflare/build.mjs

# Deploy to Cloudflare Pages (CLI or Git)
npx wrangler pages deploy cloudflare/public --project-name solladal-app
```

### Target 3: Android Release (`app-release.aab` for Google Play Store)
```powershell
# 1. Stage assets & sync Android project
npm run build:android

# 2. Build production Android App Bundle (.aab)
cd android
.\gradlew.bat clean bundleRelease
cd ..
```
- **Output:** `android/app/build/outputs/bundle/release/app-release.aab` (10.5 MB)
- **Google Play Console:** Uploaded to **Production** track $\rightarrow$ Release `1.3.3 (5)` (targetSdk 36).

### Target 4: iOS Release (`.ipa` via GitHub Actions Cloud CI)
```powershell
# 1. Sync iOS web assets
npm run build:ios

# 2. Stage only release files (avoid untracked scratch scripts)
git add index.html manifest.json package.json package-lock.json sw.js `
        data/words.json js/tamilUtils.js js/uiController.js `
        tamilwordbank-v2.md words-to-be-added.md `
        scripts/build_wordbank.py scripts/promote_words.py scripts/audit_words_to_be_added.py `
        cloudflare/overlay/manifest.json cloudflare/overlay/sw.js `
        android/app/build.gradle android/variables.gradle `
        ios/App/App.xcodeproj/project.pbxproj v-1-3-3-plan.md handoff.md

# 3. Commit, tag, and push to trigger Cloud CI
git commit -m "Release v1.3.3: ஸ்ரீ keypad button, 1,714 words, multi-platform sync"
git tag ios-v1.3.3
git push origin main
git push origin ios-v1.3.3
```
- **Cloud Runner:** GitHub Actions macOS runner archives, codesigns with distribution certificate, and uploads build `1.3.3 (7)` directly to TestFlight and App Store Connect.

---

## 7. Version History & Milestone Tracker

| Version | Android Code | iOS Build | Words | Key Features & Milestones |
| :---: | :---: | :---: | :---: | :--- |
| **v1.0.0** | `1` | `1` | 1,500 | Initial PWA & mobile prototype. Basic 2-tier keypad. |
| **v1.3.0** | `2` | `2` | 1,500 | Tactile cycle buttons for Length & Complexity; safe-area insets. |
| **v1.3.1** | `2` | `2` | 1,671 | Expanded corpus to 1,671 words; 3 progressive clues; local font hosting. |
| **v1.3.2** | `3` | `6` | 1,671 | Production submission to Google Play & TestFlight. |
| **v1.3.3** | `5` | `7` | **1,714** | **Dedicated `ஸ்ரீ` (Sri) button with 6×4 matrix symmetry; promoted 43 candidate words; targetSdk 36; Cloudflare Pages build pipeline; submitted to Google Play & App Store review.** |

---

## 8. Sanity Checklist for Handoff Verification

- [x] **`ஸ்ரீ` Keypad Button**: Rendered as 24th Mei key, completes Row 4 (`க்ஷ்`, `ஜ்`, `ஸ்`, `ஷ்`, `ஹ்`, `ஸ்ரீ`).
- [x] **Word Bank Expansion**: 1,714 words in `tamilwordbank-v2.md` and compiled in `data/words.json`.
- [x] **Service Worker Cache**: Auto-bumped to `solladal-1.3.3-42e49714` in `sw.js`.
- [x] **Integration Test Suite**: 100% pass across all 1,714 words in `scripts/test_pwa_integration.py`.
- [x] **Candidate Words Leak Gate**: 0 leaks detected in `scripts/audit_words_to_be_added.py --allow-promoted`.
- [x] **WWW Staged Assets**: Runtime bundle ready in `./www/`.
- [x] **Cloudflare Public Site**: 33 files generated in `cloudflare/public/` with `solladal-web-1.3.3-cf3`.
- [x] **Android Release Bundle**: Signed `app-release.aab` built with `versionCode 5`, `compileSdkVersion 36`, `targetSdkVersion 36`, uploaded & submitted to Google Play review.
- [x] **iOS Project Synced**: Web bundle synced into `ios/App/App/public`, versions set to `1.3.3` (Build 7), submitted to App Store review.
