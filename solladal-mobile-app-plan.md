# சொல்லாடல் (Solladal) — Mobile App Publishing Plan

### Complete End-to-End Store Release Guide for Apple App Store (iOS) & Google Play Store (Android)

**Publisher / Organization:** `deetech.org` • **Bundle Identifier:** `org.deetech.solladal`

## 1. Executive Summary & Chosen Architecture

**சொல்லாடல் (Solladal)** is an educational, authentic Tamil word-guessing game for Grade 1–5 students and Tamil learners worldwide. It is a finished **vanilla HTML/CSS/JS PWA** (no build step, no framework). The chosen strategy wraps that existing web app **1:1 with Capacitor** — zero UI rewrite — and splits the build environment to match this project's hardware reality:

- **Android** is built **locally on the Windows dev machine** (Node, JDK, Android SDK + emulator already installed).

- **iOS** is built on a **GitHub Actions `macos-latest` runner** (a cloud Mac with Xcode), since iOS cannot be compiled on Windows.

```
                        ┌─────────────────────────────────────────────────────────┐    
                        │         சொல்லாடல் (Solladal) Word-Game Core            │    
                        │   (1,650+ Words, 2-Step Keypad, 3 Clues, Polished CSS) │    
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
     │  Test in local Android emulator           │        │  → signed .ipa → TestFlight/App Store      │    
     │  JDK 21 + Android SDK (API 35/36)         │        │  Signing via GitHub Secrets (cert + ASC key)│    
     └───────────────────────────────────────────┘        └───────────────────────────────────────────┘
```

### Why this architecture

| Dimension | Decision | Rationale |
| - | - | - |
| **Wrapper** | **Capacitor** (not Expo/RN) | 100% reuse of existing `index.html`, `js/`, `css/`, `data/words.json`; no React Native rewrite. Est. **1–2 days** to store-ready vs. 1–2 weeks for a port. |
| **Android build** | **Local (Windows)** | Toolchain already installed on this machine; instant iteration in the local emulator. |
| **iOS build** | **GitHub Actions `macos-latest`** | iOS requires macOS + Xcode, impossible on Windows. GH Actions macOS runners are free for public repos / metered-but-cheap for private, and need only one `xcodebuild` workflow. |
| **OTA updates** | **Deferred** (native store releases for v1.0) | App is 100% offline; OTA adds little. If needed later, use **Capgo** or Capacitor Live Updates (note: `expo-updates`/`eas update` are React-Native-only and do **not** apply to Capacitor). |
| **Native APIs** | `@capacitor/\\\*` plugins | Haptics, Share, StatusBar, SplashScreen, Preferences, App — all covered without RN. |


> **On existing Expo/EAS access:** the Expo org is reusable for billing/identity, but standard `eas build` and `eas update` are React-Native-shaped and do not fit a Capacitor app. GitHub Actions is the cleaner cloud-Mac path for this project, so this plan does **not** depend on EAS.

## 1.1. Critical Pre-Flight Fixes (Do These First — They Are Release Blockers)

These three items must be resolved **before** the first native build. Each one, left unfixed, either breaks a core marketing claim or risks store rejection.

### 🔴 Blocker 1 — Self-host the fonts (offline + privacy correctness)

`index.html` currently pulls **Noto Sans Tamil** and **Mukta Malar** from `fonts.googleapis.com` / `fonts.gstatic.com` at runtime. This silently breaks two of this app's headline promises:

- **"100% offline"** is false — with no network the fonts fail and the carefully-tuned Tamil typography falls back to system glyphs (diacritic clipping, inconsistent rendering).

- **"Collects nothing / no data shared / COPPA-safe"** is false — every launch sends the user's IP address to Google, a third party. Under Google Play's **Designed for Families** policy this is a reportable data transfer and a likely rejection.

**Fix:** download the two font families as `woff2`, place them in `assets/fonts/`, declare them with local `@font-face` rules, remove the three `\\\<link\\\>` tags from `index.html`, and add the font files to both `sw.js` `ASSETS\\\_TO\\\_CACHE` and the native bundle. Then add a Content-Security-Policy meta tag that forbids any external origin, so the "zero network requests" claim is provably true:

```
\\\<meta http-equiv="Content-Security-Policy"    
      content="default-src 'self'; img-src 'self' data:; style-src 'self' 'unsafe-inline'; font-src 'self'; connect-src 'self'; script-src 'self'"\\\>
```

### 🔴 Blocker 2 — Avoid any sensitive information in store-facing names

This plan's listings below have been revised to lead with **"Solladal — Tamil Word Game"** . Keep "Solladal" and "Tamil word game/puzzle" as the brand.

### 🟠 Blocker 3 — Durable stats on iOS (`localStorage` caveat)

`js/storage.js` persists streaks and stats via `localStorage`. Inside iOS `WKWebView`, WebKit may **evict** localStorage under storage pressure, silently wiping a child's streak. Migrate persistence to **`@capacitor/preferences`**, keeping localStorage only as the web fallback. Wrap it behind the existing `StorageManager` so the game code is untouched.

## 2. Global App Metadata & Identifiers

### Identifiers (Aligned with `deetech.org`)

- **App Name (Tamil):** `சொல்லாடல்`

- **App Name (English):** `Solladal - Tamil Word Game`

- **Bundle ID (iOS):** `org.deetech.solladal`

- **Package Name (Android):** `org.deetech.solladal`

- **Marketing Version:** `1.0.0`

- **Initial Build Number:** `1` (`versionCode: 1` / `buildNumber: "1"`)

- **Primary Category:** Games / Word

- **Secondary Category:** Education / Puzzle

- **Content Rating:** Everyone (PEGI 3, ESRB E, iOS 4+) — Family & COPPA Compliant

## 3. Store Listings & ASO Metadata

### A. Apple App Store (iOS)

| Attribute | Specification | Content |
| - | :-: | - |
| **App Name** | Max 30 chars | `சொல்லாடல் - Tamil Word Game` |
| **Subtitle** | Max 30 chars | `தமிழ் சொல் விளையாட்டு & புதிர்` |
| **Promotional Text** | Max 170 chars | `1,650+ தமிழ் சொற்கள், 3 கல்விசார் குறிப்புகள் மற்றும் புதுமையான 2-வழி தமிழ் விசைப்பலகையுடன் தமிழ் சொல் புதிர் விளையாட்டை விளையாடுங்கள்!` |
| **Keywords** | Max 100 chars | `tamil,solladal,சொல்லாடல்,tamilwords,learntamil,wordgame,thirukkural,puzzle,kids,education,vocabulary` |


> **ASO tip:** Apple counts spaces in the 100-char keyword field — use commas only, no spaces (as above), to fit more terms. Do not repeat words already in the App Name/Subtitle; Apple indexes those separately.

### B. Google Play Store (Android)

| Attribute | Specification | Content |
| - | :-: | - |
| **App Title** | Max 30 chars | `சொல்லாடல்: Tamil Word Game` |
| **Short Description** | Max 80 chars | `1-5 எழுத்து தமிழ் சொல் புதிர் விளையாட்டு. 1,650+ சொற்கள் & 3 குறிப்புகள்!` |
| **Full Description** | Max 4000 chars | *(See Section 3.C below)* |
| **Target Audience** | Family Policy | Ages 6-8, 9-12, and 13+ (Designed for Families) |
| **Data Safety** | Form | **No data collected, No data shared, No tracking, No ads** |


### C. Bilingual Full Store Description

```
சொல்லாடல் (Solladal) — தமிழ் மொழி ஆர்வலர்களுக்கும், பள்ளி மாணவர்களுக்கும் ஏற்ற முழுமையான தமிழ் சொல் புதிர் விளையாட்டு!    
    
Solladal is an elegant, authentic, and educational Tamil Word Guessing Game crafted for Grade 1 through Grade 5 learners, families, and Tamil enthusiasts worldwide.    
    
🌟 சிறப்பு அம்சங்கள் (Key Features):    
    
• 1,650+ தரப்படுத்தப்பட்ட தமிழ் சொற்கள் (1,650+ Curated Words):    
  - 1-எழுத்து ஓரெழுத்து ஒருமொழி    
  - 2-எழுத்து சொற்கள்    
  - 3-எழுத்து சொற்கள்    
  - 4-எழுத்து சொற்கள்    
  - 5-எழுத்து சொற்கள்     
    
• புதுமையான 2-படி தமிழ் விசைப்பலகை (Innovative 2-Step Keypad):    
  மெய் எழுத்து + உயிர் எழுத்து = உயிர்மெய் எழுத்து (எ.கா: \\\[க்\\\] + \\\[ஆ\\\] = \\\[கா\\\]). தமிழ் எழுத்துக்களை எளிதாக உருவாக்கலாம்.    
    
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

## 4. Privacy Policy & Compliance (COPPA & Family Policy)

Create a dedicated `PRIVACY.md` for Solladal:

```
\\\# Privacy Policy — சொல்லாடல் (Solladal)    
    
\\\*\\\*App:\\\*\\\* சொல்லாடல் (Solladal)      
\\\*\\\*Owner:\\\*\\\* deetech.org      
\\\*\\\*Effective Date:\\\*\\\* 2026-08-22      
    
\\\#\\\# Summary    
\\\*\\\*சொல்லாடல் (Solladal) collects nothing.\\\*\\\* It has no accounts, no servers, no analytics, no advertising SDKs, and makes zero network requests. The entire word bank and gameplay logic run 100% locally on your device.    
    
\\\> ⚠️ This "zero network requests" statement is only true after \\\*\\\*Blocker 1\\\*\\\* (self-hosting the fonts) is completed. Do not publish this policy or submit the Play "Data Safety" / App Store "Privacy" forms until the runtime Google Fonts fetch has been removed and the CSP is in place — otherwise the app leaks the user's IP to Google on every launch and the statement is false.    
    
\\\#\\\# Data Storage    
- Game statistics (win streaks, games played, guess distribution histogram) are stored \\\*\\\*strictly on your local device\\\*\\\* using LocalStorage / OS sandbox storage.    
- No personal information, device identifiers, or usage logs ever leave your device.    
    
\\\#\\\# Children's Privacy (COPPA Compliance)    
Because the app collects no data whatsoever from any user, it collects no data from children under 13.    
    
\\\#\\\# Contact    
Questions regarding this policy: deetech.org
```

## 5. Visual Asset Specifications

Icons and screenshots are under ./solladal/assets/icons and ./solladal/assets/screenshots.

## 6. Implementation Guide: Capacitor (Android — Local Windows Build)

### Step 0: Build Environment Prerequisites (verified on this machine)

| Dependency | Required | Status on dev machine | Action |
| - | - | - | - |
| Node.js + npm | ≥ 20 | ✅ Node 24+ / npm 11+ | — |
| JDK | 21 | ✅ OpenJDK 21 (Android Studio JBR) | `JAVA_HOME` set |
| Android SDK | API 35+ | ✅ `ANDROID_HOME` configured; **API 36 / 35 installed** | Play target API 35 |
| Build-tools | recent | ✅ 36.1.0, 37.0.0 | — |
| Platform-tools (adb) | any | ✅ 1.0.41 | — |
| Android emulator + image | — | ✅ installed | — |
| Gradle | via wrapper | ✅ uses `gradlew` (auto-downloaded) | no standalone install needed |
| `package.json` | — | ❌ none yet | run `npm init -y` first |
| Release keystore | for signing | ❌ not created | generate once (Step 4) |


```
\\\# Recommended env tidy-ups (PowerShell) — not blockers, but avoid tool warnings:    
setx ANDROID\\\_SDK\\\_ROOT "\\\<..\\\\androidsdk\\\>"     \\\# some tools read this instead of ANDROID\\\_HOME    
\\\# Add Android platform 35 (Google Play's current target for new apps):    
& "\\\<..\\\\androidsdk\\\\cmdline-tools\\\\latest\\\\bin\\\\sdkmanager.bat\\\>" "platforms;android-35"
```

> **iOS build environment is intentionally NOT on this machine** — it lives entirely in GitHub Actions (Section 7). Nothing iOS-related needs to be installed on Windows.

### Step 1: Package & Plugin Setup

```
\\\# 1. Install Capacitor core dependencies    
npm install @capacitor/core @capacitor/cli @capacitor/ios @capacitor/android    
    
\\\# 2. Install Native Plugins (Haptics, Share, StatusBar, SplashScreen, App, Preferences)    
npm install @capacitor/haptics @capacitor/share @capacitor/status-bar @capacitor/splash-screen @capacitor/app @capacitor/preferences    
    
\\\# 3. Icon/splash generator — run on demand, NOT a permanent dependency    
\\\# (keeping it installed pulls in vulnerable sharp/tar/uuid; use npx only when regenerating assets)    
\\\# npx @capacitor/assets generate    
    
\\\# 4. Initialize Capacitor (webDir is a dedicated build folder, NOT the repo root)    
npx cap init "Solladal" "org.deetech.solladal" --web-dir "www"
```

> **Why `www`, not `.`:** Capacitor copies the *entire* `webDir` into each native project. Pointing it at the repo root would bundle `.git/`, `scripts/`, the 1.2 MB `tamilwordbank.md`, and this plan into the shipped app. Add a tiny copy step that stages only the runtime assets:

```
// package.json  →  "scripts"    
"prep:mobile": "node -e \\\\"const \\\{cpSync,rmSync,mkdirSync\\\}=require('fs');rmSync('www',\\\{recursive:true,force:true\\\});mkdirSync('www');for(const p of \\\['index.html','manifest.json','css','js','data','assets'\\\]) cpSync(p,'www/'+p,\\\{recursive:true\\\});\\\\""
```

Run `npm run prep:mobile && npx cap sync` before every build. (The PWA still serves from the repo root for the web target.) Generate icons/splash from a source image with `npx capacitor-assets generate`.

### Step 2: `capacitor.config.json` Configuration

```
\\\{    
  "appId": "org.deetech.solladal",    
  "appName": "சொல்லாடல்",    
  "webDir": "www",    
  "backgroundColor": "\\\#FAF7F2",    
  "ios": \\\{    
    "contentInset": "always",    
    "preferredContentMode": "mobile",    
    "scheme": "Solladal"    
  \\\},    
  "android": \\\{    
    "backgroundColor": "\\\#FAF7F2",    
    "allowMixedContent": false,    
    "captureInput": true    
  \\\},    
  "plugins": \\\{    
    "SplashScreen": \\\{    
      "launchShowDuration": 1500,    
      "launchAutoHide": true,    
      "backgroundColor": "\\\#D97706",    
      "androidSplashResourceName": "splash",    
      "showSpinner": false,    
      "splashFullScreen": true,    
      "splashImmersive": true    
    \\\},    
    "StatusBar": \\\{    
      "style": "DARK",    
      "backgroundColor": "\\\#D97706"    
    \\\}    
  \\\}    
\\\}
```

### Step 3: Native Enhancements in Code

1. **Safe Area CSS (`css/style.css`)**:

```
body \\\{    
  padding-top: env(safe-area-inset-top);    
  padding-bottom: env(safe-area-inset-bottom);    
  padding-left: env(safe-area-inset-left);    
  padding-right: env(safe-area-inset-right);    
  user-select: none;    
  -webkit-user-select: none;    
  -webkit-touch-callout: none;    
\\\}
```

1. **Native Haptic Feedback (`js/gameEngine.js` & `js/app.js`)**:

> Note: with no bundler, `ImpactStyle` / `NotificationType` are **not** on `window.Capacitor.Plugins` — those enums are exports of the `@capacitor/haptics` module. Their values are plain strings, so pass the string literals directly. Wrap every call in `try/catch`; haptics rejects on unsupported devices.

```
async function playHaptic(style = 'light') \\\{    
  try \\\{    
    if (window.Capacitor?.isPluginAvailable?.('Haptics')) \\\{    
      const \\\{ Haptics \\\} = window.Capacitor.Plugins;    
      if (style === 'light')       await Haptics.impact(\\\{ style: 'LIGHT' \\\});    
      else if (style === 'medium') await Haptics.impact(\\\{ style: 'MEDIUM' \\\});    
      else if (style === 'success') await Haptics.notification(\\\{ type: 'SUCCESS' \\\});    
      else if (style === 'error')   await Haptics.notification(\\\{ type: 'ERROR' \\\});    
      return;    
    \\\}    
  \\\} catch (e) \\\{ /\\\* fall through to web vibrate \\\*/ \\\}    
  if (navigator.vibrate) navigator.vibrate(style === 'light' ? 15 : 30);    
\\\}
```

1. **Android hardware back button (`js/app.js`)** — without this, pressing Back mid-game exits the app straight to the home screen (a common review complaint and a poor experience for kids):

```
if (window.Capacitor?.isPluginAvailable?.('App')) \\\{    
  const \\\{ App \\\} = window.Capacitor.Plugins;    
  App.addListener('backButton', (\\\{ canGoBack \\\}) =\\\> \\\{    
    if (isModalOpen()) closeModal();          // close a modal first    
    else App.exitApp();                        // only exit from the home screen    
  \\\});    
\\\}
```

1. **Durable stats (`js/storage.js`)** — swap the localStorage read/write for `@capacitor/preferences` when running natively, keeping localStorage as the web fallback (see Blocker 3):

```
const P = window.Capacitor?.Plugins?.Preferences;    
async function saveStats(stats) \\\{    
  const json = JSON.stringify(stats);    
  if (P) await P.set(\\\{ key: 'solladal\\\_stats', value: json \\\});    
  else localStorage.setItem('solladal\\\_stats', json);    
\\\}
```

1. **Native Share Dialog (`js/uiController.js`)**:

```
async function shareScore(scoreText) \\\{    
  if (window.Capacitor && window.Capacitor.isPluginAvailable('Share')) \\\{    
    const \\\{ Share \\\} = window.Capacitor.Plugins;    
    await Share.share(\\\{    
      title: 'சொல்லாடல் (Solladal)',    
      text: scoreText,    
      dialogTitle: 'Share your Solladal score'    
    \\\});    
  \\\} else if (navigator.share) \\\{    
    await navigator.share(\\\{ text: scoreText \\\});    
  \\\} else \\\{    
    await navigator.clipboard.writeText(scoreText);    
    showToast("முடிவுகள் நகலெடுக்கப்பட்டன! (Copied)");    
  \\\}    
\\\}
```

### Step 4: How to Run the Android App on the Simulator / Emulator

The development machine is equipped with the **`Pixel\\\_8`** Android Virtual Device (AVD). You can launch and test the Android application using any of the following 3 options:

#### Option A: One-Command CLI Run (Fastest & Easiest)

Run directly from the root project directory in PowerShell:

```
npx cap run android --target "Pixel\\\_8"
```

*This command automatically executes `npm run prep:mobile`, syncs Capacitor plugins, boots the `Pixel\\\_8` emulator (if not already running), compiles the debug build, installs the APK, and opens the app.*

#### Option B: Visual GUI via Android Studio

1. Open the Android project in Android Studio:

```
npx cap open android
```

1. In the top toolbar device selector, pick **`Pixel\\\_8`**.

2. Click the green **Run (▶)** button (or press `Shift + F10`).

3. Android Studio compiles, boots the emulator, and attaches live Webview & Logcat debugging.

#### Option C: Manual Emulator Boot & Gradle/ADB Install

If you prefer running the emulator in a dedicated terminal window:

1. **Launch the Emulator:**

```
& "..\\\\androidsdk\\\\emulator\\\\emulator.exe" -avd Pixel\\\_8
```

1. **Build and Deploy the App (in project terminal):**

```
npm run prep:mobile    
npx cap sync android    
cd android    
.\\\\gradlew.bat installDebug    
& "..\\\\androidsdk\\\\platform-tools\\\\adb.exe" shell am start -n org.deetech.solladal/org.deetech.solladal.MainActivity
```

## 7. Implementation Guide: iOS via GitHub Actions (`macos-latest`)

Since iOS cannot be built on Windows, the iOS `.ipa` is produced by a cloud Mac in CI. Capacitor generates a standard Xcode project (`ios/App/App.xcworkspace`, scheme `App`) with CocoaPods — a `macos-latest` runner has Xcode + CocoaPods preinstalled, so the workflow only has to sync, install pods, sign, archive, and upload.

### Step 1: One-time prerequisites (done once on a Mac or via Apple Developer portal)

You cannot generate iOS signing material on Windows. Do this once through the Apple Developer web portal (and a Mac or an online CSR tool for the certificate), then store everything as **GitHub repository secrets** — CI never needs a Mac of your own afterward.

| Secret name | What it is | How to obtain |
| - | - | - |
| `IOS\\\_DIST\\\_CERT\\\_P12\\\_BASE64` | Apple **Distribution** certificate + private key, exported as `.p12`, then base64-encoded | Apple Developer → Certificates → Apple Distribution. `base64 -i cert.p12` |
| `IOS\\\_DIST\\\_CERT\\\_PASSWORD` | Password set when exporting the `.p12` | you choose it at export |
| `IOS\\\_PROVISIONING\\\_PROFILE\\\_BASE64` | **App Store** provisioning profile (`.mobileprovision`) for `org.deetech.solladal`, base64-encoded | Apple Developer → Profiles → App Store distribution |
| `IOS\\\_KEYCHAIN\\\_PASSWORD` | Any random string used to create a temporary CI keychain | you choose it |
| `ASC\\\_KEY\\\_ID` | App Store Connect API key ID | App Store Connect → Users and Access → Integrations → App Store Connect API |
| `ASC\\\_ISSUER\\\_ID` | App Store Connect API issuer ID | same page |
| `ASC\\\_API\\\_KEY\\\_P8\\\_BASE64` | The `.p8` API key file, base64-encoded (used for TestFlight/App Store upload) | download once at key creation; `base64 -i AuthKey\\\_XXXX.p8` |


> The App ID `org.deetech.solladal` must exist in the Apple Developer portal before creating the provisioning profile.

### Step 2: `ios/App/ExportOptions.plist` (commit this into the repo)

```
\\\<?xml version="1.0" encoding="UTF-8"?\\\>    
\\\<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd"\\\>    
\\\<plist version="1.0"\\\>    
\\\<dict\\\>    
  \\\<key\\\>method\\\</key\\\>            \\\<string\\\>app-store\\\</string\\\>    
  \\\<key\\\>teamID\\\</key\\\>            \\\<string\\\>YOUR\\\_APPLE\\\_TEAM\\\_ID\\\</string\\\>    
  \\\<key\\\>uploadSymbols\\\</key\\\>     \\\<true/\\\>    
  \\\<key\\\>signingStyle\\\</key\\\>      \\\<string\\\>manual\\\</string\\\>    
  \\\<key\\\>provisioningProfiles\\\</key\\\>    
  \\\<dict\\\>    
    \\\<key\\\>org.deetech.solladal\\\</key\\\>    
    \\\<string\\\>NAME\\\_OF\\\_YOUR\\\_APPSTORE\\\_PROFILE\\\</string\\\>    
  \\\</dict\\\>    
\\\</dict\\\>    
\\\</plist\\\>
```

### Step 3: `.github/workflows/ios-release.yml`

```
name: iOS Release (Capacitor)    
    
on:    
  workflow\\\_dispatch:        \\\# manual trigger from the Actions tab    
  push:    
    tags: \\\[ 'ios-v\\\*' \\\]      \\\# or auto-run when you push a tag like ios-v1.0.0    
    
jobs:    
  build-ios:    
    runs-on: macos-latest   \\\# cloud Mac with Xcode + CocoaPods    
    timeout-minutes: 40    
    steps:    
      - uses: actions/checkout@v4    
    
      - uses: actions/setup-node@v4    
        with:    
          node-version: 20    
    
      \\\# Install JS deps + stage the web assets into ./www, then sync the iOS project    
      - name: Build web bundle & sync Capacitor iOS    
        run: |    
          npm ci    
          npm run prep:mobile          \\\# copies index.html, css, js, data, assets → ./www    
          npx cap sync ios    
    
      - name: Install CocoaPods    
        run: |    
          cd ios/App    
          pod install    
    
      \\\# Import the distribution certificate into a temporary keychain    
      - name: Import signing certificate    
        env:    
          CERT\\\_B64:   $\\\{\\\{ secrets.IOS\\\_DIST\\\_CERT\\\_P12\\\_BASE64 \\\}\\\}    
          CERT\\\_PW:    $\\\{\\\{ secrets.IOS\\\_DIST\\\_CERT\\\_PASSWORD \\\}\\\}    
          KC\\\_PW:      $\\\{\\\{ secrets.IOS\\\_KEYCHAIN\\\_PASSWORD \\\}\\\}    
        run: |    
          echo "$CERT\\\_B64" | base64 --decode \\\> cert.p12    
          security create-keychain -p "$KC\\\_PW" build.keychain    
          security default-keychain -s build.keychain    
          security unlock-keychain -p "$KC\\\_PW" build.keychain    
          security import cert.p12 -k build.keychain -P "$CERT\\\_PW" -T /usr/bin/codesign    
          security set-key-partition-list -S apple-tool:,apple: -s -k "$KC\\\_PW" build.keychain    
    
      - name: Install provisioning profile    
        env:    
          PROFILE\\\_B64: $\\\{\\\{ secrets.IOS\\\_PROVISIONING\\\_PROFILE\\\_BASE64 \\\}\\\}    
        run: |    
          mkdir -p ~/Library/MobileDevice/Provisioning\\\\ Profiles    
          echo "$PROFILE\\\_B64" | base64 --decode \\\> ~/Library/MobileDevice/Provisioning\\\\ Profiles/profile.mobileprovision    
    
      - name: Archive    
        run: |    
          cd ios/App    
          xcodebuild -workspace App.xcworkspace \\\\    
            -scheme App \\\\    
            -configuration Release \\\\    
            -archivePath $RUNNER\\\_TEMP/App.xcarchive \\\\    
            -destination 'generic/platform=iOS' \\\\    
            clean archive CODE\\\_SIGNING\\\_ALLOWED=YES    
    
      - name: Export .ipa    
        run: |    
          cd ios/App    
          xcodebuild -exportArchive \\\\    
            -archivePath $RUNNER\\\_TEMP/App.xcarchive \\\\    
            -exportOptionsPlist ExportOptions.plist \\\\    
            -exportPath $RUNNER\\\_TEMP/export    
    
      \\\# Upload to TestFlight / App Store Connect using the ASC API key (no Apple ID password)    
      - name: Upload to App Store Connect    
        env:    
          ASC\\\_KEY\\\_ID:    $\\\{\\\{ secrets.ASC\\\_KEY\\\_ID \\\}\\\}    
          ASC\\\_ISSUER\\\_ID: $\\\{\\\{ secrets.ASC\\\_ISSUER\\\_ID \\\}\\\}    
          ASC\\\_KEY\\\_B64:   $\\\{\\\{ secrets.ASC\\\_API\\\_KEY\\\_P8\\\_BASE64 \\\}\\\}    
        run: |    
          mkdir -p ~/private\\\_keys    
          echo "$ASC\\\_KEY\\\_B64" | base64 --decode \\\> ~/private\\\_keys/AuthKey\\\_$ASC\\\_KEY\\\_ID.p8    
          xcrun altool --upload-app -f "$RUNNER\\\_TEMP/export/App.ipa" -t ios \\\\    
            --apiKey "$ASC\\\_KEY\\\_ID" --apiIssuer "$ASC\\\_ISSUER\\\_ID"    
    
      - name: Upload .ipa as build artifact    
        uses: actions/upload-artifact@v4    
        with:    
          name: solladal-ios-ipa    
          path: $\\\{\\\{ runner.temp \\\}\\\}/export/App.ipa
```

> **Notes**

> - This workflow requires `package.json` with the `prep:mobile` script (Section 6, Step 1) and a committed `ios/` project (`npx cap add ios` — run once, then commit; it can be run on the Mac runner too, but committing it keeps CI deterministic).

> - `macos-latest` minutes are **free for public repositories**. For private repos, macOS minutes bill at **10× the Linux rate** — a ~15-minute iOS build ≈ 150 min of quota; the 2,000-min free tier ≈ ~13 builds/month. Trigger on tags/manual dispatch (as above), not every push, to conserve minutes.

> - `xcrun altool` still works; Apple's newer `notarytool`/Transporter are alternatives. For TestFlight-only distribution you can stop after the export step and use `apple-actions/upload-testflight-build` instead.

> - Bump the build number each upload (App Store Connect rejects duplicates). Set `CURRENT\\\_PROJECT\\\_VERSION` via `agvtool new-version -all $GITHUB\\\_RUN\\\_NUMBER` before archiving, or manage it in Xcode.

### Step 4 (optional): Android release build in CI too

Android is built locally on Windows for v1.0, but the same repo can add a Linux CI job later (`ubuntu-latest`, no 10× multiplier) running `npm ci && npm run prep:mobile && npx cap sync android && cd android && ./gradlew bundleRelease` with the keystore supplied via secrets. Keep it separate from the macOS job so Android builds stay cheap.

## 8. Store Submission & Review Checklists

> Checkboxes are unchecked because nothing is done yet — tick them as you complete each item. The three pre-flight blockers (§1.1) gate everything below.

### Pre-flight (blockers — must clear first)

- [x] 

- **Fonts self-hosted** and runtime Google Fonts `\\\<link\\\>`s removed; CSP added (Blocker 1).

- [x] 

- **No "sensitive information"** in app name, subtitle, keywords, or screenshots (Blocker 2).

- [x] 

- **Stats persistence** migrated to native storage via `@capacitor/preferences` (Blocker 3).

- [x] 

- `python scripts/sync\\\_wordbank.py` run clean; `data/words.json` current and bundled.

### Apple App Store Connect Checklist

- [x] 

- **Account:** Apple Developer Program (`deetech.org`).

- [x] 

- **App ID:** `org.deetech.solladal` with no special entitlements needed.

- [ ] 

- **Guideline 4.2 (Minimum Functionality):** Full offline capability with 1,650+ words, rich 3-level clues, native haptic feedback, 2-step keypad synthesizer.

- [ ] 

- **Guideline 4.3 (Spam/duplicates):** Word games get scrutiny — lead the listing with the educational Tamil-literacy angle (Grades 1–5, Thirukkural/Aathichoodi clues, grapheme keypad) to show original value.

- [ ] 

- **Guideline 5.1.1 (Privacy):** Privacy "Nutrition Label" marked "Data Not Collected"; a public Privacy URL is required even when nothing is collected.

- [ ] 

- **Kids Category (optional):** If listing under Kids, no third-party analytics/ads are allowed and a privacy policy is mandatory — this app already qualifies.

- [x] 

- **Encryption:** `ITSAppUsesNonExemptEncryption` set to `false`.

- [ ] 

- **Signing material in GitHub Secrets:** distribution cert (`.p12`), App Store provisioning profile, and App Store Connect API key (`.p8`) added as repo secrets (§7 Step 1). No local Mac required.

- [ ] 

- **TestFlight:** `.ipa` produced by the `macos-latest` GitHub Actions workflow and uploaded to App Store Connect → complete internal beta testing.

### Google Play Console Checklist

- [x] 

- **Account:** Google Play Developer Account (`deetech.org`).

- [x] 

- **Package:** `org.deetech.solladal`.

- [x] 

- **Target API Level:** meet Google's current minimum for new apps (Android 15 / API 35 configured).

- [ ] 

- **App Bundle:** Signed `.aab`; enroll in **Play App Signing** (Google holds the upload/signing keys).

- [ ] 

- **Families Policy:** "Designed for Families" requires the Data Safety form to show no data leaves the device — this is why Blocker 1 is mandatory before opting in.

- [ ] 

- **Data Safety:** Form submitted stating "No data collected, no data shared" (accurate only post-Blocker 1).

- [ ] 

- **Content rating (IARC) questionnaire** completed → expect "Everyone / PEGI 3".

- [ ] 

- **Internal / Closed Testing:** New personal developer accounts must run **closed testing with ≥12 testers for 14 days** before production — budget for this in the timeline.

## 9. Launch Roadmap & Verification Plan

> Dates are illustrative. The critical-path constraint is **Google Play closed testing**: a new personal developer account must run closed testing with ≥12 opted-in testers for 14 continuous days before it can promote to production. On an established org account this requirement is relaxed. Plan the real launch date around whichever store gates you longest.

```
gantt    
    title சொல்லாடல் Mobile App Release Schedule    
    dateFormat  YYYY-MM-DD    
    section Phase 0: Pre-Flight Blockers    
    Self-host fonts + CSP (Blocker 1)      :2026-08-23, 1d    
    Remove "ensitive information" (Blocker 2)     :2026-08-23, 1d    
    Native stats storage (Blocker 3)       :2026-08-24, 1d    
    section Phase 1: Native Wrapper Setup    
    Capacitor init + www staging           :2026-08-25, 1d    
    Haptics, back-button, safe area        :2026-08-26, 1d    
    section Phase 2: Assets & Store Listings    
    Icons, adaptive icons, splash          :2026-08-27, 1d    
    Screenshots & feature graphic          :2026-08-28, 1d    
    Store listing copy (bilingual)         :2026-08-28, 1d    
    section Phase 3: Android Build & Track    
    Release keystore / Play App Signing    :2026-08-29, 1d    
    Play closed testing (≥12, 14 days)     :crit, 2026-08-30, 14d    
    Play production submission             :2026-09-13, 2d    
    section Phase 4: iOS Build & Track (GitHub Actions)    
    Apple certs/profile + GitHub Secrets   :2026-08-29, 1d    
    GitHub Actions macOS build → TestFlight :2026-08-30, 1d    
    TestFlight beta feedback               :2026-08-31, 3d    
    App Store review submission            :2026-09-03, 3d    
    section Phase 5: Live Worldwide Release    
    Both stores live                       :milestone, 2026-09-15, 0d
```

## 10. Verification & Test Commands

```
\\\# 1. Sync & Validate Word Bank before Mobile Build    
$env:PYTHONIOENCODING="utf-8"; python scripts/sync\\\_wordbank.py    
    
\\\# 2. Run PWA Integration Test Suite    
python scripts/test\\\_pwa\\\_integration.py    
    
\\\# 3. Android — build & run LOCALLY on Windows (stage www first — see §6 Step 1)    
npm run prep:mobile        \\\# copy runtime assets into ./www    
npx cap sync android    
npx cap open android       \\\# Opens Android Studio → run on the local emulator    
\\\# ...or headless release bundle:    
cd android; ./gradlew bundleRelease   \\\# produces app/build/outputs/bundle/release/\\\*.aab    
    
\\\# 4. iOS — build in the cloud (no local Mac). Trigger the GitHub Actions workflow:    
git tag ios-v1.0.0 && git push origin ios-v1.0.0     \\\# or run it manually from the Actions tab    
\\\# The macos-latest runner does cap sync ios → pod install → xcodebuild → upload to App Store Connect.
```

## 11. Phased Technical Implementation Plan

### Phase 0: Pre-Flight Blockers (Privacy, Offline Fonts & Trademarks)

1. **Self-Host Fonts & Strict Content Security Policy:**

   - Create directory `assets/fonts/`.

   - Download `NotoSansTamil` (weights 400, 500, 600, 700, 800) and `MuktaMalar` (weights 400, 600, 700, 800) in `.woff2` format.

   - Update `css/style.css` with `@font-face` rules referencing local `assets/fonts/\\\*.woff2`.

   - Update `index.html`:

     - Remove external Google Fonts preconnect/stylesheet `\\\<link\\\>` tags.

     - Insert strict Content-Security-Policy:


\<meta http-equiv="Content-Security-Policy"  
content="default-src 'self'; img-src 'self' data:; style-src 'self' 'unsafe-inline'; font-src 'self'; connect-src 'self'; script-src 'self'"\>

```
  
   - Update \`sw.js\`:  
  
     - Add local font files to \`ASSETS\\\_TO\\\_CACHE\`.  
  
     - Bump cache version to \`solladal-v1.3.0\`.  
  
2. \*\*Trademark & Branding Audit:\*\*  
  
   - Ensure game title and descriptions strictly use "சொல்லாடல் (Solladal) — Tamil Word Game" and sensitive information across \`index.html\`, \`manifest.json\`, \`PRIVACY.md\`, and metadata.  
  
3. \*\*Durable Stats & Settings Storage:\*\*  
  
   - Update \`js/storage.js\` to integrate \`@capacitor/preferences\` for native iOS/Android persistence with synchronous/localStorage fallback for web mode.  
  
\#\#\# Phase 1: Capacitor Integration & Native Plugins  
  
1. \*\*Package Configuration (\`package.json\`):\*\*  
  
   - Create \`package.json\` with dependencies:  
  
     - \`@capacitor/core\`, \`@capacitor/cli\`, \`@capacitor/android\`, \`@capacitor/ios\`  
  
     - \`@capacitor/haptics\`, \`@capacitor/share\`, \`@capacitor/status-bar\`, \`@capacitor/splash-screen\`, \`@capacitor/app\`, \`@capacitor/preferences\`  
  
     - Icon/splash generation: run \`npx @capacitor/assets generate\` on demand — do **not** keep it as an installed dependency (it pulls in vulnerable \`sharp\`/\`tar\`/\`uuid\` transitively)  
  
   - Add build scripts:  
  
     - \`"prep:mobile"\`: Node script to clean \`www/\` and stage runtime files (\`index.html\`, \`manifest.json\`, \`css/\`, \`js/\`, \`data/\`, \`assets/\`).  
  
     - \`"build:android"\`: \`npm run prep:mobile && npx cap sync android\`  
  
     - \`"build:ios"\`: \`npm run prep:mobile && npx cap sync ios\`  
  
2. \*\*Capacitor Configuration (\`capacitor.config.json\`):\*\*  
  
   - Configure \`appId\`: \`org.deetech.solladal\`  
  
   - \`appName\`: \`சொல்லாடல்\`  
  
   - \`webDir\`: \`www\`  
  
   - \`backgroundColor\`: \`\\\#FAF7F2\`  
  
   - Configure SplashScreen & StatusBar plugin properties.  
  
3. \*\*Native UI & Interaction Enhancements:\*\*  
  
   - \*\*Safe Area Insets & Touch Styling\*\* (\`css/style.css\`):  
  
     - Add \`env(safe-area-inset-top)\`, \`env(safe-area-inset-bottom)\`, \`env(safe-area-inset-left)\`, \`env(safe-area-inset-right)\`.  
  
     - Add \`-webkit-touch-callout: none\` and \`user-select: none\`.  
  
   - \*\*Haptics Integration\*\* (\`js/tamilUtils.js\` or \`js/gameEngine.js\`):  
  
     - Add \`playHaptic(style)\` supporting \`'light'\`, \`'medium'\`, \`'success'\`, \`'error'\` via \`@capacitor/haptics\` with \`navigator.vibrate\` fallback.  
  
   - \*\*Android Hardware Back Button\*\* (\`js/app.js\`):  
  
     - Listen to \`backButton\` event from \`@capacitor/app\`; close open modal if active, else exit app if on main screen.  
  
   - \*\*Native Share Dialog\*\* (\`js/modals.js\` / \`js/uiController.js\`):  
  
     - Connect score sharing to \`@capacitor/share\` with Web Share API and clipboard fallback.  
  
\#\#\# Phase 2: Android Platform Setup (Local Windows Build)  
  
1. \*\*Add Android Platform:\*\*  
  
   - Run \`npx cap add android\` to generate the \`android/\` directory.  
  
   - Verify \`android/app/build.gradle\` and Android SDK platform levels (target SDK 35/36).  
  
2. \*\*Android Asset & Icon Generation:\*\*  
  
   - Prepare \`assets/icons/\` and \`assets/screenshots/\` if needed.  
  
\#\#\# Phase 3: iOS Cloud CI Setup (GitHub Actions \`macos-latest\`)  
  
1. \*\*Add iOS Platform:\*\*  
  
   - Run \`npx cap add ios\` to generate the \`ios/\` project structure.  
  
   - Add \`ios/App/ExportOptions.plist\` with \`method: app-store\`, \`teamID: YOUR\\\_APPLE\\\_TEAM\\\_ID\`, and provisioning profile configuration.  
  
2. \*\*Create GitHub Actions Release Workflow:\*\*  
  
   - Create \`.github/workflows/ios-release.yml\` for automated building on cloud Mac runners (\`macos-latest\`):  
  
     - Checkout & setup Node 20.  
  
     - \`npm ci && npm run prep:mobile && npx cap sync ios\`.  
  
     - \`pod install\`.  
  
     - Temporary keychain setup and distribution certificate import via GitHub Secrets.  
  
     - Provisioning profile installation.  
  
     - \`xcodebuild\` archive & export \`.ipa\`.  
  
     - Upload to App Store Connect / TestFlight via ASC API key (\`.p8\`).
```

