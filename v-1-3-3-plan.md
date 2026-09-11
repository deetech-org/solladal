# "சொல்லாடல்" (Solladal) — Version 1.3.3 Build & Release Plan

## Comprehensive Step-by-Step Multi-Platform Release Guide (WWW • Cloudflare • Android • iOS)

**Publisher:** `deetech.org` • **App ID / Bundle ID:** `org.deetech.solladal` • **Target Release:** `v1.3.3`  
**Android Version Code:** `5` • **iOS Build Number:** `7` • **Total Word Bank:** `1,714 words` (expanded from 1,671)

---

## 1. User Review Required

> [!IMPORTANT]
> **Keypad Matrix Symmetry with ஸ்ரீ (Sri):**
> Appending `ஸ்ரீ` as the 24th key to the Mei keypad completes the Grantha consonant row (Row 4: `க்ஷ்`, `ஜ்`, `ஸ்`, `ஷ்`, `ஹ்`, `ஸ்ரீ`), transforming the Mei layout into a 6-column × 4-row matrix with zero empty cells.
> Because `ஸ்ரீ` is an indivisible, single-grapheme letter with a built-in vowel, tapping it will immediately display `ஸ்ரீ` in the synthesis preview and allow direct 1-tap entry without selecting an Uyir vowel.

> [!IMPORTANT]
> **Word Bank Expansion:**
> All 43 candidate words in [`words-to-be-added.md`](file:///d:/pethuraj/solladal/words-to-be-added.md) will be promoted into [`tamilwordbank-v2.md`](file:///d:/pethuraj/solladal/tamilwordbank-v2.md). Total word bank expands from 1,671 to 1,714 words.
> Denormalized dataset [`data/words.json`](file:///d:/pethuraj/solladal/data/words.json) will be re-indexed and the PWA Service Worker cache will be bumped with the new data hash.

---

## 2. Proposed Changes

### Component 1: Keypad UI & Input Synthesis Engine

#### [MODIFY] [js/tamilUtils.js](file:///d:/pethuraj/solladal/js/tamilUtils.js)
- Append `'ஸ்ரீ'` to `MEI_LETTERS` (24 keys total).
- Update `combineMeiUyir(mei, uyir)`: if `mei === 'ஸ்ரீ' || uyir === 'ஸ்ரீ'`, return `'ஸ்ரீ'` immediately.

#### [MODIFY] [js/uiController.js](file:///d:/pethuraj/solladal/js/uiController.js)
- In `handleMeiClick(mei)`: if `mei === 'ஸ்ரீ'`, clear `this.selectedUyir = null` to prevent conflicting vowel synthesis.
- In `handleUyirClick(uyir)`: if `this.selectedMei === 'ஸ்ரீ'`, clear `this.selectedMei = null`.

#### [MODIFY] [index.html](file:///d:/pethuraj/solladal/index.html)
- Update keypad markup comment: `<!-- Left: 24 Mei Keys (including ஸ்ரீ) -->`.
- Update version in footer: `சொல்லாடல் பதிப்பு v1.3.3 • Solladal Tamil Word Game`.

#### [NO CHANGE] [css/style.css](file:///d:/pethuraj/solladal/css/style.css)
- `#mei-keypad` is already `grid-template-columns: repeat(6, 1fr)`, so the 24th key fills the grid into a clean 6×4 with zero empty cells — **no CSS change required**.

---

### Component 2: Word Bank Promotion & Data Indexing

#### [NEW] [scripts/promote_words.py](file:///d:/pethuraj/solladal/scripts/promote_words.py)
- Script that parses [`words-to-be-added.md`](file:///d:/pethuraj/solladal/words-to-be-added.md), generates rows matching the **exact column schema** of [`tamilwordbank-v2.md`](file:///d:/pethuraj/solladal/tamilwordbank-v2.md), and merges them into the respective letter sections.
- Must preserve clue text verbatim, including the `===` blank markers (not `[...]`), and treat `ஸ்ரீ` as a single grapheme when classifying by letter length.

> [!WARNING]
> **Use `build_wordbank.py`, NOT `sync_wordbank.py`, for this release.** The live [`sw.js`](file:///d:/pethuraj/solladal/sw.js) cache name is `solladal-1.3.2-feac1356` — the `solladal-<version>-<hash>` format written by `build_wordbank.py`. `sync_wordbank.py` expects a `solladal-v<X.Y.Z>` format; run against the current tree it will fail to detect the existing version and reset to `1.0.0`. (The promotion note inside `words-to-be-added.md` still points at `sync_wordbank.py` and should be updated separately.)

#### [MODIFY] [scripts/build_wordbank.py](file:///d:/pethuraj/solladal/scripts/build_wordbank.py)
- Bump `VERSION = "1.3.3"`.
- Update `_GRAPHEME_RE` to treat `ஸ்ரீ` as a **single indivisible grapheme** (mirroring `getTamilLetters` in `tamilUtils.js` and the audit script) so `ஸ்ரீ`-words are length-classified correctly, and extend `transliterate()` with `ஸ்ரீ` $\rightarrow$ `sri`.
- Running it rebuilds [`data/words.json`](file:///d:/pethuraj/solladal/data/words.json) (stamping `metadata.version = "1.3.3"`) **and auto-bumps the root** [`sw.js`](file:///d:/pethuraj/solladal/sw.js) `CACHE_NAME` to `solladal-1.3.3-<newhash>` via `bump_service_worker()`. Do **not** hand-edit the root `sw.js` cache name — the builder owns it.

#### [RUN] Integration tests
- After the rebuild, run [`scripts/test_pwa_integration.py`](file:///d:/pethuraj/solladal/scripts/test_pwa_integration.py) and confirm it passes before packaging any build.

#### [MODIFY] [tamilwordbank-v2.md](file:///d:/pethuraj/solladal/tamilwordbank-v2.md)
- Promoted 43 candidate entries:
  - 1-Letter: +0 words $\rightarrow$ 100 words (unchanged)
  - 2-Letter: +2 words (`காணி`, `பொறை`) $\rightarrow$ 252 words
  - 3-Letter: +18 words $\rightarrow$ 394 words
  - 4-Letter: +16 words $\rightarrow$ 453 words
  - 5-Letter: +7 words $\rightarrow$ 515 words
  - **Total**: 1,671 + 43 = **1,714 words**.

---

### Component 3: Version Stamping & Four-Build Packaging

#### [MODIFY] [package.json](file:///d:/pethuraj/solladal/package.json)
- Bump version to `1.3.3`.

#### [MODIFY] [manifest.json](file:///d:/pethuraj/solladal/manifest.json)
- Bump version to `1.3.3`.

#### [MODIFY] [cloudflare/overlay/manifest.json](file:///d:/pethuraj/solladal/cloudflare/overlay/manifest.json)
- Bump version to `1.3.3`.

#### [MODIFY] [cloudflare/overlay/sw.js](file:///d:/pethuraj/solladal/cloudflare/overlay/sw.js)
- Bump `CACHE_NAME` to `solladal-web-1.3.3-cf3` (hand-edit; the overlay SW is separate from the root SW).
- Note: the **root** [`sw.js`](file:///d:/pethuraj/solladal/sw.js) cache name is bumped automatically by `build_wordbank.py` (Component 2) — do not edit it here.

#### [MODIFY] [android/app/build.gradle](file:///d:/pethuraj/solladal/android/app/build.gradle)
- Update `versionCode 4` and `versionName "1.3.3"`.

#### [MODIFY] [ios/App/App.xcodeproj/project.pbxproj](file:///d:/pethuraj/solladal/ios/App/App.xcodeproj/project.pbxproj)
- Update `MARKETING_VERSION = 1.3.3` and `CURRENT_PROJECT_VERSION = 7`.

---

## 3. Build & Release Execution Steps (All 4 Targets)

### Build 1: WWW (`./www`) & GitHub Pages
1. **Stage Runtime Assets into `./www`**:
   ```powershell
   npm run prep:mobile
   ```
2. **Verify Staged Output**:
   Check that `./www/` contains:
   - `index.html` (with `v1.3.3` in footer)
   - `data/words.json` (1,714 words)
   - `sw.js` (with updated cache name)
   - `manifest.json` (`1.3.3`)
   - `css/`, `js/`, `assets/`
3. **GitHub Pages Deployment**:
   - Pushing changes to `main` branch automatically triggers [`.github/workflows/pages.yml`](.github/workflows/pages.yml).
   - Deploys clean bundle to GitHub Pages environment.

---

### Build 2: Cloudflare Pages (`solladal.app`)
1. **Execute Cloudflare Build Script**:
   ```powershell
   node cloudflare/build.mjs
   ```
   *Action*:
   - Cleans `cloudflare/public/`.
   - Copies runtime from repo into `cloudflare/public/play/`.
   - Replaces share URL with `https://solladal.app`.
   - Lays down landing page, privacy policy, license, and overlay service worker (`solladal-web-1.3.3-cf3`).
2. **Deploy to Cloudflare Pages**:
   - **Method A (Direct CLI with Wrangler)**:
     ```powershell
     npx wrangler pages deploy cloudflare/public --project-name solladal-app
     ```
   - **Method B (Git Push)**:
     Pushing changes to GitHub triggers Cloudflare Pages integration connected to the repository.
3. **Production Verification**:
   - Visit `https://solladal.app/play/`.
   - Inspect DevTools Application tab: verify Service Worker active with `solladal-web-1.3.3-cf3`.
   - Test typing a word with `ஸ்ரீ`.

---

### Build 3: Android Release (`org.deetech.solladal`)
1. **Sync Mobile Web Assets to Android Project**:
   ```powershell
   npm run build:android
   ```
   *(This runs `prep:mobile` and executes `npx cap sync android`).*
2. **Bump Android Versions**:
   In [`android/app/build.gradle`](android/app/build.gradle):
   ```groovy
   defaultConfig {
       applicationId "org.deetech.solladal"
       minSdkVersion rootProject.ext.minSdkVersion
       targetSdkVersion rootProject.ext.targetSdkVersion
       versionCode 4
       versionName "1.3.3"
   }
   ```
3. **Build Production Android App Bundle (.aab)**:
   ```powershell
   cd android
   .\gradlew.bat clean bundleRelease
   cd ..
   ```
4. **Verify Bundle**:
   Verify the output file exists:
   `android/app/build/outputs/bundle/release/app-release.aab`
5. **Google Play Console Release**:
   - Log into [Google Play Console](https://play.google.com/console).
   - Select **Solladal (சொல்லாடல்)** $\rightarrow$ **Production** $\rightarrow$ **Create new release**.
   - Upload `app-release.aab`.
   - **Release Name:** `1.3.3 (4)`
   - **Release Notes (English):**
     ```text
     What's New in Version 1.3.3:
     - Added dedicated single-touch 'ஸ்ரீ' (Sri) key to the virtual keypad
     - Expanded word bank to 1,714 words with 43 classical, literary, and cinema gems
     - Enhanced dictionary & literature clues across Sangam, Bharathiyar, and Thirukkural
     - 100% offline, privacy-first, zero ads
     ```
   - **Release Notes (Tamil):**
     ```text
     சொல்லாடல் பதிப்பு v1.3.3 வெளியீடு:
     - விசைப்பலகையில் பிரத்யேக 'ஸ்ரீ' பொத்தான் சேர்க்கப்பட்டது
     - 43 புதிய செந்தமிழ், இலக்கிய, சினிமா பாடல்கள் சேர்க்கப்பட்டு சொல் வங்கி 1,714 சொற்களாக விரிவுபடுத்தப்பட்டது
     - திருக்குறள், பாரதியார், திருவாசகக் குறிப்புகள் மேம்படுத்தப்பட்டன
     - இணையம் தேவையில்லை, விளம்பரங்கள் இல்லை
     ```
   - Click **Save** $\rightarrow$ **Review release** $\rightarrow$ **Start rollout to Production**.

---

### Build 4: iOS Release (`org.deetech.solladal`)
1. **Sync Mobile Web Assets to iOS Project**:
   ```powershell
   npm run build:ios
   ```
   *(This runs `prep:mobile` and executes `npx cap sync ios`).*
2. **Bump iOS Versions in Xcode Project**:
   In [`ios/App/App.xcodeproj/project.pbxproj`](ios/App/App.xcodeproj/project.pbxproj), update all occurrences:
   - `CURRENT_PROJECT_VERSION = 7;`
   - `MARKETING_VERSION = 1.3.3;`
3. **Trigger Automated Cloud Build via GitHub Actions**:
   Create and push the version release tag. **Stage only release files** — the working tree currently holds several unrelated untracked scripts (patent/figure generators, `build_bw_app.py`, etc.); `git add .` would sweep them into the release commit. Stage deliberately:
   ```powershell
   git add index.html manifest.json sw.js data/words.json js/ css/ package.json `
           tamilwordbank-v2.md words-to-be-added.md scripts/build_wordbank.py scripts/promote_words.py `
           cloudflare/overlay/ android/app/build.gradle ios/App/App.xcodeproj/project.pbxproj
   git status   # confirm nothing unrelated is staged
   git commit -m "Release v1.3.3: ஸ்ரீ keypad button, 1,714 words, multi-platform sync"
   git tag ios-v1.3.3
   git push origin main
   git push origin ios-v1.3.3
   ```
4. **Monitor CI Workflow**:
   - Navigate to **GitHub $\rightarrow$ Actions $\rightarrow$ iOS Release (Capacitor)**.
   - The cloud macOS runner will:
     1. Check out repository & run `npm ci`.
     2. Stage `./www` and run `npx cap sync ios`.
     3. Run `pod install` in `ios/App`.
     4. Decrypt distribution certificate (`IOS_DIST_CERT_P12_BASE64`) and install provisioning profile (`IOS_PROVISIONING_PROFILE_BASE64`).
     5. Execute `xcodebuild` archive & export `App.ipa`.
     6. Upload build to Apple TestFlight / App Store Connect via ASC API Key (`APP_STORE_CONNECT_API_KEY_P8`).
5. **App Store Connect Submission**:
   - Log into [App Store Connect](https://appstoreconnect.apple.com/).
   - Select **Solladal** $\rightarrow$ **iOS App** $\rightarrow$ **Prepare for Submission**.
   - Under **Build**, select `1.3.3 (7)`.
   - Update **What's New in This Version**:
     ```text
     - Added dedicated single-touch 'ஸ்ரீ' (Sri) key to the keypad
     - Expanded vocabulary library to 1,714 verified Tamil words
     - Added new literary references from Bharathiyar, Thirukkural, and classic poetry
     - Performance optimizations and offline cache enhancements
     ```
   - Submit for App Store Review.

---

## 4. Post-Release Verification & Sanity Checklist

| Checkpoint | Target / Verification Method | Pass Criteria |
| :--- | :--- | :---: |
| **Keypad Grid Count** | Inspect DOM `#mei-keypad .key-btn` | Exactly 24 buttons |
| **`ஸ்ரீ` Key Behavior** | Click `ஸ்ரீ` button on board | Preview shows `ஸ்ரீ`, commit enters `ஸ்ரீ` |
| **Word Bank Count** | Open Word Bank modal, view total badge | Exactly 1,714 words |
| **Offline Cache (PWA)** | Reload page in offline network mode | App loads 100% instantly |
| **Cloudflare Live** | Curl `https://solladal.app/play/data/words.json` | JSON `metadata.version` is `"1.3.3"`, `metadata.totalWords` is `1714` |
| **Google Play** | Play Console Release Dashboard | Version 1.3.3 (4) in review / published |
| **App Store Connect** | TestFlight build status | Build 1.3.3 (7) Ready to Test / Submit |

---

## 5. Rollback & Contingency Plan

If an unexpected regression occurs on any platform during rollout:
- **Cloudflare Pages**: Instant rollback via Wrangler or Cloudflare Pages dashboard to previous deployment hash in < 30 seconds.
- **GitHub Pages**: Re-run prior successful workflow in Actions tab or revert release commit on `main`.
- **Google Play**: Halt rollout in Google Play Console (if staged rollout percentage < 100%) or deploy expedited hotfix incrementing `versionCode 5`.
- **iOS / TestFlight**: Expire build in TestFlight or reject binary in App Store Connect prior to review release.

