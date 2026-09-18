---
name: add-animal-clip
description: Add animal clips to the Miau, Muh und mehr catalog - find a suitable YouTube Short, pick the German display name, and append it to content/catalog.json so CI publishes the media. Use when the user asks to add an animal, add a sound or clip, extend the catalog, or replace a clip that no longer works.
---

# Add an animal clip

The app plays short videos of real animals. Every clip comes from a YouTube
Short that CI downloads, normalizes, and publishes as a GitHub Release asset.
Only `content/catalog.json` is edited by hand; `content/manifest.json` and the
media are generated.

## Catalog entry

```json
{
  "id": "guinea-pig",
  "name": "guinea pig",
  "nameDe": "Meerschweinchen",
  "sources": [
    { "youtubeId": "JoNTmi6sfro", "url": "https://www.youtube.com/shorts/JoNTmi6sfro" }
  ]
}
```

- `id` — slug derived from the English name, stable, used in asset filenames.
- `name` — English, lowercase, single spaces. Identifies the animal and is also
  searchable in the app.
- `nameDe` — the German name exactly as it should appear in the UI, so
  capitalized as a German noun (`Löwe`, `Erdmännchen`). This is what the app
  displays. Required for every animal.
- `sources` — one entry per clip. Several clips per animal are fine; playback
  shuffles up to three of them.

Animals are sorted by `nameDe` with umlauts folded (`ä`→`a`, `ö`→`o`, `ü`→`u`,
`ß`→`ss`), so `Bär` sorts next to `Bar` rather than after `Bz`.

## Finding a clip

Use the `agent-browser` skill against YouTube search and read the result titles:

```bash
export AGENT_BROWSER_SESSION="$(agent-browser session id --scope worktree --prefix animals)"
agent-browser open "https://www.youtube.com/results?search_query=goat+sound+shorts"
agent-browser eval "Array.from(document.querySelectorAll('a[href*=\"/shorts/\"]')).map(a=>a.href+' | '+(a.innerText||'').replace(/\n/g,' ').slice(0,70)).filter(s=>s.split('| ')[1]).slice(0,8).join('\n')"
```

Pick a clip that shows the real animal making its own sound. Avoid memes,
AI-generated or cartoon footage, pure sound-effect uploads with unrelated
video, and anything scary or violent — the audience is small children.

Verify every candidate is public and embeddable before adding it; a 200 means
the video can be downloaded by CI:

```bash
curl -s -o /dev/null -w "%{http_code}\n" \
  "https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v=<videoId>&format=json"
```

## Adding the entry

Prefer the script over hand-editing, because it normalizes names, derives the
id, rejects duplicate videos, and keeps the sort order:

```bash
python3 scripts/content/add_clip.py \
  --catalog content/catalog.json \
  --animal "guinea pig" \
  --name-de "Meerschweinchen" \
  --url "https://www.youtube.com/shorts/JoNTmi6sfro"
```

`--name-de` is required for a new animal and optional when appending another
clip to an existing one. A different English name creates a separate animal, so
match the existing spelling when appending.

Maintainers without a checkout can run the **Add animal clip** workflow in
GitHub Actions, which takes the same three values as inputs.

## Checks

```bash
python3 -m unittest discover -s scripts/content -p 'test_*.py'
python3 -c "import sys,json;sys.path.insert(0,'scripts/content');from build_content import validate_catalog;validate_catalog(json.load(open('content/catalog.json')))"
npm test && npm run typecheck   # only when app code changed
```

Pushing `content/catalog.json` to `main` runs the content workflow: it downloads
the missing sources, re-encodes them, extracts covers, updates the rolling
`content` release, and commits the regenerated `content/manifest.json`. Do not
edit the manifest by hand.
