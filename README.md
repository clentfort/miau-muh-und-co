# Miau, Muh und Co

An offline-first Android app for playing short animal videos. Animals can be shown as large tiles, a carousel, or a list. Selecting one plays up to three shuffled clips and then returns home.

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
```

To create an installable Android APK with EAS:

```sh
npx eas-cli build --platform android --profile preview
```

## Adding an animal clip

No manifest editing is required.

1. Open **Actions** in `clentfort/miau-muh-und-co`.
2. Select **Add animal clip**.
3. Select **Run workflow**.
4. Enter an English animal name and a YouTube Short URL.

Names are trimmed, collapsed, and stored in lowercase. An exact normalized name appends to the existing animal; a new name creates an animal. A typo therefore creates a separate entry.

The workflow downloads every missing source with `yt-dlp`, normalizes it with FFmpeg, extracts a cover from the first clip, and publishes a rolling `content` GitHub Release. The app reads:

```text
https://github.com/clentfort/miau-muh-und-co/releases/download/content/manifest.json
```

The repository and release assets must be publicly readable by the app.

## Initial catalog

The initial source catalog contains:

- giraffe
- gnu
- lion (two clips)
- seal

Pushing the repository to `main` runs the content workflow and creates the first release automatically.

## Content files

- `content/catalog.json` — workflow-managed source records
- `content/manifest.json` — generated published manifest (created by CI)
- `scripts/content/add_clip.py` — normalization and append/create logic
- `scripts/content/build_content.py` — download and FFmpeg pipeline
