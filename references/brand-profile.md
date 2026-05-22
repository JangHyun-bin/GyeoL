# Brand Profile

Gyeol can use a local brand profile to make repeated work feel consistent without turning every output into the same document.

## Location

Preferred path:

```text
~/.config/gyeol/brand.md
```

Legacy or project-local files may be used only when the user points to them explicitly.

## Priority Order

Apply brand profile data in this order:

1. explicit prompt
2. document judgment
3. source material supplied in the current session
4. brand profile frontmatter
5. brand profile notes
6. built-in defaults

The profile fills gaps. It must not override the user's current request, source facts, or the template's document-specific quality bar.

## Frontmatter Fields

Supported fields:

| Field | Use |
|---|---|
| `name` | Person or organization name for recurring identity. |
| `role` | Default professional role when a personal document needs one. |
| `company` | Organization name for headers or attribution. |
| `email` | Contact detail for letters, resumes, and portfolios. |
| `website` | Contact or brand URL. |
| `github` | Developer profile URL when relevant. |
| `language` | Default language when the prompt is ambiguous. |
| `tone` | Preferred writing tone. |
| `brand_color` | Primary accent color, used only when it fits Gyeol's restrained palette. |
| `page_size` | Default print size when the user gives no size. |
| `currency_locale` | Locale for financial formatting. |

Unknown fields are notes, not instructions. Do not invent template behavior for unknown fields.

## Application Rules

- Use profile values silently when the user request is underspecified.
- Mention the profile only when it materially affects the output or when conflicts need resolution.
- Map `brand_color` to an accent only if contrast stays readable and the color does not break the template's restraint.
- Keep Korean and English phrasing native even when profile notes are written in the other language.
- For resumes, letters, and portfolios, profile identity can fill contact blocks.
- For reports, one-pagers, slides, and landing pages, profile identity can fill author, organization, or brand fields only when the subject is the user's own work.

## Conflict Handling

If the prompt says "formal English" and the profile says `language: ko`, use English. If the source material names a different company than the profile, use the source company for the document subject. If the requested brand color is unsafe or visually incompatible, keep Gyeol defaults and explain the constraint briefly.

## Verification

After using a profile:

- Check that no profile-only fact was turned into a source claim.
- Check that contact fields are present only in document types that need them.
- Check that the result still follows `references/writing.md` and `references/design.md`.

