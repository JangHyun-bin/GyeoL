# Design System

Gyeol is a sans-first enterprise document system for Korean and English.

## Principles

- Use white or near-white mineral surfaces.
- Use near-black text, muted slate secondary text, and a single action blue.
- Use deep green-black or dark navy for strong bands.
- Use hairlines, spacing, and type scale instead of heavy shadows.
- Keep cards at 4px or 8px radius unless a media frame needs more.
- Keep documents denser than public-site sections.

## Typography

Use a Korean/English sans stack first:

```css
font-family: Pretendard, "Noto Sans KR", Inter, system-ui, sans-serif;
```

Use JetBrains Mono for code, command labels, and narrow technical metadata.

## Color Tokens

- Canvas: `#ffffff`
- Mineral: `#f4f3ee`
- Ink: `#17171c`
- Slate: `#61616f`
- Hairline: `#dedee6`
- Dark band: `#071829`
- Deep green: `#003c33`
- Action blue: `#1863dc`
- Coral: `#ff7759`, limited use only

## Light / Dark Theme Policy

Document templates use a fixed `data-theme` value per artifact. They may expose `{{theme}}`, but they do not include a browser toggle. Landing pages may include a browser toggle because they are screen-first outputs.

Light theme is the default for IR one-pagers, investor memos, reports, and PDF-oriented work. Dark theme is preferred for strategy decks, launch pages, board previews, and executive presentation surfaces.

Dark mode is not an inversion. It uses a deep graphite/navy canvas, warm foreground text, restrained blue or semiconductor green accents, and visible hairlines.
