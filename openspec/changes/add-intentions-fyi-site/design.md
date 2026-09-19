## Context

`particulars/docs` is the model: a single 540-line `index.html`, a `CNAME`, a `README.md` with deploy and DNS notes, and one Python script that redraws a proof SVG from real workspace output. No build, no JavaScript, no external request, light and dark through CSS variables, and a plain-English headline with the philosophy carried by the diagram vocabulary rather than by naming Hegel. Its README calls the site "a visual introduction for practitioners" and keeps the spec on GitHub.

This repository's README is the normative specification, twelve hundred lines, with its own Problem and Approach sections, ASCII diagrams of the serves graph and the resolution lifecycle, and a References section crediting Heidegger, Bratman and Searle. The CLI is at v0.9.1 with a Homebrew cask. `.gitignore` excludes `.github/`, so nothing under it is tracked.

## Goals / Non-Goals

**Goals:**
- A page a practitioner reads in five minutes and comes away knowing what a slot is not, what the triad is, who authors a commitment, and that the software never chooses.
- Everything on the page true of the README as it stands, so the page cannot drift into a second specification.
- Deployable by the same steps as particulars.fyi, maintainable without tooling.
- The licence stated publicly, and stated once.

**Non-Goals:**
- Rendering the specification as web pages. The README stays canonical and linked.
- Any client-side behaviour, analytics, fonts, or asset served from elsewhere.
- A blog or subdomain. `blog.intentions.fyi` and `www` stay free, as with particulars.
- A GitHub Actions workflow. Deploy-from-branch needs none, and `.github/` is untracked anyway.

## Decisions

**One file, no build, no JavaScript.** Particulars' constraints carried over unchanged. The page is content, and a single file is the cheapest thing to review through git and the hardest to break. The alternative of an Astro site (the `particulars-website` pattern) buys a blog and a component model that this page does not need.

**A landing page, not a rendered spec.** The README is the format's single source of truth and is already kept honest by OpenSpec change by change. A rendered copy would either drift or need a build step, and both were ruled out above. The second call to action, "Read the spec", links to the repository README.

**The headline is the philosophy said plainly.** Particulars' precedent: "Knowledge that doesn't go stale" names no philosopher, and thesis, antithesis and synthesis live in the hero diagram. Here the load-bearing idea is Heidegger's datability, that every "now" is "now, that…", so the headline is **"Every hour is for something."** A muted line under the hero diagram credits Being and Time §79, matching how particulars mentions Aufhebung once, in passing. "Time is always time for something" is closer to the German and was rejected only because the doubled word fights the eye at display size.

**The register carries through the section headings, unnamed.** Each beat is one source's idea in plain words: "One plan, two fates" (spannedness against clock time), "Whose calendar is it?" (das Man against resoluteness, without the word "authentic", which reads as moralising), "It ranks. It flags. It never chooses." (Searle: a speech act with no speaker is no act). "Projection" stays off the page in the Heideggerian sense because the format already uses the word for the versioned hash. Entwurf is never mentioned.

**Seven beats, in this order.**
1. Hero: eyebrow, headline, lead, two calls to action, and the slot-against-triad diagram: `DTSTART`/`DTEND` on the left, `DURATION` · `WINDOW` · `INTENTION` on the right, the intention serving upward to a standing self-understanding.
2. "One plan, two fates": the README's own example, ninety minutes on the budget, sometime this week, before the board pack goes out. Fate one is the tentative block on Tuesday at two, moved four times. Fate two is an intention that resolves when it must and not before. Then a kicker and three cards for what existing tools do instead (the slot, the task list, the scheduling assistant).
3. "Whose calendar is it?": every object says who wrote it; a harness may draft but only the person makes an intention firm; a party's status changes only by that party's act.
4. "It ranks. It flags. It never chooses.": resolution → ranked candidates → the person's act → a commitment; flags are surfaced, never decided. Beneath it, the composition diagram: before the moment (Intentions), the moment (iCalendar / JSCalendar, linked from the COMMITMENT), after the moment (DKF, a claim citing the object at a version). This is also the page's link to particulars.fyi.
5. Proof (see below).
6. "Start in your terminal": the cask install, `init`, an intention, an availability, `resolve`, `select`; then the three links (the specification, the CLI, the release) and a status line naming what exists today.
7. Footer: the same sentence as particulars with the names swapped.

**Recurrence is not a beat in this version.** "Nothing recurs. It comes back." is a good line and Wiederholung is real in the spec, but it adds a sixth mechanism to a page that already carries four. Kept as a candidate for a later change.

**The proof section shows real output on a public workspace.** Three options were weighed. The second-reader story (intentions-cli written from the text, thirteen issues raised, all settled, four differently from what it chose) is true and needs no script, but it is a paragraph, not a figure. The DKF reasoning chain from `intentions-knowledge` could reuse `proof-graph.py` almost as-is, but it would show particulars on the intentions site. A real resolution is native to the format: one intention, two availabilities, the ranked candidates with their displacement costs, and the flag. The private personal workspace cannot be used, so the figure is drawn from a small example workspace committed under `docs/example/`, run through the released binary. That is a stronger claim than particulars could make: the reader can clone the workspace and reproduce the figure. The second-reader story becomes the section's lead paragraph, so the section has both the fact and the figure.

**The figure is generated, not drawn.** `docs/resolution-figure.py` reads `intentions resolve --json` output from the example workspace and rewrites the figure's SVG in `index.html` between marker comments, as `proof-graph.py` does. The command is recorded in `docs/README.md` and in the HTML comment at the top of the file. Ids are omitted from the rendering.

**Two sites, siblings not twins.** The same neutrals, type scale, section rhythm and SVG class vocabulary as particulars, so the two pages are recognisably from one hand, with a different accent hue so they are not confused. The palette is fixed during implementation and recorded in the file's `:root`.

**The README catches up on licence before launch.** The `LICENSE` file is CC0 1.0 Universal and the CLI's is MIT, so the README's `TBD.` is replaced with the particulars sentence: the specification is released under CC0 1.0 Universal, reference implementations under the MIT License. The footer then states what the repository already says, and there is one source for the claim.

**Deploy from branch.** Repository settings, Pages, source "Deploy from a branch", `main`, `/docs`, custom domain `intentions.fyi`, enforce HTTPS once the certificate is issued. DNS is the four GitHub Pages apex `A` records and `www` as a `CNAME` to `nodelogicau.github.io`.

## Risks / Trade-offs

- [The page and the README disagree] → The page states nothing the Problem and Approach sections do not. It names no field and no vocabulary value. A verification task reads the page against the README before launch, and the archive step records the page in the knowledge workspace so a later spec change knows to re-read it.
- [The CLI's `--json` shape changes and the figure goes stale] → The script and the example workspace are committed; regeneration is one command; the figure's caption carries the CLI version it was drawn from.
- [The domain is not held] → Nothing on the page depends on the domain except `CNAME`. The page can be reviewed at the `github.io` address while registration completes.
- [A public licence statement precedes v0.1] → The licence is a fact about the repository today, not about the version. The statement is the same either way.
- [The headline is a philosophical claim a reader may not share] → It is also the format's founding claim, stated in the README's second paragraph. A reader who rejects it should reject the format, and the page lets them do so in one line.
- [Hand-drawn SVG is slow to change] → Accepted, as particulars accepted it. The page has five diagrams and changes rarely.

## Migration Plan

1. Merge `docs/` and the README edits to `main`.
2. Pages settings as above; confirm the `github.io` address serves the page.
3. DNS at the registrar; wait for the certificate; enforce HTTPS.
4. Announce nowhere until the licence line and the footer are checked against each other.

Rollback is removing the custom domain in Pages settings; the repository is unaffected.

## Open Questions

- Is `intentions.fyi` registered and at which registrar? Step one of deployment if not.
- Does the "Start" section's status line say v0.1, or wait for the declaration? The page can launch saying "an early draft, with a first implementation" and be edited the day v0.1 is declared.
- The accent hue.
