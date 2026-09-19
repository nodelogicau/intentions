## Why

The format has a normative README and a first implementation, but no front door: nothing a practitioner can read in five minutes that says what the format is for before they open twelve hundred lines of specification. Particulars has one at particulars.fyi, this format adopts its conventions and composes with it by reference, and v0.1 is about to be declared. The site is what the declaration points at.

## What Changes

- A landing site at **intentions.fyi**, served by GitHub Pages from `docs/` on `main`, in the shape of `particulars/docs`: one hand-written `docs/index.html`, no build step, no JavaScript, no request to any other origin, inline SVG diagrams themed through CSS variables for light and dark.
- The page is a visual introduction, not the specification. The README on GitHub remains the spec and the page's second call to action links to it.
- Hero headline: **"Every hour is for something."** Heidegger's datability said plainly. Sources are credited in muted text under the hero diagram and in the README's References; no philosopher is named in a heading.
- Seven beats: the slot against the triad; "One plan, two fates"; "Whose calendar is it?"; "It ranks. It flags. It never chooses." with a before / the moment / after diagram placing the format between iCalendar and DKF; a proof section drawn from real output; "Start in your terminal"; a footer stating the licences.
- `docs/CNAME` carrying `intentions.fyi` and `docs/README.md` carrying the deploy and DNS notes, as particulars does.
- Two README edits: a one-line pointer to intentions.fyi under the title, and the License section changed from `TBD.` to the particulars wording. The `LICENSE` file is already CC0 1.0 Universal and the CLI is already MIT; only the sentence is missing.
- Outside the repo: Pages settings, DNS at the registrar, and the domain itself if it is not yet held.

## Capabilities

### New Capabilities

- `landing-site`: what intentions.fyi is built from and what it asserts. Single static file, no build, no script, no external request, both colour schemes, the required sections and calls to action, a proof figure regenerable from real CLI output, a footer whose licence statement agrees with the repository, and a README that points at the site and states its licence.

### Modified Capabilities

None. No requirement of the format changes. The page states only what the README's Problem and Approach sections already say.

## Impact

- New `docs/` directory with `index.html`, `CNAME`, `README.md`, a small example workspace and a figure-regeneration script. Two edits to `README.md`. No change to any capability spec and none to the CLI.
- The site is the first public assertion of the licence. The README currently says `TBD.` while the `LICENSE` file says CC0; particulars launched with the same contradiction and had to record a dialectic to fix it. The README catches up before the page goes live.
- The proof figure depends on the `--json` output of intentions-cli v0.9.1. The regeneration command is documented so the figure can be redrawn when the output or the example workspace changes.
- The knowledge workspace gains a claim recording the headline and the register decision, since neither is derivable from the page.
