# "சொல்லாடல்" (Solladal) — Android Build & Release Plan
## Step-by-Step Security-First Guide for Google Play Store Distribution
**Publisher:** `deetech.org` • **Application ID:** `org.deetech.solladal` • **App Version:** `1.3.2` (Version Code `2`)

---

## 1. Architecture & Release Overview

**சொல்லாடல் (Solladal)** uses a **vanilla HTML/CSS/JS PWA core** wrapped with **Capacitor** for Android distribution. Because development is conducted on a Windows workstation equipped with OpenJDK 21 and the Android SDK, release builds are generated locally via Gradle and uploaded directly to the Google Play Console.

```
┌─────────────────────────────────────────────────────────────────────────┐
│              LOCAL WORKSPACE (solladal/)                                │
│  - Vanilla PWA Core (1,671 Words, Local Fonts, Responsive UI)           │
│  - Staged into ./www via npm run prep:mobile                            │
│  - Keystore & key.properties secured and excluded from Git              │
└────────────────────────────────────┬────────────────────────────────────┘
                                     │ npx cap sync android
                                     ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                     ANDROID GRADLE BUILD SYSTEM                         │
│  1. ./gradlew.bat bundleRelease → Production Android App Bundle (.aab)  │
│  2. ./gradlew.bat assembleDebug → Debug APK for local device testing    │
│  3. Signed with local release keystore (RSA 4096-bit / 2048-bit)        │
└────────────────────────────────────┬────────────────────────────────────┘
                                     │ Manual / Automated Upload
                                     ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                     GOOGLE PLAY DEVELOPER CONSOLE                       │
│  - Google Play App Signing (Play Integrity & key derivation)            │
│  - Target Audience: Families / Children (Ages 6-8, 9-12)                │
│  - 100% Offline, Zero Ads, Zero Data Collected                          │
│  - Production Track Release & Global Distribution                       │
└─────────────────────────────────────────────────────────────────────────┘
```

> [!CAUTION]
> **Strict Security Discipline:**
> - **NEVER** commit keystore files (`.keystore`, `.jks`), `key.properties`, or plaintext passwords to Git.
> - Keystores are strictly excluded in [`.gitignore`](.gitignore) (`*.jks`, `*.keystore`, `*.key`, `key.properties`).
> - Keep a secure, encrypted backup of your release keystore in your password manager.

---

## 2. Phase 1: Keystore Generation & Key Management (One-Time)

Google Play requires all release App Bundles (`.aab`) to be cryptographically signed by the developer.

### Step 1.1: Generate a Production Release Keystore

Open PowerShell on your workstation and run `keytool` (included with OpenJDK 21):

```powershell
keytool -genkey -v -keystore "$HOME\.android\solladal-release.keystore" `
  -alias solladal `
  -keyalg RSA `
  -keysize 2048 `
  -validity 10000 `
  -dname "CN=deetech.org, OU=Solladal, O=DEE TECH LLC, L=Coimbatore, ST=Tamil Nadu, C=IN"
```

1. Enter a **strong password** when prompted and record it in your password manager.
2. The keystore will be saved safely in your user `.android` directory (`~/.android/solladal-release.keystore`, outside the repository).

---

### Step 1.2: Configure `key.properties` (Local Machine Only)

Create a file named `android/key.properties` on your local machine:

```properties
storePassword=YOUR_KEYSTORE_PASSWORD
keyPassword=YOUR_KEY_PASSWORD
keyAlias=solladal
storeFile=C:\\Users\\<YOUR_USER>\\.android\\solladal-release.keystore
```

*(Note: `android/key.properties` is in `.gitignore` and is never committed to GitHub).*

---

## 3. Phase 2: Building the Production App Bundle (.aab)

Whenever you prepare a new release for Google Play:

### Step 2.1: Stage Web Assets & Synchronize Android Platform

From the project root directory (`./`):

```powershell
# 1. Install dependencies (if needed)
npm install

# 2. Stage runtime assets into ./www (isolates tests and markdown)
npm run prep:mobile

# 3. Synchronize Capacitor Android platform
npx cap sync android
```

---

### Step 2.2: Compile the Release App Bundle (.aab)

Run the Gradle release bundle task:

```powershell
cd android
.\gradlew.bat bundleRelease
cd ..
```

When Gradle completes (`BUILD SUCCESSFUL`), the compiled release bundle is at:
📁 **`android/app/build/outputs/bundle/release/app-release.aab`**

---

### Step 2.3: Sign & Verify the Release App Bundle (.aab)

#### 1. (Optional) Check Key Alias in Keystore:
```powershell
& "$env:JAVA_HOME\bin\keytool.exe" -list -v -keystore "android\solladal-release-key.jks"
```

#### 2. Sign the `.aab` Bundle with `jarsigner`:
```powershell
& "$env:JAVA_HOME\bin\jarsigner.exe" -verbose -sigalg SHA256withRSA -digestalg SHA-256 `
  -keystore "android\solladal-release-key.jks" `
  "android\app\build\outputs\bundle\release\app-release.aab" `
  solladal
```
*(Enter your keystore password when prompted; `jarsigner` will output `jar signed`).*

#### 3. Verify Signature:
```powershell
& "$env:JAVA_HOME\bin\jarsigner.exe" -verify -verbose -certs "android\app\build\outputs\bundle\release\app-release.aab"
```
*(Note: `[Invalid certificate chain: PKIX path building failed]` is expected and normal for self-signed Android developer keys; the key signature is valid and confirmed).*

---

### Step 2.4: (Optional) Compile Debug APK for Device & Emulator Testing

To test the live build immediately on an Android phone or emulator via USB / ADB:

```powershell
cd android
.\gradlew.bat assembleDebug
cd ..
```
The installable APK will be at:
📁 **`android/app/build/outputs/apk/debug/app-debug.apk`**

Install on connected device or emulator via:
```powershell
adb install -r android\app\build\outputs\apk\debug\app-debug.apk
```

---

## 4. Phase 3: Google Play Console Listing & Store Assets

### Step 3.1: Store Listing Metadata

| Field | Content |
| :--- | :--- |
| **App Name** | `சொல்லாடல் (Solladal) — Tamil Word Game` |
| **Short Description** (max 80 chars) | `Educational Tamil Word Guessing Game with 1,600+ words, clues & UyirMei keypad.` |
| **Full Description** | Educational Tamil word game for Grade 1–5 students and learners. Features 1,671 curated words, 3-tier progressive clues (Meaning, Literature, Riddles), 2-step UyirMei keyboard, 100% offline gameplay, and zero ads. |
| **Category** | `Word` (Educational / Family) |
| **Contact Email** | `contact@deetech.org` |
| **Privacy Policy URL** | `https://deetech-org.github.io/solladal/PRIVACY.md` |

---

### Step 3.2: Store Graphic Assets Checklist

All required assets are generated and available in `assets/screenshots/`:

| Graphic Asset | Specification | Local File Path |
| :--- | :--- | :--- |
| **App Icon** | $512 \times 512\text{ px}$ PNG (32-bit, max 1MB) | [`assets/icons/icon-512.png`](assets/icons/icon-512.png) |
| **Feature Graphic** | $1024 \times 500\text{ px}$ PNG (no alpha, max 15MB) | [`assets/icons/feature-graphic.png`](assets/icons/feature-graphic.png) |
| **Phone Screenshots** | Min 2, 9:16 aspect ratio ($1080 \times 1920$) | `assets/screenshots/` |
| **7-inch Tablet** | Min 2, 9:16 or 16:9 ($1080 \times 1920$) | [`assets/screenshots/tab-7inch-*.png`](assets/screenshots/) |
| **10-inch Tablet** | Min 2, 9:16 or 16:9 ($1080 \times 1920$) | [`assets/screenshots/tab-10inch-*.png`](assets/screenshots/) |

---

## 5. Phase 4: Policy & Safety Declarations (Google Play Console)

Complete these sections in Google Play Console before submitting:

### 1. Data Safety Declaration
- **Does your app collect or share user data?** $\rightarrow$ **No**.
- **Data Encrypted in Transit:** Yes (all network traffic uses TLS/HTTPS).
- **Account Creation / Deletion:** Not applicable (offline game, no accounts).

### 2. Target Audience & Content (Families Policy)
- **Target Age Groups:** Select **6–8**, **9–12**, and **13+**.
- **Appeal to Children:** Yes.
- **Ads Declaration:** Select **"No, my app does not contain ads"**.
- **Families Policy Compliance:** Confirmed (complies with COPPA and Google Play Families Policy).

### 3. Content Rating (IARC Questionnaire)
- Category: **Game** $\rightarrow$ **Word / Trivia**.
- Violence, Blood, Sexual Content, Gambling, Offensive Language: **None**.
- Result: **Rated 3+ (Everyone)** globally.

---

## 6. Phase 5: Release Creation & Production Rollout

1. In Google Play Console, go to **Release $\rightarrow$ Production $\rightarrow$ Create new release**.
2. **App Bundles:** Upload `android/app/build/outputs/bundle/release/app-release.aab`.
3. **Release Name:** `1.3.2 (2)`
4. **Release Notes (Bilingual XML format):**
   ```xml
   <en-US>
   Initial release of Solladal (சொல்லாடல்) v1.3.2:
   - 1,671 curated Tamil words with 3-tier progressive clues (Meaning, Literature, Riddles)
   - Interactive two-step UyirMei combination keyboard
   - 100% offline gameplay with zero ads and zero tracking
   </en-US>
   <ta-IN>
   சொல்லாடல் பதிப்பு v1.3.2 வெளியீடு:
   - 1,671 தமிழ் சொற்கள் மற்றும் 3 நிலை உதவிக் குறிப்புகள் (பொருள், இலக்கியம், விடுகதை)
   - 2-படி உயிர்மெய் எழுத்து சேர்க்கை விசைப்பலகை
   - 100% ஆஃப்லைன் வசதி, விளம்பரங்கள் அற்ற தூய அனுபவம்
   </ta-IN>
   ```
5. Click **Save** $\rightarrow$ **Review release** $\rightarrow$ **Start rollout to Production**.

---

## 7. Version Bumping Checklist for Future Updates

When releasing a new version (e.g. `v1.4.0` / Version Code `3`), synchronize across all 5 files:

1. **`android/app/build.gradle`**:
   ```groovy
   versionCode 3
   versionName "1.4.0"
   ```
2. **`package.json`**: `"version": "1.4.0"`
3. **`manifest.json`**: `"version": "1.4.0"`
4. **`sw.js`**: `const CACHE_NAME = 'solladal-v1.4.0';`
5. **`index.html`**: Update version badge in Help modal to `v1.4.0`.

Then rebuild via:
```powershell
npm run prep:mobile
npx cap sync android
cd android; .\gradlew.bat bundleRelease; cd ..
```

---

## 8. Troubleshooting & Common Build Issues

| Issue | Root Cause | Solution |
| :--- | :--- | :--- |
| `Release notes: Line 1: text outside language tags` | Play Console requires XML language tags. | Wrap text in `<en-US>...</en-US>` and `<ta-IN>...</ta-IN>`. |
| `Warning: There is no deobfuscation file` | Non-blocking warning when ProGuard/R8 is disabled. | Informational only. Click "Next / Save" safely since Solladal runs web-core logic. |
| `Execution failed for task ':app:bundleRelease'` | Missing or mismatched keystore path/password. | Verify `android/key.properties` paths and password strings. |
| `Asset changes not appearing in Android build` | Forgot to stage web assets before building. | Run `npm run prep:mobile` followed by `npx cap sync android`. |
