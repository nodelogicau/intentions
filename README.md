# Intentions Format

An open format for what a person means to do with their time: intentions with
a duration and a window rather than a slot, availability as the supply those
intentions draw on, and commitments only where another party is involved.
Designed to be written and read by AI harnesses, reviewed by people through
git, and to compose with iCalendar and with the Dialectical Knowledge Format
by reference rather than by shared schema.

**[intentions.fyi](https://intentions.fyi)** — a visual introduction for
practitioners.

---

## The Problem

Every mainstream calendar format models time the same way: a homogeneous
sequence of interchangeable slots, each with a start and an end, into which
events are placed. iCalendar's `DTSTART`/`DTEND`, JSCalendar's `start`/
`duration`, and every scheduling assistant built on them share this picture.
It is the right picture for the moment two people must meet, and the wrong
picture for nearly everything before that moment.

Before a meeting is fixed, what a person actually has is not a slot. It is
something like *ninety minutes on the budget, sometime this week, before the
board pack goes out*. The duration is known, the window is known, the reason
is known, and the slot is not. A slot-based calendar has no way to hold that
without inventing a slot, which is why the tentative block appears on Tuesday
at two, gets moved four times, and ends up telling nobody anything.

Heidegger called the homogeneous-slot picture *clock time*: a levelled-off
succession of now-points, derivative of a more basic experience in which every
time is dated by what it is for and stretched across a span. Bratman, from a
different tradition, described intentions as partial plans: future-directed,
conduct-controlling, resistant to casual reconsideration, filled in
incrementally, and required to be consistent with each other. Neither picture
has a representation in any calendar format. Both are what a person is doing
when they plan.

The second problem is authorship. The same calendar can be the scaffold of a
person's own resolve or an accretion of other people's claims on their time,
and the artifact looks identical either way. A format that cannot say who
authored a commitment cannot help a person tell the difference.

---

## The Approach

The format replaces the slot with a triad: a **DURATION** (how long), a
**WINDOW** (within what bounds, expressed as the person expressed it and never
flattened to clock time until it must be), and an **INTENTION** (what this is
for, as a graph of in-order-to references that terminates in a standing
self-understanding about who the person is). Recurrence lives on the
intention, not the window: a weekly one-to-one is a recurring intention that
generates fresh instances, each its own object with its own life.

**AVAILABILITY** is the supply side: a standing statement that some particular,
a person or a room or a piece of equipment, has capacity of a kind within a
window. It is assertive where intention is commissive, so it is a different
object with a different lifecycle, including a validity horizon after which it
must be reconfirmed.

**RESOLUTION** matches an intention's demand against the availability of every
required particular and produces a ranked set of candidate placements, ordered
by how much existing intention each would disturb. It never chooses. Selection
is a recorded act by the person, or by a policy the person holds.

**COMMITMENT** is the interpersonal object: parties, a placement, a deontic
status per party that only that party's act may change, and the single link to
an external iCalendar or JSCalendar object. A commitment arises either from a
resolution, in which case it is consistent by construction, or by import, in
which case it is expected to clash with what the person meant and the clash is
surfaced as a flag. Flags are never decisions.

Everything is a YAML file in a git repository. Objects are live state edited in
place; the events that happen to them (resolution, acknowledgement, retirement)
are append-only records. Every object and record says who wrote it. A
retrospective account of what actually happened is not this format's job: a
DKF claim may cite any object here by id and version, and that is the whole of
the relationship.

---
## Core Object Types

The format defines three object types, INTENTION, AVAILABILITY, and
COMMITMENT, which are live state and are edited in place; three record types,
RESOLUTION, ACKNOWLEDGEMENT, and RETIREMENT, which are events about objects
and are append-only; and three embedded values, DURATION, WINDOW, and
PLACEMENT, which have no identity of their own. Everything else is
implementation.

### Identifiers

Every object and standalone record id is `<prefix>_` followed by a lowercase
canonical UUID version 7 ([RFC 9562](https://www.rfc-editor.org/rfc/rfc9562)):

| Prefix | Type |
|---|---|
| `int_` | intention |
| `avl_` | availability |
| `cmt_` | commitment |
| `res_` | resolution record |

Embedded records (acknowledgement, retirement) and embedded values carry no id.
UUIDv7 is time-ordered, so a directory listing is a chronological log.
Implementations MUST mint with a monotonic counter so that ids created within
the same millisecond still sort in creation order. Ids are immutable and remain
resolvable for the life of the workspace, including after retirement.

### Field order

The order in which fields are shown for each type below is that type's
canonical order, and `version` always comes second, after `id`. Writers emit
fields in that order; readers MUST accept any order and MUST NOT reject a file
for its arrangement. Fields an implementation adds beyond this specification
are written after all specified fields. Lists of strings (`location`,
`conditional`, an intention's `parties`, `displaced`) are block sequences,
sorted as in the projection; small records (`serves` entries, ranged
durations, `gap`, policy conditions) are flow mappings; multi-line prose is a
literal block scalar; everything else is block style. A boolean equal to its
documented default is omitted. Canonical order and style are what make two
implementations produce byte-identical files for identical state, which is
what makes a workspace reviewable as a diff.

### Source and timestamp

Every object and record carries a `source` block and a `timestamp`:

```yaml
source:
  author: https://example.com/people/ada   # who this is on behalf of
  harness: claude                          # optional: the agent harness
  model: claude-fable-5-1                  # optional: the model
timestamp: 2026-09-04T09:12:00Z            # assertion time, RFC 3339 UTC
```

`author` is required on an intention and on an availability. Both are speech
acts, one commissive and one assertive, and a speech act with no speaker is
not one. A harness alone can observe; it cannot intend. On records, `source`
says which hand performed the act, which is distinct from whose will it
expressed (see `selector` under RESOLUTION).

Source is not bookkeeping here. The founding observation of this format is
that the same schedule is a person's own resolve or an imposition depending on
who authors it. `source` is the only field that lets the format tell those
apart, and it is why a harness may draft an intention but may not make it
`firm` without a policy the person holds.

The timestamp may precede the minting instant embedded in the id, and
consumers MUST NOT require the two to agree. Neither `source` nor `timestamp`
is part of any scheduling projection: correcting who wrote something or when
does not change what it clashes with.

### `INTENTION`

What a person means to do. It involves no other party; when it must interlock
with someone else it produces a COMMITMENT through resolution.

```yaml
id: int_01a06d10-4c2e-7a91-b3f0-2d8e1a7c5b44
version: sha256:7c3a…d18e
subject: https://example.com/people/ada
title: Draft the Q4 budget narrative
description: |
  Two focused sessions should be enough; the numbers are already in.
duration: PT90M
window:
  calendar: 2026-W37
  relative:
    target: int_01a06cf2-8e11-7b3a-9c7d-4f0a2b6e8d13
    relation: FINISHTOSTART
    gap: {min: P0D, max: P3D}
stability: tentative
activity: deep-work
location:
  - https://example.com/places/home
serves:
  - {id: int_01a06cf2-8e11-7b3a-9c7d-4f0a2b6e8d13, role: in-order-to}
  - {id: int_01a05a00-1111-7000-8000-000000000001, role: for-the-sake-of}
source:
  author: https://example.com/people/ada
  harness: claude
  model: claude-fable-5-1
timestamp: 2026-09-04T09:12:00Z
acknowledgements: []
```

Fields, in canonical order:

| Field | Required | Meaning |
|---|---|---|
| `id` | yes | |
| `version` | yes | The projection hash, written by every writer; the computed value is authoritative. |
| `subject` | on disk | URI of the particular whose intention this is. The writer applies `defaults.subject` from `intentions.yaml` when the caller omits it; a workspace without a default requires it explicitly. |
| `title` | yes | Prose. |
| `description` | no | Prose. |
| `duration` | no | A DURATION. Required before the intention can be resolved. |
| `window` | no | A WINDOW. Required before the intention can be resolved. |
| `stability` | yes | `tentative` or `firm`. |
| `firmed_under` | no | The policy under which a harness set `firm`. Required whenever `stability` is `firm` and `source` carries a harness; absent when a person firmed by their own act. |
| `activity` | no | A term from the workspace's activity vocabulary, matched against availability `conditional`. |
| `location` | no | URIs at one of which this must happen. Absent means anywhere. |
| `parties` | no | URIs of other particulars whose availability must be satisfied, where the workspace tracks it. |
| `serves` | yes | Outbound references, possibly empty: `{id, role}` with role `in-order-to`, `for-the-sake-of`, or `instance-of`. |
| `cadence` | no | An RRULE. Makes this a recurring intention; the window must then carry a calendar anchor. |
| `occurrence` | no | On generated instances only: the EDTF granule the cadence produced. |
| `placement` | no | A PLACEMENT, written only by resolution. |
| `preference` | no | `earliest`, `latest`, `adjacent`, or `spread`. |
| `auto_select`, `auto_firm` | no | On termini only: policy conditions. |
| `reference` | no | Informal pointer to a DKF claim; never resolved by validation. |
| `source`, `timestamp` | yes | |
| `acknowledgements` | yes | Append-only list, possibly empty. |
| `retired` | no | At most one RETIREMENT record. |

**Stability.** A firm intention is costly to reconsider; a tentative one is
cheap. Resolution ranks candidate placements by that cost. `firm` may be set
only by an act whose `source` carries no `harness`, or by a harness acting
under a policy of the subject whose `auto_firm` condition the intention
satisfies, in which case the write sets `firmed_under` to that policy's id.
The field is provenance, like `source`, and is outside the projection; it is
required whenever a firm intention's `source` carries a harness, so that
validation can tell an authorised firming from a forged one after the fact.
Whether the condition held is checked at write time only, since the intention
may legitimately change afterwards. A harness may draft; it may not resolve
on the person's behalf.

**The serves graph.** `in-order-to` links an intention to another it is a means
to. `for-the-sake-of` links an intention to its terminus: an intention with
no window, no duration, and no outbound references, such as *being someone
who follows through*, which may carry an informal `reference` to a DKF claim
the person holds about themselves. Where this text says *standing intention*
it means a terminus, never a recurring one. `instance-of` links a generated
instance to the recurring intention that produced it. The graph is directed and
acyclic but not a tree: an intention may serve several ends and several may
converge on one. Only these three roles are admitted; temporal relations
belong to WINDOW, never to `serves`.

**Recurring intentions and instances.** An intention with a `cadence` is a
recurring intention; its window carries a calendar anchor for the cadence to
expand within, and it generates instances: new intention objects carrying
`instance-of`, an `occurrence`, a window whose calendar anchor is that
occurrence and whose clock anchor is the recurring intention's, and the
recurring intention's subject, duration, activity, location, and parties
unless overridden. Instances are materialised by an explicit `generate`
operation over `resolver.horizon`, the one planning horizon resolution also
uses, and are written to disk immediately so that flags and
acknowledgements have something to attach to. Generation is idempotent on
`(recurring, occurrence)`. Retiring one instance skips one occasion; retiring
the recurring intention ends the arrangement and leaves already-generated
instances to be retired individually.

**Policies.** A policy is a terminus carrying `auto_select` or `auto_firm`,
each a condition with terms `max_duration` and `stability`. A condition is
satisfied when every term it states holds for the intention being acted on.
Conditions are admitted on termini only: an intention with a window, a
duration, or any `serves` entry may not carry them, because a scheduled thing
must not be able to authorise a firming. These are the only means by which a
harness may select a candidate or set `firm` without a person's direct act. A
policy is itself an intention the person holds, so the will that acts is
still theirs.

**Location.** A place is a URI the person chooses, matched by exact equality:
a room, a house, a city, a meeting link. The format owns no hierarchy of
places and requires no coordinates; what a URI denotes is a fact about the
URI. A `geo:` URI is admitted, and it is to place what a clock bound is to
time. A room that must be booked and is also where the thing happens appears
in both `parties` and `location`: one consumes supply, the other constrains
placement.

**Scheduling projection:** `subject`, `duration`, `window`, `stability`,
`activity`, `location`, `parties`, `serves`, `cadence`, `occurrence`,
`placement`, `retired.kind`. Neither `version` nor `firmed_under` is in it.

### `AVAILABILITY`

A standing statement that some particular has capacity for a kind of
engagement within a window. Any absolute URI may be a subject: a person, a
room, a vehicle, a shared instrument. The format does not require the subject
to exist in any registry.

```yaml
id: avl_01a06d12-9b7e-7c03-a5d1-6e2f4a8b0c77
version: sha256:2e91…a47b
subject: https://example.com/people/ada
title: Tuesday mornings for deep work
duration: PT3H
window:
  calendar: 2026-09/2026-12
  clock: 09:00/12:00
conditional:
  - deep-work
  - writing
location:
  - https://example.com/places/home
cadence: FREQ=WEEKLY;BYDAY=TU
valid_until: 2026-12
scope: personal
source:
  author: https://example.com/people/ada
timestamp: 2026-09-04T09:20:00Z
```

Fields, in canonical order:

| Field | Required | Meaning |
|---|---|---|
| `id` | yes | |
| `version` | yes | The projection hash. |
| `subject` | yes | URI of the particular whose availability this is. |
| `title`, `description` | no | Prose. |
| `duration` | yes | Capacity offered per occasion, optionally ranged. May be shorter than the window's clock interval. |
| `window` | yes | A WINDOW. |
| `conditional` | no | Activity terms this supply is good for. Absent means anything. |
| `location` | no | URIs at which this capacity holds. Absent means anywhere. |
| `cadence` | no | An RRULE. Makes this recurring. |
| `valid_until` | no | EDTF expression or datetime. See validity horizon. |
| `scope` | yes | `personal`, `organisation`, or `public`. Only ever widened. |
| `source`, `timestamp` | yes | |
| `retired` | no | At most one RETIREMENT record, kind `retracted` or `superseded`. |

**Conditional is a filter, not a reason.** It constrains which intentions this
supply may serve, by exact match on `activity`. It carries no chain of reasons
and never references the intention graph.

**Location is the second filter.** An availability with `location` supplies an
intention only if the intention has no `location` or the two lists share a
URI. Place rides on the availability that offers the capacity: *Tuesdays at
home for deep work* is one object. Supply for a subject is the union of their
availabilities, and two overlapping capacities at different places are
alternatives, not a contradiction. Whereabouts has the opposite rule: where a
person will be narrows every candidate it covers. That is a different object,
not a different rule for this one, and it is not in this version (see
[Status](#status)). Until it is, a location-free capacity supplies an at-home
intention on a day the person is away, and nothing flags it.

**Capacity is consumed.** Each occasion offers its `duration` (the `max`
when ranged), less the opaque, unretired placements already resting on it. Two
two-hour intentions cannot both land on one three-hour morning. A commitment
consumes a party's capacity only where that party is `tentative` or
`accepted`. An intention's placement and the commitment created from it count
once against the subject, and that placement consumes whatever the subject's
party entry says. A transparent commitment consumes nothing.

**Scope has a subject.** `personal` availability is supply only for an
intention whose subject, or one of whose parties, is the availability's
subject. `organisation` and `public` availability are visible to any resolver
whose `resolver.scope` is at or narrower than theirs. So in an organisation
workspace Priya's personal Tuesdays are never Ada's supply unless Priya is a party
to what she is placing.

**No instances.** Recurring availability is one object re-evaluated at
resolution time. A standing disposition is not an act and needs no
per-occasion retrieval.

**Validity horizon.** A capacity can silently stop being true with no
triggering event. One-off availability expires with its window. Recurring
availability without an explicit `valid_until` is treated as valid until its
`timestamp` plus the workspace's `availability.default_horizon`; the
recommended default is one quarter, `P13W`. Past the horizon the availability
is unusable as supply, not false: any commitment resting on it carries an
`expired-ground` flag, and reconfirmation is an edit to `valid_until`. The
horizon is checked at resolution and consistency time, never by a background
sweep.

**Renewal versus supersession.** Renewing is an edit to `valid_until` on the
same object. Changing the window, duration, conditional, or location is a different
disposition: a new object, with the old one retired as `superseded` pointing at
it. A tool refuses an edit that changes those terms in place.

**Scheduling projection:** `subject`, `duration`, `window`, `conditional`,
`location`, `cadence`, `valid_until`, `retired.kind`.

### `COMMITMENT`

The interpersonal object, and the only one that touches an external calendar.
An intention becomes a commitment when it must interlock with another party.

```yaml
id: cmt_01a06d15-3f8a-7d61-8c2b-9a4e6f1d3b05
version: sha256:b60f…3c1d
parties:
  - uri: https://example.com/people/ada
    status: accepted
  - uri: https://example.com/people/priya
    status: tentative
  - uri: https://example.com/rooms/3
    status: accepted
placement:
  start: 2026-09-15T10:00:00+10:00
  duration: PT1H
  location: https://example.com/rooms/3
intention: int_01a06d10-4c2e-7a91-b3f0-2d8e1a7c5b44
origin:
  resolution: res_01a06d14-7e2c-7b19-a0d3-5c8f2e4a6b91
external:
  system: jscalendar
  uid: 2a6f0b3e-4d1c-4e8a-9b7f-0c5d3e2a1f44
title: Budget narrative review
source:
  author: https://example.com/people/ada
  harness: claude
timestamp: 2026-09-08T14:02:00Z
acknowledgements: []
```

Fields, in canonical order:

| Field | Required | Meaning |
|---|---|---|
| `id` | yes | |
| `version` | yes | The projection hash. |
| `parties` | yes | `{uri, status}` per party, sorted by `uri`; status `tentative`, `accepted`, or `declined`. |
| `placement` | yes | A PLACEMENT. Commitments always have one. |
| `intention` | no | The intention this fulfils. Absent on imports. |
| `origin` | yes | `{resolution: res_…}` or `import`. |
| `transparent` | no | `true` means this occupies none of the subject's time. Absent means `false`, and a writer omits it when false. Only an import may set it. |
| `external` | no | `{system: icalendar or jscalendar, uid}`. The only link to an external calendar. |
| `title`, `description` | no | Prose. |
| `source`, `timestamp` | yes | |
| `acknowledgements` | yes | Append-only list. |
| `retired` | no | At most one RETIREMENT record, kind `cancelled`. |

**Two origins.** A commitment from a resolution is consistent with availability
and intention by construction. A commitment from import is not: external
calendars have no concept of availability and cannot respect it, so an
imported commitment is expected to clash with what the person meant. It is
created exactly as the import states it and the clash is surfaced as a flag.
An import creates one commitment per occurrence brought in, sharing the
external `uid`, and never creates an intention or an availability.

**Party status is that party's act.** A status changes only through an explicit
act attributed to the party: the workspace owner's own action for their entry,
an imported iTIP reply for another's. No resolution, consistency check, flag,
or policy changes a status. A commissive status requires sincerity, and
software cannot supply it.

A status also decides whose time this occupies. The commitment occupies a
party's time, consuming their capacity and standing to be displaced by their
resolutions, exactly where that party's own entry is `tentative` or
`accepted`. A party at `declined` is not occupied by it, and one party's
decline changes nothing for the others, whose commitment still stands. A
calendar that kept charging someone for a claim they refused would be the
imposition this format exists to surface. Where the commitment fulfils an
intention, that intention's placement occupies its subject's time on its own,
so a decline by the subject frees nothing while the placement stands: the
two disagree, and the disagreement is a `party-declined` flag.

**Cancellation** appends a RETIREMENT record of kind `cancelled`. It does not
retire the intention; the intention's placement is cleared so it may be
resolved again.

**External reference only.** Recurrence, timezone definitions, alarms, attendee
delegation, and iTIP negotiation stay in the external system. Nothing of them
is copied here. The one exception is place: a JSCalendar `locations` or
`virtualLocations` entry with a URI, or an iCalendar `LOCATION` that is a URI,
becomes `placement.location` on import and is written back on export.
Free-text locations are dropped. Two more properties cross: iCalendar
`TRANSP:TRANSPARENT` or JSCalendar `freeBusyStatus: free` becomes
`transparent: true` and is written back on export, an absent `TRANSP` being
opaque; and a `DTSTART` of value type `DATE`, or JSCalendar `showWithoutTime`,
becomes an all-day placement and is written back in that form.

**Transparency.** A commitment from a resolution consumed supply to exist and
is opaque by construction; `transparent: true` on it is a validation error.
Transparency arrives only from outside, as a conference week or a colleague's
leave that shares the calendar without claiming the person's time. Where the
subject will be, as their own statement, is presence (see [Status](#status)),
not a transparent intention.

**Scheduling projection:** `parties`, `placement`, `intention`, `origin`, `transparent`,
`external`, `retired.kind`.

### Records

Objects are edited in place. What happens to them is recorded, never edited.
One record type stands alone because it relates several objects and recurs;
two are embedded because each is about exactly the object it sits in.

#### `RESOLUTION`

The act of selecting one candidate placement for an intention. Resolution the
operation produces a ranked candidate set; the record is written only when
someone chooses.

```yaml
# resolutions/res_01a06d14-7e2c-7b19-a0d3-5c8f2e4a6b91.yaml
id: res_01a06d14-7e2c-7b19-a0d3-5c8f2e4a6b91
version: sha256:e4a2…917c
intention: int_01a06d10-4c2e-7a91-b3f0-2d8e1a7c5b44
placement:
  start: 2026-09-15T10:00:00+10:00
  duration: PT1H
selector: person
candidates_considered: 4
displaced:
  - int_01a06c88-2b5d-7f40-9e17-3a6c8d0b2e59
supply:
  - avl_01a06d12-9b7e-7c03-a5d1-6e2f4a8b0c77
presumed:
  - mailto:someone@another-company.example
source:
  author: https://example.com/people/ada
timestamp: 2026-09-08T14:02:00Z
```

`selector` is `person` or the id of the policy whose `auto_select` condition
authorised automatic selection. `selector` says whose will chose;
`source` says which hand performed it. A harness selecting under a policy
carries the policy in `selector` and itself in `source.harness`. `supply`
names the availabilities the placement was chosen against: what the selector
saw, kept outside the projection. It is not what the placement rests on now,
which consistency recomputes from the current workspace. `presumed` names the
parties that contributed no supply because the workspace does not track them,
so a reader sees whose time the placement assumes without evidence. Both are
provenance and neither is in the projection.

On selection the intention gains the placement. If the intention has
`parties`, a COMMITMENT is created with every party, the subject included, at
`tentative`. Anything the placement displaces is listed and flagged; it is not
retired, moved, or changed.

Selecting for an intention that already has a placement is refused unless the
caller asks to replace. Replacing clears the old placement, writes the new one,
and adds a new record; the old record stays. A live commitment resting on the
old placement is cancelled, with the new resolution's id as the reason, and a
fresh one is created with every party tentative, because a placement its
parties accepted cannot move under them.

**Scheduling projection:** `intention`, `placement`, `selector`, `displaced`.

#### `ACKNOWLEDGEMENT`

An entry in the `acknowledgements` list of an intention or commitment, saying
that the person has seen a specific flag against a specific state of a
specific counterpart and is proceeding anyway.

```yaml
acknowledgements:
  - kind: window-clash
    counterpart: int_01a06c88-2b5d-7f40-9e17-3a6c8d0b2e59
    counterpart_version: sha256:9f2c…e41a
    reason: The review matters more than the reading block this week.
    source:
      author: https://example.com/people/ada
    timestamp: 2026-09-08T14:05:00Z
```

The list is append-only and may be appended to even after the object is
retired. A flag is suppressed while an acknowledgement matches its kind,
counterpart, and the counterpart's current version; when the counterpart's
projection changes the acknowledgement lapses, the flag returns, and the old
entry stays. The person acknowledged a state of affairs, not any future one.
Acknowledgements are excluded from the projection.

An acknowledgement carries everything a later DKF claim needs to say what was
decided and why, citing the object by id and version. This format does not
write that claim.

#### `RETIREMENT`

A single `retired` block appended to an object. Active is the absence of the
block; there is no status field.

```yaml
retired:
  kind: superseded
  reason: Split into two shorter sessions after the scope changed.
  superseded_by: int_01a06d20-5a3b-7e88-b1c4-7d9e0f2a4c66
  source:
    author: https://example.com/people/ada
  timestamp: 2026-09-10T08:30:00Z
```

Kinds are per type:

| Object | Kinds |
|---|---|
| intention | `fulfilled`, `abandoned`, `superseded` |
| availability | `retracted`, `superseded` |
| commitment | `cancelled` |

`superseded_by` is required when and only when `kind` is `superseded`, and
validation requires its target to exist. A retired object is never edited
again except to append acknowledgements, and its file is never deleted.
`retired.kind` is part of the projection, because a retired object no longer
clashes with anything and consistency must see that; `reason`, `source`, and
`timestamp` are not.

### Values

#### `DURATION`

An ISO 8601 duration, optionally ranged:

```yaml
duration: PT90M
# or
duration: {nominal: PT1H, min: PT30M, max: PT2H}
```

When ranged, the nominal value lies within the range and resolution prefers it.
A zero duration is written `P0D`, on disk and in the projection.

#### `WINDOW`

The bounds within which an intention should happen or an availability holds,
stored as the person expressed it. A window never stores computed start and
end datetimes. Its bounds are computed when a resolver needs them, from the
resolver context (`resolver.timezone`, and `resolver.hemisphere` for neutral
season codes) in `intentions.yaml` or overridden on the call. Week granules
are ISO weeks, Monday to Sunday, in every context.

A window has one or more of three anchors, and a placement must satisfy
every anchor present:

```yaml
window:
  calendar: 2026-W37                       # a calendar anchor: EDTF
  relative:                                # a relational anchor: RFC 9253
    target: int_01a06cf2-8e11-7b3a-9c7d-4f0a2b6e8d13
    relation: FINISHTOSTART
    gap: {min: P0D, max: P3D}
  clock: 09:00/12:00                       # a clock anchor: time of day
```

**Calendar anchor.** An ISO 8601-2 / EDTF expression from the admitted subset:

| Expression | Means |
|---|---|
| `2026`, `2026-09`, `2026-W36`, `2026-09-04` | that year, month, week, day |
| `2026-21` … `2026-24` | spring, summer, autumn, winter, resolved by `resolver.hemisphere` |
| `2026-25` … `2026-28` | Northern spring, summer, autumn, winter (EDTF) |
| `2026-29` … `2026-32` | Southern spring, summer, autumn, winter (EDTF) |
| `2026-33` … `2026-36` | Q1 … Q4 (EDTF quarter codes) |
| `2026-W36/2026-W38` | a bounded interval between granules |
| `../2026-09` | by the end of September |
| `2026-09/..` | from September on |

Northern spring, summer, autumn and winter are March to May, June to August,
September to November, and December to February; Southern are September to
November, December to February, March to May, and June to August. A season
that begins in December starts in the granule's year and runs into the next.
`resolver.hemisphere` defaults to `north`, which is what every EDTF reader
assumes; a Melbourne workspace sets `south` once rather than writing `29`
every time. EDTF uncertain and approximate qualifiers (`?`, `~`, `%`) are not
admitted; a qualifier with no resolution semantics is decoration.

Deixis is resolved at write time; bounds are resolved at resolution time. A
person who says *this week* on 2026-09-04 gets `2026-W36` in the file, so the
object means the same week a month later. What `2026-W36` starts and ends at in
clock time depends on the resolver's timezone, and is never written. A writer
that accepts deictic terms recognises at least `today`, `tomorrow`,
`this-week`, `next-week`, `this-month`, `next-month`, `this-quarter`,
`next-quarter`, and `this-year`, each the granule containing the current
instant in the resolver's timezone or the one after it. Because weeks are ISO
weeks, `this-week` on a Sunday is the week ending that day; a writer talking
to someone whose week starts on Sunday may ask which week was meant, since
the format carries no such preference.

**Relational anchor.** `target` is another intention or commitment; `relation`
is one of `FINISHTOSTART`, `FINISHTOFINISH`, `STARTTOFINISH`, `STARTTOSTART`
as defined in [RFC 9253](https://www.rfc-editor.org/rfc/rfc9253); `gap` is an
optional `{min, max}` pair of ISO 8601 durations, generalising RFC 9253's
single `GAP` into a range so that *within three days after X* is expressible.
The dependent window holds the reference, inverting RFC 9253's convention of
placing the relation on the predecessor, to match the outbound-reference rule.
Each relation bounds one end of the candidate by one end of the target;
`min` defaults to `P0D` and an absent `max` is unbounded above:

| Relation | Constrains |
|---|---|
| `FINISHTOSTART` | candidate start in `[target end + min, target end + max]` |
| `STARTTOSTART` | candidate start in `[target start + min, target start + max]` |
| `FINISHTOFINISH` | candidate end in `[target end + min, target end + max]` |
| `STARTTOFINISH` | candidate end in `[target start + min, target start + max]` |

A relational anchor whose target has no placement, or is retired or
cancelled, is a constraint between two unresolved windows, not an error;
resolution reports the dependent intention as blocked on its target.

**Clock anchor.** An ISO 8601 time-of-day interval, `HH:MM/HH:MM`, read in
the resolver's timezone and applied to every local day the other anchors
admit. The start is inclusive and the end exclusive. The interval may cross
midnight, in which case it belongs to the local day of its start. Absent
means whole days. Like the other anchors it is stored as written and its
bounds are computed when needed, so *mornings* survives a move between
zones; where a clock time does not exist on a given day, the resolver follows
[RFC 5545 §3.3.5](https://www.rfc-editor.org/rfc/rfc5545#section-3.3.5) for
nonexistent local times. Time of day lives here and nowhere else.

Temporal relations live here and nowhere else. `DEPENDS-ON`, `FIRST`, `NEXT`,
`PARENT`, and `CHILD` are not admitted anywhere: the first three are precedence
without scheduling semantics, which `FINISHTOSTART` already expresses; the last
two imply a tree, and the intention graph is not one.

#### Cadence

Where an object carries `cadence`, it is an iCalendar RRULE
([RFC 5545 §3.3.10](https://www.rfc-editor.org/rfc/rfc5545#section-3.3.10)).
using only its date-level parts: `BYHOUR`, `BYMINUTE`, and `BYSECOND` are not
admitted, because time of day belongs to the window's clock anchor. An object
carrying `cadence` has a window with a calendar anchor, and the rule expands
from a seed: the first local day of that anchor's lower bound, or, when the
bound is open (`../X`), the first day of the horizon the caller supplies.
`WKST` defaults to `MO` unless the rule says otherwise. Cadence expresses only
a generating pattern. `RDATE`, `EXDATE`, and `RECURRENCE-ID`
are never used: a skipped occurrence is a retired instance.

#### `PLACEMENT`

A concrete start, a duration, and optionally one location:

```yaml
placement:
  start: 2026-09-15T10:00:00+10:00
  duration: PT1H
  location: https://example.com/rooms/3
```

`start` is an RFC 3339 datetime with offset, or a calendar day. A calendar
day makes the placement all-day: `duration` is then whole days and the
placement spans those local days in the resolver's timezone, so a day with a
timezone transition is still one day. Resolution writes datetimes; only an
import writes a calendar day.

It exists only on a resolved intention and on a commitment, and is written only
by a resolution or an import. It is the single point where this format touches
clock time and fixed place, and it arrives last. When the intention or its
supply constrained location, resolution picks one URI from the intersection.

---
## Object Model

```
INTENTION      what a person means to do — no other party
                 ← subject: whose it is
                 ← duration, window: how long, within what bounds
                 ← serves[]: in-order-to → other intentions
                             for-the-sake-of → a terminus
                             instance-of → the recurring intention that generated it
                 ← cadence: makes it recurring; instances are generated from it
                 → placement: written by RESOLUTION

AVAILABILITY   what a particular has capacity for — supply
                 ← subject: any URI
                 ← duration, window, conditional[], location[], cadence
                 ← valid_until: after which it is unusable, not false

COMMITMENT     an intention that interlocks with others — the hand-off
                 ← parties[{uri, status}]: status is that party's act alone
                 ← placement: always
                 ← origin: resolution | import
                 ← external.uid: the only link to iCalendar / JSCalendar

records        RESOLUTION      standalone — relates intention, placement, displaced
               ACKNOWLEDGEMENT embedded — "I have seen this flag against this version"
               RETIREMENT      embedded — kind, reason, superseded_by
```

### The serves graph

```
   int: 90 min on the budget narrative
         │ in-order-to
         ▼
   int: board pack out by 2026-W38            int: weekly 1:1 with Priya (recurring)
         │ in-order-to                              │ generates
         ▼                                          ▼
   int: run the finance function well      int: 1:1, occurrence 2026-09-15
         │ for-the-sake-of                          │ instance-of (back to recurring)
         ▼                                          │ for-the-sake-of
   int: being someone who follows through  ◀────────┘
         (terminus: no window, no duration, no serves;
          reference → a DKF claim Ada holds about herself)
```

The graph is a DAG reconstructed by walking outbound references; no object
stores inbound links. A write that would close a cycle is refused, and
validation detects cycles that arrive by merge, reporting each strongly
connected component as an error. Intentions in a cycle are quarantined
(unresolvable, flagged `cycle`); the rest of the graph is unaffected. Termini
are sinks by definition, which removes the most likely accidental cycle.

### The resolution lifecycle

```
  INTENTION (duration + window, no placement)
       │
       │  generate: instances of recurring intentions over the horizon
       ▼
  RESOLUTION operation — a function of workspace, intentions.yaml, now
       │  range:  [max(window start, now), min(window end, now + horizon)]
       │  demand: duration, window, activity, subject + parties
       │  supply: ∩ eligible AVAILABILITY per tracked particular
       │          (unretired, unexpired, conditional ∋ activity,
       │           location ∩ location ≠ ∅ or either absent, visible,
       │           remaining capacity ≥ duration)
       │          an untracked party constrains no supply and still
       │          brings every placement that occupies them
       │          candidates lie within every clock interval present,
       │          start on a resolver.step grid aligned to each supply
       │          interval, and span the nominal duration (shorter, down
       │          to min, only when the nominal yields nothing)
       ▼
  ranked candidates
       │  1. displaces nothing firm or accepted
       │     (a commitment's status here is the subject's own entry;
       │      overlapping one they declined, or a transparent one,
       │      is not displacement)
       │  2. displaces only tentative
       │  3. requires retiring something firm
       │  then: declared preference; then earliest
       ▼
  selection — a recorded act (person, or a policy the person holds)
       │
       ├──▶ intention.placement written (replacing cancels a live commitment)
       ├──▶ RESOLUTION record written (selector, displaced, supply, presumed)
       └──▶ if parties: COMMITMENT created, everyone tentative
```

Resolution refuses an intention that lacks duration or window, is retired,
carries a `cycle` flag, has a relational anchor whose target is unplaced, or
is already placed and the caller did not ask to replace. A window that has
passed, or starts beyond the horizon, yields no candidates and a reason;
nothing before now is ever offered.

**A party the workspace does not track.** A workspace holds the capacity of
the people it is for, and mostly cannot hold anyone else's. It tracks a party
exactly when it holds at least one availability whose subject is that party,
retired or expired included. A party it does not track contributes no supply
constraint: resolution places against the subject's own supply and every
tracked party's, and the commitment carries that party `tentative`, which is
already what this format calls someone who has not yet agreed and is the state
an invitation is sent from. A party it does track, whose eligible availability
does not fit, still yields no candidates and is named, because that is the
party's own answer rather than a gap in the workspace. The subject is never
unconstrained by this rule, whatever their records and even where they appear
in their own `parties`.

Untracked means unconstrained, not satisfied. The format presumes nothing
about that party's capacity and records the presumption in `presumed` on the
resolution. And what the workspace does know about them still counts: every
unretired placement that occupies them constrains candidates exactly as a
tracked party's would, so a second meeting with the same person at the same
hour is displacement rather than nothing. A workspace never writes an
availability for a party in order to make a resolution succeed. An
availability is an assertion about that particular's capacity, and inventing
one records a fact nobody asserted about time that is not the writer's to
declare.

One consequence is worth naming, because it looks like a defect and is not:
declaring your first availability makes you strictly harder to schedule with
than declaring none. Supply is a positive assertion, so this is the difference
between having spoken and not having spoken.

Displaced objects are listed and flagged,
never changed.

### Composition by reference

```
  iCalendar / JSCalendar  ◀── external.uid ──  COMMITMENT
                                                    ▲
  this format owns all prospective state            │ id (+ version)
                                                    │
  DKF claim  ── cites ──▶  any object here          │
  (retrospective, contested, evidential)  ──────────┘
  INTENTION.reference ── informal ──▶ DKF claim (never validated)
```

Three deliberate reuses cross the iCalendar boundary: ISO 8601 durations,
RRULE cadence, and the RFC 9253 relation vocabulary. Nothing else does. No
object here depends on a DKF object to exist or validate.

---

## Consistency

The consistency check surfaces every way the prospective graph fails to hang
together. It never decides. Its outputs are flags; what persists is the
person's acknowledgement.

### Flags

A flag has exactly one `kind`, no numeric severity, and is recomputed on every
check rather than stored:

| Kind | Meaning |
|---|---|
| `window-clash` | two placements overlap while sharing a party whom both occupy, or a placement falls where there is no eligible supply |
| `condition-mismatch` | the supplying availability's `conditional` does not include the intention's `activity` |
| `location-mismatch` | the placement's location is outside the supplying availability's `location` list, or outside the intention's |
| `expired-ground` | an availability the placement rests on has expired or been retired |
| `intention-inconsistency` | two active unplaced intentions of one subject each have candidates alone but no non-overlapping pair; checked pairwise, never globally |
| `party-declined` | a commitment has a party at `declined` while the intention it fulfils is still placed |
| `cycle` | the intention is in a strongly connected component of the serves graph |

A transparent commitment occupies no time and rests on no supply, so it is
never the subject or counterpart of `window-clash`, and never the subject of
`condition-mismatch`, `location-mismatch`, or `expired-ground`: there is no
supplying availability to compare it against. An opaque import still clashes
with everything it overlaps, which is the point.

A decline is flagged only where it contradicts something. An imported
commitment has no intention behind it, so declining one frees the decliner's
hour and there is nothing left to disagree with. A commitment from a
resolution is different: the intention's own placement still occupies the
subject's time, so their decline frees nothing and they have said they will
not attend a thing they still intend at that hour. `party-declined` names
that, on both objects, with the declining party in the detail. A counterparty's
decline is flagged for the same reason, since the arrangement has lost someone
it needed. The person then cancels, replaces, or acknowledges and goes ahead
without them; nothing here decides for them.

What a placement rests on is recomputed at every check: every occasion of
each involved particular that contains it. Nothing stored on the placement or
the resolution record decides this. No containing occasion is a `window-clash`
without counterpart; containing occasions that all fail are reported by why
they fail, as `expired-ground`, `condition-mismatch`, or `location-mismatch`.

Kinds are not graded. `location-mismatch` sits beside `condition-mismatch`
because it has the same shape: the capacity exists but was not offered for
this. Whether two URIs denote compatible places (a meeting link taken from
home) is a fact about the URIs the format does not know, so a mismatch is
never an impossibility judgement. An imported meeting at a place the person
will not be is a different fact, expressible only once presence is modelled,
and would be its own kind.

A flag carries `kind`, `subject` (the object it is reported on),
`counterpart` (the other object, where there is one), `counterpart_version`
(the counterpart's projection hash at check time), and a human-readable
`detail`. A clash between two objects is reported on both.

The check runs on creation or projection change of a commitment, projection
change of an availability or intention, every resolution, and on demand. It
never retires an object or changes stability, placement, or party status.

### Acknowledgement, suppression, lapse

A computed flag is suppressed when its subject carries an acknowledgement with
the same kind, the same counterpart, and a `counterpart_version` equal to the
counterpart's current projection hash. If the counterpart's projection has
changed since, the acknowledgement has lapsed: the flag is reported again and
the old entry remains. A prose edit to the counterpart does not lapse it,
because prose is not in the projection.

An imported commitment clashing with declared availability is the technical
signature of someone else's claim on a schedule arriving without the person's
resolve having had any say. Flag-not-decide is how the format makes that
visible and contestable rather than silently absorbed.

---
## Versioning

Every object has a version: the hash of a canonical serialisation of its
**scheduling projection**, the fields that bear on consistency, as listed for
each type above. The version is derived, never declared.

The projection is expressed as a JSON object with values normalised first,
serialised with the JSON Canonicalization Scheme
([RFC 8785](https://www.rfc-editor.org/rfc/rfc8785)), and hashed with the
algorithm named by `hash` in `intentions.yaml`. Normalisation is:

- EDTF expressions in shortest admitted form.
- ISO 8601 durations with zero components dropped; weeks folded into days
  (`P1W` becomes `P7D`); the time part re-expressed from its total seconds as
  hours, minutes and seconds (`PT90M` becomes `PT1H30M`, `PT60M` becomes
  `PT1H`); no conversion between the date part and the time part, so `P1D`
  and `PT24H` stay distinct; no conversion of months or years; zero as `P0D`.
- Datetimes as RFC 3339 UTC with seconds.
- Every set-valued list sorted: references by id then role, commitment
  `parties` by `uri`, and string lists (`location`, `conditional`, an
  intention's `parties`, `displaced`) lexically.
- Absent optional fields omitted, and a boolean equal to its documented
  default omitted, so an explicit `transparent: false` hashes as absent.

The version is written `sha256:<lowercase hex>`. This version of the format
admits only `sha256`.

Prose, `source`, `timestamp`, acknowledgements, and a retirement's `reason`,
`source`, and `timestamp` are never in a projection. Editing them leaves the
version unchanged, so an acknowledgement lapses only when what was
acknowledged changed. Every object and every RESOLUTION record carries its
version in the file, immediately after `id`, so that a diff shows whether an
edit touched the projection; the computed value is authoritative and
validation warns when the written value disagrees or is missing.

Projection field sets are frozen per format version. `window.clock` and
`transparent` joined them while v0.1 was still undeclared, which is the last
moment such a change costs nothing. `intentions/0.1` hashes
exactly the fields this document enumerates; a change to any projection is a
new format version, so a stored `counterpart_version` stays comparable for as
long as its format version is known.

---

## File Layout

```
/intentions.yaml               workspace marker and configuration
/intentions.md                 optional conventions for agents and people
/.intentions                   optional pointer, when tools start elsewhere

/intentions/
  int_01a06d10-4c2e-7a91-b3f0-2d8e1a7c5b44.yaml

/availability/
  avl_01a06d12-9b7e-7c03-a5d1-6e2f4a8b0c77.yaml

/commitments/
  cmt_01a06d15-3f8a-7d61-8c2b-9a4e6f1d3b05.yaml

/resolutions/
  res_01a06d14-7e2c-7b19-a0d3-5c8f2e4a6b91.yaml

/index.yaml                    derived cache — see below
```

One object per file, in a directory named for its type. Objects are mutable
files edited in place: a window narrowing from `2026-09` to a concrete
placement is the same intention becoming definite, not a new one. History is
git's. Retirement appends; nothing is ever deleted.

### `intentions.yaml`

```yaml
format: intentions/0.1
hash: sha256
resolver:
  timezone: Australia/Melbourne
  horizon: P4W                                # planning horizon: resolution and generation
  hemisphere: south                           # optional; north when absent
  step: PT15M                                 # optional; candidate grid
  scope: personal                             # optional; visibility ceiling
availability:
  default_horizon: P13W
defaults:
  subject: https://example.com/people/ada     # optional
  source:
    author: https://example.com/people/ada
```

`resolver.horizon` is the one planning horizon: how far ahead resolution
offers candidates and how far ahead instances are generated. `resolver.step`
is the grid candidate starts lie on, aligned to each supply interval's start.
`resolver.scope` is a ceiling on what shared availability a resolver may see.
`resolver.hemisphere` resolves the neutral EDTF season codes and nothing
else. There is no week-start setting, and no separate generation horizon:
weeks are ISO weeks, and a reader that finds `resolver.week_start` or
`generation.horizon` in an older file ignores it and reports it at info
level. `defaults.subject` is optional. When present it is applied to any
intention written without one; when absent every intention names its subject. A
workspace may hold objects for several subjects: rooms and equipment already
require it, and an organisation workspace will leave the default unset.

Tools find the workspace by `--workspace`, then `$INTENTIONS_WORKSPACE`, then
the nearest ancestor directory containing `intentions.yaml` or a
`.intentions` pointer file holding a path.

### `intentions.md`

An optional prose file for agents and people: the activity terms in use, which
tags won when two overlapped, what the workspace is for. It has no schema and
validation does not read it. The activity vocabulary itself is not fixed by
this specification: terms are lowercase kebab-case, matched by exact equality,
never rejected for being unknown, and reported at info level when only one
object uses them.

### `index.yaml`

A derived cache of the object files, never the reverse. Each entry carries the
object's id, type, subject, file path, projection version, `retired.kind` if
any, and the ids of its outbound references, and nothing not derivable from
the file. It is regenerated by `index`, verified by `index --check`, committed
alongside the objects, and resolved on merge conflict by regeneration. A reader
that finds the index and a file disagreeing uses the file, and validation
reports the drift as a warning.

### Validation

`validate` checks the whole workspace and exits non-zero on any error:
dangling references, unknown `serves` roles, cycles, unparseable EDTF or ISO
8601 values, unknown retirement kinds, `superseded` without `superseded_by`,
duplicate active instances for one occurrence, an intention or availability
with no author, `firm` on an intention whose `source` carries a harness and
which has no `firmed_under`, `firmed_under` naming anything but an active
policy of the subject, `auto_select` or `auto_firm` on an intention that is
not a terminus, `cadence` on an object whose window has no calendar anchor, a
sub-day RRULE part in `cadence`, a fractional duration on an all-day
placement, and `transparent` on a commitment born of a resolution. Where a write
can tell that its result would fail, it refuses. Write-time refusal is a
convenience; validation is the invariant, because files arrive by merge
without passing through any writer.

---

## Design Principles

**The window is the person's, not the clock's.** A window stores what was
said, at the precision it was said, and is collapsed to clock time only at
resolution, by a resolver whose timezone is its own. Nothing
in this format writes a computed bound.

**Intention is not commitment.** An intention involves no other party and is
the person's alone. A commitment interlocks with others and hands off to
iCalendar. The two are different speech acts with different lifecycles, and
conflating them is how a calendar fills up with other people's time.

**Resolution is a function.** Given the workspace, `intentions.yaml`, and a
`now`, the candidate set and its order are determined: the range is bounded
by now and the horizon, starts lie on a grid, capacity is consumed, and the
checks are pairwise. Two implementations produce the same candidates, which
is the only sense in which they can be said to agree about an operation.

**Flags, never decisions.** Resolution ranks and the person selects. A clash
is surfaced and the person acknowledges or does not. A party's status changes
by that party's act. Software here proposes; it does not resolve on anyone's
behalf, except under a policy the person holds and that names itself on the
act.

**Every object says who wrote it.** A harness may draft. It may not make an
intention firm, select a placement, or accept a commitment without either the
person's direct act or a policy they hold. Authorship is the axis on which
a schedule is authentic or imposed, and the format keeps it visible.

**Live state is mutable; events are appended.** Unlike DKF, whose claims are
epistemic history and therefore immutable, these objects are what a person
currently intends and are edited in place. What happens to them is recorded
and never rewritten.

**Compose by reference, never by shared schema.** ISO 8601, RRULE, RFC 9253
and EDTF are borrowed as grammars. iCalendar and JSCalendar are linked by a
uid. DKF is linked by an id. No other system's object model is embedded here
and this format's is embedded in none.

**Files over databases.** The canonical store is a directory of YAML files in
a git repository. The index is a cache of the files, never the reverse.

---

## Status

This specification is in early draft. The object and record types, identifier
format, field sets and canonical order, the projection and its hashing, the
serves graph and its roles, the WINDOW anchor forms and their admitted
vocabularies, the resolution ranking and the flag kinds are believed settled
and are backed by a reasoning chain in a companion knowledge workspace. A
first implementation, [intentions-cli](https://github.com/nodelogicau/intentions-cli)
v0.1.0, has been written from this text and raised thirteen issues where it
was ambiguous or silent; all thirteen are settled in the text as it now
stands, four of them differently from what the implementation chose.

Deferred from this version, deliberately:

- **Federation.** Scope visibility is defined within one workspace. Reading
  another workspace's availability, and how commitments travel between
  workspaces (most likely as iCalendar or JSCalendar over iTIP rather than as
  this format at all), are undesigned.
- **A retrospective record.** What was actually done against a resolved
  intention is DKF's job, by a claim citing the object at a version. Whether a
  personal workspace that never writes DKF claims needs something minimal of
  its own is open.
- **Presence.** Where a subject will be, independent of what they have
  capacity for. Not an availability: capacity unions, whereabouts intersects,
  and making every location-bearing availability constrain would turn two
  overlapping capacities at different places into nothing. If added it is a
  `PRESENCE` object with subject, window, cadence, a required `location` list,
  and a validity horizon, but no duration or conditional. It supplies nothing;
  it narrows the location set of every candidate its window covers, absent
  meaning anywhere. A placement outside every covering presence would be a
  new flag kind, `presence-clash`, reported on both objects. Not supported;
  place rides on capacity.
- **The policy condition grammar.** `auto_select` and `auto_firm` admit
  `max_duration` and `stability`; further terms await a use.
- **v0.1.** Its condition, a second reader implementing from this text, is
  met. Declaring it is a deliberate act still to come.

Feedback on the object model, field names, and missing cases is the most
valuable contribution at this stage.

---

## References

**Dialectical Knowledge Format (DKF).** The format this one composes with for
the retrospective layer, and whose conventions (file-per-object YAML,
prefixed UUIDv7 ids, canonical field order, `source`, derived index,
review through git) this specification adopts. Reading its README first will
make this one's shape familiar.
[Specification](https://github.com/nodelogicau/particulars) ·
[particulars.fyi](https://particulars.fyi), a visual introduction ·
[particulars-cli](https://github.com/nodelogicau/particulars-cli), the
reference implementation.

**Standards borrowed as grammars.**
[RFC 9562](https://www.rfc-editor.org/rfc/rfc9562) UUID version 7 ·
[RFC 3339](https://www.rfc-editor.org/rfc/rfc3339) timestamps ·
[ISO 8601](https://www.iso.org/iso-8601-date-and-time-format.html) durations ·
[EDTF](https://www.loc.gov/standards/datetime/), the Extended Date/Time
Format (ISO 8601-2), for calendar anchors ·
[RFC 5545 §3.3.10](https://www.rfc-editor.org/rfc/rfc5545#section-3.3.10)
RRULE for cadence ·
[RFC 9253](https://www.rfc-editor.org/rfc/rfc9253) temporal relations for
relational anchors ·
[RFC 8785](https://www.rfc-editor.org/rfc/rfc8785) JSON Canonicalization
Scheme for the projection hash ·
[RFC 5870](https://www.rfc-editor.org/rfc/rfc5870) `geo:` URIs, admitted as
locations.

**Calendar formats composed with by reference.**
[RFC 5545](https://www.rfc-editor.org/rfc/rfc5545) iCalendar ·
[RFC 8984](https://www.rfc-editor.org/rfc/rfc8984) JSCalendar ·
[RFC 5546](https://www.rfc-editor.org/rfc/rfc5546) iTIP.

**Philosophical sources.** Martin Heidegger, *Being and Time* (1927), on
clock time versus lived temporality (Division II §§78–81), the referential
totality of in-order-to and for-the-sake-of (Division I §§14–18), and
repetition (Division II §74). Michael Bratman, *Intention, Plans, and
Practical Reason* (1987), on intentions as partial plans, reconsideration,
and self-governing policies. John Searle, *Speech Acts* (1969) and
*Expression and Meaning* (1979), on the assertive/commissive distinction and
felicity conditions that separate availability from intention and forbid
software from setting a party's status.

---

## License

The specification is released under [CC0 1.0 Universal](LICENSE). Reference
implementations are released under the MIT License. You are free to implement
the format without restriction.
