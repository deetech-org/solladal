# "சொல்லாடல்" (Solladal) — Tamil Word Game (v1.3.2)

## Master Handoff & Project Delivery Document

**Publisher:** `deetech.org` • **App ID:** `org.deetech.solladal` • **Platforms:** Web (PWA), Android (Play Store), iOS (App Store)


## 1. Executive Summary & Architecture

**"சொல்லாடல்" (Solladal)** is an educational, elegant, and culturally authentic Tamil word-guessing game designed for Grade 1 through Grade 5 students and Tamil learners worldwide.

The application uses a **vanilla HTML/CSS/JS PWA core** wrapped **1:1 with Capacitor** for native mobile app distribution:

- **Zero UI Rewrite:** 100% reuse of the web game engine, styles, and 1,500-word offline dictionary.

- **Asset Staging (`./www`):** `npm run prep:mobile` stages only runtime assets into `www/`, isolating build files and source markdown from mobile app bundles.

- **Android Target:** Built locally on Windows using OpenJDK 21, Android SDK (API 35/36), and Gradle.

- **iOS Target:** Built in the cloud via GitHub Actions on `macos-latest` runners (Xcode, CocoaPods, automated signing & TestFlight upload).

```
                        ┌─────────────────────────────────────────────────────────┐  
                        │         சொல்லாடல் (Solladal) Word-Game Core            │  
                        │   (1,500 Words, 2-Step Keypad, 3 Clues, Polished CSS)  │  
                        │   Vanilla HTML/CSS/JS PWA — served from repo root       │  
                        └────────────────────────────┬────────────────────────────┘  
                                                     │  npm run prep:mobile → ./www  
                                           ┌──────────┴──────────┐  
                                           │  Capacitor wraps www │  (100% code reuse)  
                                           └──────────┬──────────┘  
                           ┌────────────────────────────┴────────────────────────────┐  
                           ▼ Android (build LOCALLY on Windows)          ▼ iOS (build on GitHub Actions macOS)  
      ┌───────────────────────────────────────────┐        ┌───────────────────────────────────────────┐  
      │  npx cap sync android                     │        │  macos-latest runner + Xcode              │  
      │  Android Studio / gradlew → signed .aab   │        │  cap sync ios → pod install → xcodebuild  │  
      │  Test in local Android emulator (Pixel 8) │        │  → signed .ipa → TestFlight/App Store      │  
      │  JDK 21 + Android SDK (API 35/36)         │        │  Signing via GitHub Secrets (cert + ASC)  │  
      └───────────────────────────────────────────┘        └───────────────────────────────────────────┘
```


## 2. Pre-Flight Blockers Resolved (Phase 0)

1. **Self-Hosted Fonts & Zero-Leakage CSP:**

   - Downloaded `Noto Sans Tamil` and `Mukta Malar` (`.woff2`) into `assets/fonts/`.

   - Local `@font-face` definitions configured with `./` relative paths in `assets/fonts/fonts.css`.

   - Enforced strict Content-Security-Policy meta tag in `index.html` preventing third-party IP leakage:

   - ```
\<meta http-equiv="Content-Security-Policy"  
      content="default-src 'self'; img-src 'self' data:; style-src 'self' 'unsafe-inline'; font-src 'self'; connect-src 'self'; script-src 'self'"\>
```

   - Fully compliant with **COPPA** and **Google Play Designed for Families**.

2. **Trademark & Brand Protection:**

   - Branded cleanly as **"சொல்லாடல் (Solladal) — Tamil Word Game"** with zero usage of "Wordle" to prevent store rejections.

3. **Durable Mobile Storage:**

   - Integrated `@capacitor/preferences` inside `js/storage.js` (with `localStorage` fallback) to prevent iOS `WKWebView` storage eviction from wiping child win streaks.


## 3. Responsive Layout Architecture (`100dvh` Discipline)

The UI uses a **Zero-Scroll (`100dvh`)** layout with dynamic viewport height and safe-area insets (`env(safe-area-inset-\*)`), ensuring zero page overflow across all phone and tablet screens:

```
+-----------------------------------------------------------------------------------------+  
| TOP SECTION: Persistent Cultural Banner & Tactile Cycle Controls                        |  
| - Subsection 1: \[அன்பே இறை / Love is Divine\]   சொல்லாடல்   \[அறமே வழி / Virtue is the Path\]|  
| - Subsection 2: \[ 3 எழுத்து ▾ \] (Cycle)    \[அடுத்த சொல் ❯\]    \[ Beginner ▾ \] (Cycle)       |  
|   \* Zero OS modal pickers / dialogs on mobile; cycles directly in-place with haptics    |  
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
| - Subsection 2: [ 23 Mei Keys (Left) ]   | (Vertical Line) |   [ 13 Uyir Keys (Right) ]  |  
|   * Ergonomic button sizing (reduced 8%) preventing bottom cutoff on small screens      |  
| - Subsection 3:          [ ழ் சொல் வங்கி ]      [ ? விளையாடும் முறை ] (Centered in Middle) |  
+-----------------------------------------------------------------------------------------+
```


## 4. File Inventory & Repository Structure

```
./solladal/  
├── index.html                   \# HTML5 entry with local fonts, strict CSP, cycle controls & PWA meta  
├── manifest.json                \# Web App Manifest for mobile/desktop standalone install  
├── sw.js                        \# Service Worker caching all static & font assets (v1.3.1)  
├── package.json                 \# Node dependencies & prep:mobile staging scripts  
├── capacitor.config.json        \# Capacitor configuration (appId: org.deetech.solladal)  
├── .gitignore                   \# Ignores www/, node\_modules/, and native build caches  
├── css/  
│   └── style.css                \# Polished CSS (100dvh viewport, safe area insets, 3D tactile buttons, custom scrollbar)  
├── js/  
│   ├── app.js                   \# App coordinator, Capacitor hooks (Back button), haptics, cycle actions  
│   ├── gameEngine.js            \# Turn manager, multi-letter safe evaluator, clue triggers  
│   ├── tamilUtils.js            \# NFC grapheme tokenizer, Mei+Uyir synthesizer & haptic helper  
│   ├── wordBank.js              \# In-memory dataset manager & random selector  
│   ├── uiController.js          \# DOM renderer, 3-box preview updater, row shake/flip animator, cycle helpers  
│   ├── modals.js                \# Searchable Word Bank explorer, Help modal & Game Over dialog  
│   └── storage.js               \# Durable persistence (@capacitor/preferences + localStorage)  
├── data/  
│   └── words.json               \# 1,500 indexed Tamil words with 3 bilingual clues each  
├── assets/  
│   ├── fonts/  
│   │   ├── fonts.css            \# Local @font-face declarations (relative ./ paths)  
│   │   ├── MuktaMalar-\*.woff2   \# Mukta Malar fonts (weights 400, 600, 700, 800)  
│   │   └── NotoSansTamil-\*.woff2\# Noto Sans Tamil fonts (variable woff2)  
│   └── icons/  
│       ├── icon-192.svg         \# 192x192 maskable icon  
│       └── icon-512.svg         \# 512x512 maskable icon  
├── android/                     \# Local Android native project (compileSdkVersion 35)  
│   ├── app/  
│   │   ├── build.gradle         \# Application gradle config (namespace: org.deetech.solladal)  
│   │   └── src/main/            \# AndroidManifest.xml & native assets  
│   └── build.gradle  
├── ios/                         \# iOS native project for Cloud CI  
│   ├── App/  
│   │   ├── App/Info.plist       \# Non-exempt encryption false & portrait lock  
│   │   └── ExportOptions.plist  \# App Store distribution export configuration  
│   └── Podfile  
├── .github/  
│   └── workflows/  
│       └── ios-release.yml      \# Automated macOS cloud build & TestFlight upload workflow  
├── scripts/  
│   ├── download\_fonts.py        \# Utility to fetch and generate local woff2 font files  
│   ├── sync\_wordbank.py         \# One-click master word bank parser, validator & cache bumper  
│   ├── test\_pwa\_integration.py  \# Master test suite validating all PWA & asset components  
│   └── tamil\_utils.py           \# Python Tamil grapheme regex parser  
├── solladal-mobile-app-plan.md  \# Comprehensive Mobile Store Publishing Plan  
├── tamilwordbank.md             \# Master Markdown table of all 1,500 words  
├── PRIVACY.md                   \# Family & COPPA compliant privacy policy  
└── handoff.md                   \# This Master Project Handoff Document
```


## 5. How to Run the Android App on the Simulator / Emulator

There are **three convenient ways** to run and test the Android app on your local machine:

### Option A: One-Command CLI Run (Easiest)

Run directly from PowerShell:

```
npx cap run android --target "Pixel\_8"
```

*Capacitor will automatically stage the web bundle, sync plugins, boot the `Pixel\_8` emulator, install the debug APK, and launch the game.*


### Option B: Visual GUI via Android Studio

1. Open the Android project in Android Studio:

```
npx cap open android
```

2. Select **`Pixel\_8`** from the device dropdown at the top toolbar.

3. Click the green **Run (▶)** button (or press `Shift + F10`).

4. Android Studio will boot the emulator, compile, install, and attach the Chrome/Android webview debugger.


### Option C: Manual Terminal Boot & ADB Install

If you prefer running the emulator in a dedicated terminal window:

1. **Launch the Emulator:**

```
& "..\\androidsdk\\emulator\\emulator.exe" -avd Pixel\_8
```

2. **Build and Deploy the App (in project terminal):**

```
npm run prep:mobile  
npx cap sync android  
cd android  
.\\gradlew.bat installDebug  
& "..\\androidsdk\\platform-tools\\adb.exe" shell am start -n org.deetech.solladal/org.deetech.solladal.MainActivity
```


## 6. How to Build Release Packages

### 1. Android Release Bundle (`.aab` for Google Play)

```
\# 1. Sync latest assets  
npm run prep:mobile  
npx cap sync android  
  
\# 2. Build release bundle  
cd android  
.\\gradlew.bat bundleRelease
```

*Output:* `android/app/build/outputs/bundle/release/app-release.aab`


### 2. iOS Release Build (`.ipa` via GitHub Actions)

Since iOS compilation requires Xcode on macOS, the release pipeline runs entirely in the cloud on GitHub Actions `macos-latest`:

1. Store Apple Distribution signing certificate (`.p12`), App Store provisioning profile, and App Store Connect API Key (`.p8`) in your GitHub repository secrets:

   - `IOS\_DIST\_CERT\_P12\_BASE64`, `IOS\_DIST\_CERT\_PASSWORD`, `IOS\_KEYCHAIN\_PASSWORD`

   - `IOS\_PROVISIONING\_PROFILE\_BASE64`

   - `ASC\_KEY\_ID`, `ASC\_ISSUER\_ID`, `ASC\_API\_KEY\_P8\_BASE64`

2. Push a release tag or trigger the workflow manually from the GitHub Actions tab:

```
git tag ios-v1.0.0  
git push origin ios-v1.0.0
```

*The GitHub Actions runner executes `cap sync ios` $\\rightarrow$ `pod install` $\\rightarrow$ `xcodebuild` $\\rightarrow$ uploads directly to TestFlight / App Store Connect.*


## 7. How to Review & Sync the Tamil Word Bank

As you edit or add words to [`tamilwordbank.md`](file:///d:/pethuraj/solladal/tamilwordbank.md):

1. **Run the One-Click Sync Tool:**

```
$env:PYTHONIOENCODING="utf-8"; python scripts/sync\_wordbank.py
```

2. **Run Integration Tests:**

```
$env:PYTHONIOENCODING="utf-8"; python scripts/test\_pwa\_integration.py
```

3. **Sync with Mobile Projects:**

```
npm run build:android  
npm run build:ios
```


## 8. Web / Local Browser Play

To test the web app directly in any browser:

```
python -m http.server 8080
```

Open `http://localhost:8080` in Chrome, Safari, or Edge.

