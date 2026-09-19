#!/usr/bin/env python3
"""Regenerate the proof figure in index.html from the example workspace.

Usage:
    python3 docs/resolution-figure.py [docs/index.html]

Runs the installed `intentions` binary against docs/example with the clock
fixed at the moment the workspace was written, asks it to rank every candidate
placement for the budget intention and to report the workspace's flags, and
rewrites the SVG between the RESOLUTION-FIGURE markers. Nothing else in the
file is touched. Ids are omitted from the rendering; every element carries a
native SVG <title> tooltip with the output it was drawn from. The binary's
version is written into the figure, so a second run with the same binary is
byte-identical and a run with a newer one shows in the diff.
"""
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timedelta
from html import escape

HERE = os.path.dirname(os.path.abspath(__file__))
WORKSPACE = os.path.join(HERE, "example")
NOW = "2026-09-19T09:00:00Z"
BUDGET_TITLE = "Draft the Q4 budget narrative"
BEGIN, END = "<!-- RESOLUTION-FIGURE:BEGIN -->", "<!-- RESOLUTION-FIGURE:END -->"

# geometry
X0, COL_W, Y0, HOUR_H = 58, 104, 46, 26
HOUR_FROM, HOUR_TO = 8, 18
DAYS = 7
GRID_H = (HOUR_TO - HOUR_FROM) * HOUR_H
WIDTH = X0 + DAYS * COL_W + 14
HEIGHT = Y0 + GRID_H + 118
WEEKDAY = ["MO", "TU", "WE", "TH", "FR", "SA", "SU"]


def cli(*args):
    cmd = ["intentions", "--workspace", WORKSPACE, "--json", *args]
    run = subprocess.run(cmd, capture_output=True, text=True)
    if run.returncode != 0:
        sys.exit(f"{' '.join(cmd)}: exit {run.returncode}\n{run.stderr}")
    return json.loads(run.stdout)


def version():
    out = subprocess.run(["intentions", "version"], capture_output=True, text=True).stdout
    m = re.search(r"\d+\.\d+\.\d+", out)
    return m.group(0) if m else "unknown"


def minutes(iso):
    m = re.fullmatch(r"PT(?:(\d+)H)?(?:(\d+)M)?", iso)
    if not m:
        sys.exit(f"unsupported duration {iso}")
    return int(m.group(1) or 0) * 60 + int(m.group(2) or 0)


def by_day(cadence):
    if not cadence:
        return set(WEEKDAY)
    for part in cadence.split(";"):
        if part.startswith("BYDAY="):
            return set(part[6:].split(","))
    return set(WEEKDAY)


def y_of(dt):
    return Y0 + (dt.hour + dt.minute / 60 - HOUR_FROM) * HOUR_H


def short(uri):
    return uri.rstrip("/").rsplit("/", 1)[-1].capitalize()


def main():
    target = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "index.html")
    intentions = cli("intention", "list")["intentions"]
    budget = next(i for i in intentions if i["title"] == BUDGET_TITLE)
    availability = cli("availability", "list")["availability"]
    commitments = cli("commitment", "list")["commitments"]
    titles = {i["id"]: i["title"] for i in intentions}
    titles.update({a["id"]: a["title"] for a in availability})
    titles.update({c["id"]: c["title"] for c in commitments})
    resolved = cli("resolve", budget["id"], "--limit", "500", "--now", NOW, "--timestamp", NOW)
    flags = cli("check", "--now", NOW)["flags"]
    ver = version()

    start_of_range = datetime.fromisoformat(resolved["range"].split(" to ")[0])
    days = [start_of_range + timedelta(days=i) for i in range(DAYS)]
    tz = start_of_range.tzinfo

    out = []
    w = out.append
    w(f'<svg class="min640" viewBox="0 0 {WIDTH} {HEIGHT}" role="img" aria-labelledby="proof-title proof-desc">')
    w('  <title id="proof-title">Every candidate the binary ranked</title>')
    w('  <desc id="proof-desc">A week grid. Shaded bands are the availability the person declared. '
      'A box is a commitment already placed, marked where a party has declined. '
      'Bars are the candidate placements the binary ranked for the budget intention: '
      'solid where the candidate disturbs nothing, dashed where it would displace a commitment the person still holds.</desc>')

    # day headers and hour grid
    w(f'  <text x="{X0 - 8}" y="{Y0 - 22}" text-anchor="end" class="lbl">{days[0].strftime("%B %Y")}</text>')
    for i, d in enumerate(days):
        x = X0 + i * COL_W
        w(f'  <text x="{x + COL_W / 2:.0f}" y="{Y0 - 22}" text-anchor="middle" class="lbl" font-weight="600">{d.strftime("%a %-d")}</text>')
        w(f'  <line x1="{x}" y1="{Y0}" x2="{x}" y2="{Y0 + GRID_H}" class="grid"/>')
    w(f'  <line x1="{X0 + DAYS * COL_W}" y1="{Y0}" x2="{X0 + DAYS * COL_W}" y2="{Y0 + GRID_H}" class="grid"/>')
    for h in range(HOUR_FROM, HOUR_TO + 1):
        y = Y0 + (h - HOUR_FROM) * HOUR_H
        w(f'  <line x1="{X0}" y1="{y}" x2="{X0 + DAYS * COL_W}" y2="{y}" class="grid"/>')
        if h % 3 == 0:
            w(f'  <text x="{X0 - 8}" y="{y + 4}" text-anchor="end" class="small lbl">{h:02d}:00</text>')

    # supply
    for a in availability:
        clock = a.get("window", {}).get("clock")
        if not clock:
            continue
        (h1, m1), (h2, m2) = [map(int, t.split(":")) for t in clock.split("/")]
        y1 = Y0 + (h1 + m1 / 60 - HOUR_FROM) * HOUR_H
        y2 = Y0 + (h2 + m2 / 60 - HOUR_FROM) * HOUR_H
        cond = ", ".join(a.get("conditional", [])) or "anything"
        tip = escape(f'availability: {a["title"]} · {clock} · {a.get("cadence", "every day")} · good for {cond} · capacity {a["duration"]} per occasion')
        for i, d in enumerate(days):
            if WEEKDAY[d.weekday()] not in by_day(a.get("cadence")):
                continue
            x = X0 + i * COL_W
            w(f'  <rect x="{x + 1}" y="{y1:.1f}" width="{COL_W - 2}" height="{y2 - y1:.1f}" class="sup"><title>{tip}</title></rect>')

    # candidate runs
    step = 15
    runs = []
    for c in sorted(resolved["candidates"], key=lambda c: c["start"]):
        s, e = datetime.fromisoformat(c["start"]), datetime.fromisoformat(c["end"])
        key = (s.date(), c["rank"], tuple(c["displaces"]))
        if runs and runs[-1]["key"] == key and (s - runs[-1]["last"]) <= timedelta(minutes=step):
            runs[-1]["last"], runs[-1]["end"], runs[-1]["n"] = s, max(runs[-1]["end"], e), runs[-1]["n"] + 1
        else:
            runs.append({"key": key, "first": s, "last": s, "end": e, "n": 1, "supply": c["supply"]})
    counts = {}
    for r in runs:
        day, rank, displaces = r["key"]
        i = (r["first"].date() - start_of_range.date()).days
        if not 0 <= i < DAYS:
            continue
        x = X0 + i * COL_W + (6 if rank == 1 else 18)
        y1, y2 = y_of(r["first"]), y_of(r["end"])
        cls = "cand1" if rank == 1 else "cand2"
        disturb = "displaces nothing" if not displaces else "would displace " + ", ".join(
            f'{titles.get(d, d)} (still held by the person)' for d in displaces)
        supply = ", ".join(titles.get(s, s) for s in r["supply"])
        tip = escape(f'rank {rank} · {r["n"]} candidate starts from {r["first"]:%H:%M} to {r["last"]:%H:%M} on a 15-minute grid · {disturb} · supply: {supply}')
        w(f'  <rect x="{x}" y="{y1:.1f}" width="9" height="{y2 - y1:.1f}" rx="2" class="{cls}"><title>{tip}</title></rect>')
        counts.setdefault(i, {}).setdefault(rank, 0)
        counts[i][rank] += r["n"]

    # placed commitments and their flags
    for c in commitments:
        s = datetime.fromisoformat(c["placement"]["start"])
        e = s + timedelta(minutes=minutes(c["placement"]["duration"]))
        i = (s.date() - start_of_range.date()).days
        if not 0 <= i < DAYS:
            continue
        x = X0 + i * COL_W + 32
        bw = COL_W - 34
        y1, y2 = y_of(s), y_of(e)
        parties = "; ".join(f'{short(p["uri"])} {p["status"]}' for p in c["parties"])
        own = [f["detail"] for f in flags if f["subject"] == c["id"]]
        tip = escape(f'commitment: {c["title"]} · {s:%a %H:%M}–{e:%H:%M} · {parties}' + (" · flagged: " + " / ".join(own) if own else ""))
        w(f'  <g><title>{tip}</title>')
        w(f'    <rect x="{x}" y="{y1:.1f}" width="{bw}" height="{y2 - y1:.1f}" rx="4" class="placed"/>')
        w(f'    <text x="{x + 4}" y="{y1 + 14:.1f}" class="mono" font-size="10.5">{escape(c["title"].split(" with ")[0])}</text>')
        if own:
            w(f'    <circle cx="{x + bw}" cy="{y1:.1f}" r="7" class="flag"/>')
            w(f'    <text x="{x + bw}" y="{y1 + 4:.1f}" text-anchor="middle" class="flag-t">!</text>')
        w('  </g>')

    # counts under each column
    for i in range(DAYS):
        x = X0 + i * COL_W + COL_W / 2
        y = Y0 + GRID_H + 18
        if i in counts:
            parts = [f'{n} rank {rank}' for rank, n in sorted(counts[i].items())]
            w(f'  <text x="{x:.0f}" y="{y}" text-anchor="middle" class="small lbl">{" · ".join(parts)}</text>')
        else:
            w(f'  <text x="{x:.0f}" y="{y}" text-anchor="middle" class="small lbl">no supply</text>')

    # legend
    ly = Y0 + GRID_H + 52
    w(f'  <rect x="{X0}" y="{ly - 10}" width="18" height="12" class="sup"/>')
    w(f'  <text x="{X0 + 24}" y="{ly}" class="small">declared availability</text>')
    w(f'  <rect x="{X0 + 172}" y="{ly - 10}" width="9" height="12" rx="2" class="cand1"/>')
    w(f'  <text x="{X0 + 188}" y="{ly}" class="small">candidate, disturbs nothing</text>')
    w(f'  <rect x="{X0 + 372}" y="{ly - 10}" width="9" height="12" rx="2" class="cand2"/>')
    w(f'  <text x="{X0 + 388}" y="{ly}" class="small">candidate, would displace a commitment</text>')
    w(f'  <rect x="{X0}" y="{ly + 16}" width="18" height="12" rx="3" class="placed"/>')
    w(f'  <text x="{X0 + 24}" y="{ly + 26}" class="small">commitment already placed</text>')
    w(f'  <circle cx="{X0 + 216}" cy="{ly + 22}" r="7" class="flag"/><text x="{X0 + 216}" y="{ly + 26}" text-anchor="middle" class="flag-t">!</text>')
    w(f'  <text x="{X0 + 231}" y="{ly + 26}" class="small">a party declined: flagged, not decided</text>')
    n = len(resolved["candidates"])
    w(f'  <text x="{WIDTH - 14}" y="{HEIGHT - 8}" text-anchor="end" class="small lbl">{n} candidates considered · drawn by intentions {ver}</text>')
    w('</svg>')
    svg = "\n".join(out)

    html = open(target, encoding="utf-8").read()
    a, b = html.index(BEGIN) + len(BEGIN), html.index(END)
    html = html[:a] + "\n" + svg + "\n" + html[b:]
    open(target, "w", encoding="utf-8").write(html)
    print(f"figure regenerated: {n} candidates, {len(flags)} flags, intentions {ver}")


if __name__ == "__main__":
    main()
