# Gyeol Premium Hero Lane Design

Date: 2026-05-22

## Goal

Raise Gyeol from a functional skill/template repository into a premium Korean/English enterprise document system. The first proof should not be broad template coverage. It should be a convincing investment/strategy hero lane that makes the repository feel credible within seconds.

The target impression is:

> This is not a generic HTML template pack. This is a Korean/English document system that can produce serious IR, investor memo, research, and strategy documents.

## Positioning

Gyeol should own the lane of Korean/English premium enterprise documents for startups, investment, strategy, hiring, and product teams.

The immediate hero lane is investment/strategy. Hiring and product/sales lanes remain important, but they should follow after the investment/strategy proof pack establishes the visual and editorial bar.

Gyeol should not imitate Kami's parchment/serif identity. Kami already owns that editorial paper feel. Gyeol should develop a Korean enterprise editorial sans direction: restrained, dense, boardroom-ready, and native in both Korean and English.

## Hero Fiction

Use a fictional Korean fabless semiconductor company as the shared subject for the hero samples.

Working company name: `Haneul NPU Systems`

Profile:

- Korean fabless semiconductor company.
- Private-stage company, roughly Series B/C in maturity.
- Written with public-company research-level structure and analytical density.
- Core product: on-device NPU for smartphones and laptops.
- Technical moat: low-power inference chiplet/IP platform.
- Reality level: real industry context, fictional company, fictional metrics.

This lets the samples feel as concrete as a public-company report without requiring current factual claims about a real company.

Every hero sample must mark the company and figures as fictional sample data where appropriate.

## Hero Sample Set

Create four related proof documents from the same fictional company context.

| Sample | Language | Purpose | Default Theme |
|---|---|---|---|
| Korean IR one-pager | Korean | Compressed VC/strategic investor brief | Light |
| English investor memo | English | Global VC or strategic investor memo | Light |
| Equity-style research report | English and Korean variants | Public-market style private-company analysis | Light |
| Strategy deck | Korean primary with English executive summary | Executive/investor meeting deck | Dark preferred, light supported |

The README and public pages should show this pack first. Existing generic Gyeol demos can remain, but they should move below the hero proof pack.

## Design Direction

The design language is Korean enterprise editorial sans.

### Principles

- Use information density instead of decorative complexity.
- Use white or warm off-white surfaces with precise hairlines.
- Use graphite/navy/mineral neutrals with one restrained accent.
- Avoid gradient-driven, card-heavy SaaS decoration.
- Avoid oversized empty cards. Every section should hold a decision, evidence, metric, risk, or source note.
- Use Korean typography that feels native, not like English layouts with Korean words inserted.
- Keep English prose concise and evidence-led.

### Primitive Components

The hero lane should introduce reusable primitives that can later spread to other templates:

- Metric rail
- Investment thesis block
- Decision bar
- KPI table
- Risk matrix
- Roadmap strip
- Comparable-positioning table
- Source note
- Callout / analyst note
- Chart container for later render work

These primitives should be defined in the relevant templates first. A shared abstraction is optional only after duplication becomes painful.

## Theme Policy

Gyeol must support Light and Dark as first-class theme choices.

### Documents

Document/PDF-oriented templates output a fixed theme per artifact:

- `light`
- `dark`

They do not include an in-document browser toggle because PDF/render stability matters more.

Default choices:

- IR one-pager: light
- Investor memo: light
- Equity-style report: light
- Strategy deck: dark is a strong default, light remains supported

### Web Outputs

Landing pages and README/public demo pages may include a browser light/dark toggle.

For web outputs, the toggle should switch between two intentional token sets, not a naive color inversion.

### Agent Behavior

When theme is ambiguous:

- Choose light for print, memo, report, send-as-PDF, and formal investment documents.
- Consider dark for premium, board, keynote, launch, executive preview, and strategy deck requests.
- Ask a short question only when both choices are genuinely plausible and the visual tone matters.

## Implementation Scope

Do not redesign all 18 templates in the first implementation pass.

First pass includes:

- `one-pager` and `one-pager-ko`
- `long-doc` or equivalent investor memo path
- `equity-report` and `equity-report-ko`
- `slides` and `slides-ko`
- `landing-page` and `landing-page-ko`
- demo data for the hero fictional company
- generated hero demos/screenshots
- README showcase update
- checks that preserve the hero proof pack and theme policy

Out of scope for first pass except for shared tokens if unavoidable:

- resume
- portfolio
- letter
- changelog

## Quality Bar

The work is not complete if it only changes colors or adds more cards.

The improved hero lane must satisfy these standards:

- The first screenshot looks like a real investment or strategy artifact, not a template placeholder.
- Korean copy reads like native Korean business writing.
- English copy reads like native investor/business prose.
- Metrics, risks, thesis, roadmap, and source notes appear as structured decision material.
- Dark mode feels premium and intentional, not simply inverted.
- Light mode remains print-friendly.
- Every final demo has no unfilled `{{placeholder}}` fields.
- README shows the investment/strategy proof pack before generic demos.

## Verification Strategy

Add tests before implementation where possible.

Minimum checks:

- Registry still contains the verified template set.
- Hero sample files exist and contain no placeholders.
- Hero screenshots are generated or tracked in the expected location.
- Theme markers exist in upgraded templates, at least `data-theme` or equivalent token evidence.
- Landing page supports a light/dark toggle.
- Document templates do not rely on browser-only toggles for theme selection.
- Existing `python scripts/tests/test_build.py`, `python scripts/build.py --check`, and skill validation pass.

Visual QA should include at least:

- one desktop screenshot for the Korean IR one-pager
- one desktop screenshot for the equity-style report
- one desktop screenshot for the dark strategy deck
- one desktop screenshot for the landing page with toggle visible

## Risks

- Overfitting to one fictional semiconductor story could make Gyeol feel narrow. Mitigation: label it as the first proof lane and keep other lanes listed as next targets.
- Dark mode could harm PDF legibility. Mitigation: keep light as default for print-oriented documents and treat dark as a deliberate theme choice.
- Template complexity could grow too fast. Mitigation: improve the hero lane first; extract shared primitives only after two or more templates need the same code.
- Fictional financial data could look misleading. Mitigation: mark sample data as fictional and avoid references to real company financials.

## Next Step After This Spec

After this design is approved, create an implementation plan that breaks work into testable slices:

1. hero sample data model
2. light/dark token policy
3. one-pager upgrade
4. investor memo/report upgrade
5. deck/landing upgrade
6. demo generation and screenshots
7. README/public showcase update
