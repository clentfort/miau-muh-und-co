import type { LocalClip } from './types';

export const MAX_CLIPS_PER_PLAYBACK = 3;

export function shuffleClips(
  clips: LocalClip[],
  lastPlayedId: string | null,
  random: () => number = Math.random,
): LocalClip[] {
  const shuffled = [...clips];

  for (let index = shuffled.length - 1; index > 0; index -= 1) {
    const otherIndex = Math.floor(random() * (index + 1));
    [shuffled[index], shuffled[otherIndex]] = [shuffled[otherIndex], shuffled[index]];
  }

  if (shuffled.length > 1 && shuffled[0]?.id === lastPlayedId) {
    const replacementIndex = shuffled.findIndex((clip) => clip.id !== lastPlayedId);
    [shuffled[0], shuffled[replacementIndex]] = [
      shuffled[replacementIndex],
      shuffled[0],
    ];
  }

  return shuffled.slice(0, MAX_CLIPS_PER_PLAYBACK);
}

export function normalizeSearch(value: string): string {
  return value
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
    .trim()
    .toLocaleLowerCase('en');
}

export function matchesSearch(name: string, query: string): boolean {
  return normalizeSearch(name).includes(normalizeSearch(query));
}

export function displayName(name: string): string {
  return name.replace(/(^|[\s-])\p{L}/gu, (letter) => letter.toLocaleUpperCase('en'));
}
