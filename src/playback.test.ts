import { describe, expect, it } from 'vitest';

import { displayName, matchesSearch, normalizeSearch, shuffleClips } from './playback';
import type { LocalClip } from './types';

function clip(id: string): LocalClip {
  return {
    id,
    url: `https://example.test/${id}.mp4`,
    sha256: id.repeat(64).slice(0, 64),
    bytes: 1,
    durationMs: 1000,
    localUri: `file:///${id}.mp4`,
  };
}

describe('shuffleClips', () => {
  it('returns at most three distinct clips', () => {
    const selected = shuffleClips(
      ['a', 'b', 'c', 'd'].map(clip),
      null,
      () => 0.5,
    );

    expect(selected).toHaveLength(3);
    expect(new Set(selected.map(({ id }) => id)).size).toBe(3);
  });

  it('does not start with the last displayed clip when alternatives exist', () => {
    const selected = shuffleClips([clip('a'), clip('b')], 'b', () => 0.99);
    expect(selected[0]?.id).toBe('a');
  });

  it('allows the only clip to repeat', () => {
    expect(shuffleClips([clip('a')], 'a')[0]?.id).toBe('a');
  });
});

describe('animal names', () => {
  it('normalizes search terms', () => {
    expect(normalizeSearch('  Gíraffe ')).toBe('giraffe');
    expect(matchesSearch('sea lion', 'LION')).toBe(true);
  });

  it('formats lowercase names for display', () => {
    expect(displayName('red fox')).toBe('Red Fox');
  });
});
