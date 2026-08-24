# "சொல்லாடல்" (Solladal) — iOS Build & Release Plan

## Step-by-Step Security-First Guide for App Store Distribution

**Publisher:** `deetech.org` • **Bundle Identifier:** `org.deetech.solladal` • **App Version:** `1.3.2` (Build `2`)


## 1. Architecture & Security Overview

Because development is conducted on a Windows workstation, the iOS release is built using **GitHub Actions on a cloud macOS runner (`macos-latest`)** equipped with Xcode, CocoaPods, and Apple CLI signing tools (`xcodebuild`, `altool`/`notarytool`).

```
┌─────────────────────────────────────────────────────────────────────────┐  
│              LOCAL WORKSPACE (Windows - solladal\\)           │  
│  - Vanilla PWA Core (1,500 Words, Local Fonts, Responsive UI)           │  
│  - Staged into ./www via npm run prep:mobile                            │  
│  - Private Keys & Passwords converted to Base64 and stored in Secrets  │  
└────────────────────────────────────┬────────────────────────────────────┘  
                                     │ git push / GitHub Repository Secrets  
                                     ▼  
┌─────────────────────────────────────────────────────────────────────────┐  
│           GITHUB ACTIONS CLOUD CI (macos-latest Runner + Xcode)         │  
│  1. Checkout & npm ci → Staging ./www → npx cap sync ios               │  
│  2. Pod Install (Capacitor iOS CocoaPods)                               │  
│  3. Decode base64 cert into ephemeral, isolated build.keychain          │  
│  4. Install .mobileprovision profile                                    │  
│  5. xcodebuild clean archive → .xcarchive                               │  
│  6. xcodebuild -exportArchive → App.ipa (Production Signed)            │  
│  7. Upload to TestFlight / App Store Connect via ASC API Key (.p8)     │  
│  8. Delete ephemeral keychain & publish .ipa artifact                   │  
└────────────────────────────────────┬────────────────────────────────────┘  
                                     │ Automated Delivery  
                                     ▼  
┌─────────────────────────────────────────────────────────────────────────┐  
│                 APPLE APP STORE CONNECT / TESTFLIGHT                    │  
│  - Internal / External TestFlight Testing                               │  
│  - App Store Review Submission & Global Release                         │  
└─────────────────────────────────────────────────────────────────────────┘
```

> \[!CAUTION\] **Strict Security Discipline:**

> - **NEVER** commit certificates (`.p12`), private keys (`.p8`), provisioning profiles (`.mobileprovision`), or plaintext passwords to Git.

> - All signing credentials reside exclusively in **GitHub Repository Encrypted Secrets**, which are masked in logs and injected into ephemeral CI memory.


## 2. Phase 1: Apple Developer Portal Setup (One-Time)

Log in to the [Apple Developer Member Center](https://developer.apple.com/account/).

### Step 1.1: Register App ID

1. Navigate to **Certificates, Identifiers & Profiles $\\rightarrow$ Identifiers $\\rightarrow$ (+)**.

2. Select **App IDs** $\\rightarrow$ **App**.

3. **Description:** `Solladal Tamil Word Game`

4. **Bundle ID:** Select **Explicit** $\\rightarrow$ enter `org.deetech.solladal`.

5. Under Capabilities, keep defaults (no special entitlements needed). Click **Register**.


### Step 1.2: Generate Apple Distribution Certificate (`.p12`)

1. In **Certificates, Identifiers & Profiles $\\rightarrow$ Certificates $\\rightarrow$ (+)**.

2. Select **Apple Distribution** (or *iOS Distribution*).

3. If creating on a Mac (Keychain Access) or via an OpenSSL Certificate Signing Request (CSR):

   - Upload the `.certSigningRequest` file.

   - Download the generated `.cer` file.

   - Double-click to open in macOS Keychain Access $\\rightarrow$ right-click the certificate $\\rightarrow$ select **Export "Apple Distribution: ..."**.

   - Save as `solladal-dist-cert.p12`.

   - Set a strong export password (e.g. 20+ random characters). Save this password!


### Step 1.3: Generate App Store Provisioning Profile

1. In **Certificates, Identifiers & Profiles $\\rightarrow$ Profiles $\\rightarrow$ (+)**.

2. Select **App Store** under *Distribution*.

3. Choose the App ID: `org.deetech.solladal`.

4. Select your **Apple Distribution Certificate** created in Step 1.2.

5. **Profile Name:** `Solladal AppStore Distribution`

6. Download the file: `Solladal\_AppStore.mobileprovision`.


### Step 1.4: Generate App Store Connect API Key (`.p8`)

*(Used by GitHub Actions to securely upload the build without 2-Factor Authentication friction).*

1. Log in to [App Store Connect](https://appstoreconnect.apple.com/).

2. Go to **Users and Access $\\rightarrow$ Integrations $\\rightarrow$ App Store Connect API** (or *Keys*).

3. Click **(+)** to generate an API Key:

   - **Name:** `GitHub CI Solladal Uploader`

   - **Access:** `App Manager` (or `Admin`).

4. Note the following values immediately:

   - **Issuer ID** (UUID at the top of the page, e.g. `57246542-96fe-1a63-e053-0824d011072a`).

   - **Key ID** (10-character string, e.g. `2X9R4HXF34`).

5. Click **Download API Key** to get `AuthKey\_XXXXXXXXXX.p8`.  
*(Note: Apple only lets you download this `.p8` file once).*


## 3. Phase 2: Secure Secret Management (Handling Credentials)

Convert your private credentials into Base64 strings locally on your computer so they can be stored as encrypted secrets in GitHub.

### Step 2.1: Convert Files to Base64 (on Windows PowerShell)

Run these commands in PowerShell (replace file paths with your actual downloaded files):

```
\# 1. Base64 Encode Distribution Certificate (.p12)  
\[Convert\]::ToBase64String(\[IO.File\]::ReadAllBytes("C:\\path\\to\\solladal-dist-cert.p12")) | Set-Clipboard  
\# The base64 string is now in your clipboard! Paste it into GitHub Secret: IOS\_DIST\_CERT\_P12\_BASE64  
  
\# 2. Base64 Encode Provisioning Profile (.mobileprovision)  
\[Convert\]::ToBase64String(\[IO.File\]::ReadAllBytes("C:\\path\\to\\Solladal\_AppStore.mobileprovision")) | Set-Clipboard  
\# Paste into GitHub Secret: IOS\_PROVISIONING\_PROFILE\_BASE64  
  
\# 3. Base64 Encode App Store Connect API Key (.p8)  
\[Convert\]::ToBase64String(\[IO.File\]::ReadAllBytes("C:\\path\\to\\AuthKey\_XXXXXXXXXX.p8")) | Set-Clipboard  
\# Paste into GitHub Secret: ASC\_API\_KEY\_P8\_BASE64
```


### Step 2.2: Add Secrets to GitHub Repository

1. Open your repository: **[https://github.com/deetech-org/solladal**](https://github.com/deetech-org/solladal)

2. Go to **Settings $\\rightarrow$ Secrets and variables $\\rightarrow$ Actions $\\rightarrow$ New repository secret**.

3. Create the following **7 Secrets**:

| Secret Name | Content to Enter |
| - | - |
| **`IOS\_DIST\_CERT\_P12\_BASE64`** | The Base64 string of your `.p12` certificate. |
| **`IOS\_DIST\_CERT\_PASSWORD`** | The password you chose when exporting the `.p12` certificate. |
| **`IOS\_PROVISIONING\_PROFILE\_BASE64`** | The Base64 string of your `.mobileprovision` file. |
| **`IOS\_KEYCHAIN\_PASSWORD`** | Any random strong string (e.g. `TempCiKeyChainPass2026!`) used to lock the temporary CI keychain. |
| **`ASC\_KEY\_ID`** | The 10-character Key ID from App Store Connect (e.g. `2X9R4HXF34`). |
| **`ASC\_ISSUER\_ID`** | The Issuer ID UUID from App Store Connect (e.g. `57246542-96fe-1a63-e053-0824d011072a`). |
| **`ASC\_API\_KEY\_P8\_BASE64`** | The Base64 string of your `AuthKey\_XXXXXXXXXX.p8` private key file. |



## 4. Phase 3: Project Configuration (`ExportOptions.plist`)

Update [`ios/App/ExportOptions.plist`](ios/App/ExportOptions.plist) with your Apple Team ID and Provisioning Profile Name:

```
\<?xml version="1.0" encoding="UTF-8"?\>  
\<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd"\>  
\<plist version="1.0"\>  
\<dict\>  
  \<key\>method\</key\>  
  \<string\>app-store\</string\>  
  \<key\>teamID\</key\>  
  \<string\>YOUR\_APPLE\_TEAM\_ID\</string\>  
  \<key\>uploadSymbols\</key\>  
  \<true/\>  
  \<key\>signingStyle\</key\>  
  \<string\>manual\</string\>  
  \<key\>provisioningProfiles\</key\>  
  \<dict\>  
    \<key\>org.deetech.solladal\</key\>  
    \<string\>Solladal AppStore Distribution\</string\>  
  \</dict\>  
\</dict\>  
\</plist\>
```

*(Your Apple Team ID is visible in the top-right corner of the Apple Developer portal next to `deetech.org`).*


## 5. Phase 4: Triggering the Cloud Build & Release

You can trigger the iOS release in two ways:

### Option A: Manual Trigger via GitHub Actions Web UI (Recommended)

1. Go to **[https://github.com/deetech-org/solladal/actions**](https://github.com/deetech-org/solladal/actions).

2. Click **iOS Release (Capacitor)** in the left sidebar.

3. Click **Run workflow** $\\rightarrow$ select branch `main` $\\rightarrow$ click **Run workflow**.

4. GitHub Actions boots a macOS runner, compiles the web bundle, runs `pod install`, codesigns with your certificate, exports `App.ipa`, and uploads directly to App Store Connect / TestFlight.

5. You can also download the signed `.ipa` build artifact directly from the workflow run summary page!


### Option B: Trigger via Git Release Tag

Push a version tag to origin:

```
git tag ios-v1.3.2  
git push origin ios-v1.3.2
```

*The workflow will start automatically.*


## 6. Phase 5: Alternative Local Mac / Xcode Workflow

If you or a team member has access to a physical Mac or MacBook:

```
\# 1. Clone repo on Mac  
git clone https://github.com/deetech-org/solladal.git  
cd solladal  
  
\# 2. Install dependencies & stage assets  
npm ci  
npm run prep:mobile  
npx cap sync ios  
  
\# 3. Open in Xcode  
npx cap open ios
```

Inside Xcode:

1. Select the root **App** target $\\rightarrow$ **Signing & Capabilities**.

2. Check **Automatically manage signing** and select your `deetech.org` team (or choose manual signing with your profile).

3. Set destination in top bar to **Any iOS Device (arm64)**.

4. Go to **Product $\\rightarrow$ Archive**.

5. When the Organizer window appears:

   - Click **Distribute App** $\\rightarrow$ select **App Store Connect** $\\rightarrow$ click **Upload**.

   - Xcode handles validation, signing, and TestFlight delivery.


## 7. Phase 6: App Store Connect Submission & Review

Once uploaded, the build will process in App Store Connect (typically 10–15 minutes).

### Step 6.1: TestFlight Internal Testing

1. In [App Store Connect](https://appstoreconnect.apple.com/) $\\rightarrow$ **Apps $\\rightarrow$ சொல்லாடல்**.

2. Go to **TestFlight** tab.

3. Under *Internal Testing*, add your email/testers.

4. Install the **TestFlight app** from the App Store on an iPhone/iPad and test the build.


### Step 6.2: App Store Listing Metadata & Submitting for Review

Under **App Store $\\rightarrow$ 1.0 (or 1.3.2) Prepare for Submission**:

1. **App Name:** `சொல்லாடல் (Solladal) — Tamil Word Game`

2. **Subtitle (max 30 chars):** `Tamil Word Guessing Game`

3. **Primary Category:** `Games / Word` (Secondary: `Education`).

4. **Age Rating (Questionnaire):**

   - No violence, gambling, or mature content $\\rightarrow$ Rated **4+** (and select **Made for Kids: Ages 6–8 & 9–11**).

5. **App Privacy:**

   - Select **"No, we do not collect data from this app"**.

   - Provide Privacy Policy URL: `https://deetech-org.github.io/solladal/PRIVACY.md` (or your hosted deetech.org link).

6. **Screenshots:**

   - Upload 6.5" / 6.7" iPhone screenshots (captured from iPhone or scaled from 9:16).

   - Upload 12.9" iPad screenshots (using `assets/screenshots/tab-10inch-\*.png`).

7. **Select Build:**

   - Click **(+)** under *Build* $\\rightarrow$ select Version `1.3.2 (2)`.

8. Click **Submit for Review**.

*(Apple review for educational/family apps typically takes 24 to 48 hours).*


## 8. Troubleshooting & Common Issues

| Issue | Root Cause | Solution |
| - | - | - |
| `Code signing failed: No profile matching...` | Profile name in `ExportOptions.plist` doesn't match developer portal. | Ensure `\<string\>Solladal AppStore Distribution\</string\>` exactly matches the profile name in Apple Developer Portal. |
| `Missing Purpose String in Info.plist` | Apple rejects apps for unrequested permissions. | Solladal uses zero hardware permissions (no camera, microphone, or location). Keep Info.plist minimal. |
| `Non-Exempt Encryption (ITMS-90738)` | Apple requires declaration regarding HTTPS encryption. | Already configured in `ios/App/App/Info.plist` with `\<key\>ITSAppUsesNonExemptEncryption\</key\>\<false/\>`. |
| `Session expired during upload` | Token expired during long upload. | Handled automatically by the App Store Connect API Key (`.p8`), which uses fresh stateless JWT tokens for every upload. |


