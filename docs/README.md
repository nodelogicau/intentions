# intentions.fyi

The landing page for the Intentions Format: one hand-written HTML file, no
build step, no JavaScript, no external requests. Served by GitHub Pages from
this `docs/` directory on `main`, with the custom domain in `CNAME`.

The page is a visual introduction, not the specification. The README at the
root of this repository is the specification, and the page says nothing it
does not.

## Deployment

Repository settings → Pages: source **Deploy from a branch**, branch `main`,
folder `/docs`, custom domain `intentions.fyi`, **Enforce HTTPS** once the
certificate is issued.

## DNS (Cloudflare, for intentions.fyi)

Apex `A` records, all four GitHub Pages addresses, DNS-only (grey cloud) so
GitHub can issue the certificate:

```
intentions.fyi.  A  185.199.108.153
intentions.fyi.  A  185.199.109.153
intentions.fyi.  A  185.199.110.153
intentions.fyi.  A  185.199.111.153
```

Optional: `www` as a `CNAME` to `nodelogicau.github.io` (GitHub redirects it
to the apex once the custom domain is set).

`blog.intentions.fyi` and every other subdomain are deliberately left free.

## The example workspace

`example/` is a real workspace written by intentions-cli 0.11.0 with the clock
fixed at `2026-09-19T09:00:00Z`. It holds one person's supply for the week of
21 September 2026 (Tuesday and Thursday mornings kept for deep work, weekday
afternoons for anything), a terminus, an intention to send the board pack the
following week, a weekly one-to-one already placed on Tuesday afternoon and
declined by the other party, and the ninety-minute budget intention the site's
prose is about. Nothing in it is hand-edited. It was built with:

```sh
export INTENTIONS_NOW=2026-09-19T09:00:00Z TS=2026-09-19T09:00:00Z
export ADA=https://example.com/people/ada PRIYA=https://example.com/people/priya
intentions init docs/example --author "$ADA" --subject "$ADA" \
  --timezone Australia/Melbourne --hemisphere south
W="--workspace docs/example"
intentions $W availability add --subject "$ADA" --title "Deep-work mornings" \
  --description "Tuesday and Thursday mornings are kept clear for focused work." \
  --calendar 2026-W39 --clock 09:00/12:00 --cadence "FREQ=WEEKLY;BYDAY=TU,TH" \
  --duration PT3H --conditional deep-work --valid-until 2026-W40 --timestamp $TS
intentions $W availability add --subject "$ADA" --title "Weekday afternoons" \
  --calendar 2026-W39 --clock 13:00/17:00 --cadence "FREQ=WEEKLY;BYDAY=MO,TU,WE,TH,FR" \
  --duration PT4H --valid-until 2026-W40 --timestamp $TS
TERM=$(intentions $W intention add --title "Being someone the board can rely on" \
  --stability firm --timestamp $TS --json | jq -r .id)
PACK=$(intentions $W intention add --title "Send the board pack" --duration PT30M \
  --calendar 2026-W40 --serves "$TERM:for-the-sake-of" --timestamp $TS --json | jq -r .id)
ONE=$(intentions $W intention add --title "One-to-one with Priya" --duration PT45M \
  --calendar 2026-09-22 --clock 14:00/15:00 --party "$PRIYA" --timestamp $TS --json | jq -r .id)
intentions $W select $ONE --candidate 2 --timestamp $TS
CMT=$(intentions $W commitment list --json | jq -r '.commitments[0].id')
intentions $W commitment decline $CMT --party "$PRIYA" --timestamp $TS
intentions $W intention add --title "Draft the Q4 budget narrative" \
  --description "Ninety minutes, sometime this week, before the board pack goes out." \
  --duration PT90M --calendar 2026-W39 --activity deep-work \
  --serves "$PACK:in-order-to" --serves "$TERM:for-the-sake-of" --timestamp $TS
```

Re-running that produces a workspace with different ids. The committed one is
the one the figure was drawn from; do not rebuild it to regenerate the figure.
One later edit, with intentions-cli 0.11.1 and the same fixed clock, gave the
one-to-one its chain (`intention edit <id> --serves <terminus>:for-the-sake-of`)
so that every intention reaches the terminus; no candidate changed.

## Regenerating the proof figure

The figure in the proof section is a static SVG rendered from the binary's
own output on `example/`, by `resolution-figure.py`:

```sh
python3 docs/resolution-figure.py
```

The script runs `intentions resolve` and `intentions check` against the
example workspace with the fixed clock above, and rewrites the SVG between
the `RESOLUTION-FIGURE` markers in `index.html`. With the same binary the
result is byte-identical; with a newer binary the version written into the
figure changes, which is the signal to re-read the caption.
