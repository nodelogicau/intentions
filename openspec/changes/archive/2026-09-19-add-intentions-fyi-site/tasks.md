## 1. Settle what the page will assert

- [x] 1.1 Confirm whether intentions.fyi is registered and where; register it if not
- [x] 1.2 README License section: replace `TBD.` with the particulars sentence (specification CC0 1.0 Universal, reference implementations MIT)
- [x] 1.3 README: add the one-line pointer to intentions.fyi under the title, worded as particulars' README words its own
- [x] 1.4 Choose the accent hue and record the full palette for both schemes

## 2. The example workspace and the figure script

- [x] 2.1 Create `docs/example/` with `intentions init`, one intention (the ninety-minutes example), two availabilities, and one imported commitment that produces a clash
- [x] 2.2 Run `intentions resolve --json` with v0.9.1 and confirm the output carries ranked candidates with displacement and the flag
- [x] 2.3 Write `docs/resolution-figure.py`: read the JSON, emit the SVG between marker comments in `index.html`, omit ids, use the shared SVG class vocabulary
- [x] 2.4 Confirm a second run is byte-identical

## 3. The page

- [x] 3.1 `docs/index.html` skeleton: head, `:root` palette and dark override, type scale, section rhythm and SVG class vocabulary carried over from particulars
- [x] 3.2 Hero: eyebrow, "Every hour is for something.", lead, two calls to action, slot-against-triad SVG, muted source credit
- [x] 3.3 "One plan, two fates": the two-fates SVG, the kicker, the three cards
- [x] 3.4 "Whose calendar is it?": prose and the authorship SVG (harness drafts, person firms, party sets own status)
- [x] 3.5 "It ranks. It flags. It never chooses.": the resolution SVG, then the before / the moment / after composition SVG with the link to particulars.fyi
- [x] 3.6 Proof: the second-reader lead paragraph, the generated figure between markers, caption with CLI version and date
- [x] 3.7 "Start in your terminal": install and first-run commands, the three links, the status line
- [x] 3.8 Footer with the licence sentence
- [x] 3.9 Top-of-file HTML comment recording how the figure is regenerated

## 4. Supporting files

- [x] 4.1 `docs/CNAME` containing `intentions.fyi`
- [x] 4.2 `docs/README.md`: purpose, Pages settings, DNS records, `www` note, subdomains left free, figure regeneration command

## 5. Verify

- [x] 5.1 No `<script`, no external stylesheet, font, image or `@import`; one request in the network inspector
- [x] 5.2 Both colour schemes, every diagram legible in each
- [x] 5.3 Phone width: no horizontal page scroll, diagrams scroll within their wrap
- [x] 5.4 Every link resolves: spec README, CLI repo, release, particulars.fyi, `#start`
- [x] 5.5 Read every sentence of prose against the README's Problem, Approach and Status sections; the page names no field, value or flag kind
- [x] 5.6 Footer licence sentence agrees with both `LICENSE` files and the README License section

## 6. Deploy and close out

- [x] 6.1 Commit `docs/` and the README edits; push
- [x] 6.2 Pages settings: deploy from `main`, folder `/docs`; confirm the `github.io` address serves the page
- [x] 6.3 DNS: four apex `A` records and `www` CNAME; wait for the certificate; enforce HTTPS
- [x] 6.4 Knowledge workspace: a claim recording the headline, the register decision, and the proof-section choice; commit and push
- [x] 6.5 Archive the change with sync so `landing-site` lands in the main specs
