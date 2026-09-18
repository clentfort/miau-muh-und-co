# Miau, Muh und Mehr

An offline-first Android app for playing short animal videos. Animal names are shown in German. Animals can be shown as large tiles, a carousel, or a list. Selecting one plays up to three shuffled clips and then returns home.

## App development

Requirements: Node.js 24 and an Android device or emulator.

```sh
npm ci
npm run android
```

The first launch downloads the current content release over Wi-Fi. Later launches use the local copy and update it atomically when a new manifest is available.

Useful checks:

```sh
npm run typecheck
npm test
python3 -m unittest discover -s scripts/content -p 'test_*.py'
python3 -m unittest discover -s scripts/android -p 'test_*.py'
```

To create an installable APK without local Android tooling, run **Build Android APK** from GitHub Actions and download the `miau-muh-und-mehr` artifact. The release-signing keystore and credentials are backed up in the private 1Password vault and supplied to Actions through repository secrets. An EAS build is also configured:

```sh
npx eas-cli build --platform android --profile preview
```

## Adding an animal clip

No manifest editing is required.

1. Open **Actions** in `clentfort/miau-muh-und-mehr`.
2. Select **Add animal clip**.
3. Select **Run workflow**.
4. Enter an English animal name, the German name shown in the app, and a YouTube Short URL.

English names are trimmed, collapsed, and stored in lowercase; they identify the animal and stay searchable. The German name is displayed as entered, so capitalize it as a German noun (`Löwe`). It is required for a new animal and optional when appending a clip to an existing one. An exact normalized English name appends to the existing animal; a new name creates an animal. A typo therefore creates a separate entry.

Agents adding clips from a checkout should follow `.claude/skills/add-animal-clip/SKILL.md`.

The workflow downloads every missing source with `yt-dlp` through a pinned Cloudflare WARP container, normalizes it with FFmpeg, extracts a cover from the first clip, and publishes a rolling `content` GitHub Release. The app reads:

```text
https://github.com/clentfort/miau-muh-und-mehr/releases/download/content/manifest.json
```

The repository and release assets must be publicly readable by the app.

## Catalog

The catalog covers common zoo, farm, petting zoo, and household animals — 38 in total, from Affe to Ziege, with two clips for Löwe.

Pushing the repository to `main` runs the content workflow and creates the first release automatically.

## Content files

- `content/catalog.json` — workflow-managed source records
- `content/manifest.json` — generated published manifest (created by CI)
- `scripts/content/add_clip.py` — normalization and append/create logic
- `scripts/content/build_content.py` — download and FFmpeg pipeline
