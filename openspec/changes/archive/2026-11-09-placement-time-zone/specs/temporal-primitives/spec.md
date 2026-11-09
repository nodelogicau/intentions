## MODIFIED Requirements

### Requirement: Placement is the collapse to clock time

A `placement` is a concrete `start`, a DURATION, and an optional `location` (one absolute URI), and SHALL exist only on a resolved intention or a COMMITMENT. `start` SHALL be either an RFC 3339 datetime with offset or an EDTF calendar day. When `start` is a calendar day the placement is all-day: `duration` SHALL be a whole number of days and the placement SHALL span those local days in the resolver context's timezone, so that a day on which a timezone transition occurs is still one day. Resolution SHALL write datetime placements; a calendar-day `start` SHALL be written only by import. It is the single point where this specification touches clock time and fixed place, and it is written only as the result of a RESOLUTION or an import. When the intention or the supplying availability carries `location`, resolution SHALL set `placement.location` to one URI from their intersection; otherwise `placement.location` MAY be absent.

A datetime `start` MAY carry an RFC 9557 time-zone suffix: one bracketed IANA time zone name after the offset, as in `2026-09-15T10:00:00+10:00[Australia/Melbourne]`, recording the zone whose clock the placement was made on. The suffix SHALL be a bare zone name: an offset-form suffix, any other suffix tag, and the critical flag `!` SHALL NOT be admitted. A calendar-day `start` SHALL NOT carry a suffix, and no datetime in this specification other than a placement's `start`, on an intention, a commitment or a RESOLUTION record, SHALL carry one. Resolution SHALL write the zone it resolved in, which is `resolver.timezone` or the override on the call. Import SHALL write the zone the external event names when it is an IANA name, as Commitment's External reference only states. A writer SHALL NOT add a zone to a placement it did not make, and a placement with no suffix remains valid.

The offset SHALL fix the placement's instant. Where the offset differs from the offset the zone gives at that instant, as after a change to the zone's rules, the placement SHALL stay at the instant its offset gives, and validation SHALL report a warning (see Validation in Object model). The zone SHALL NOT change how windows, clock anchors or all-day spans are computed, which remain in the resolver context. Wherever two placements are compared, they SHALL be compared by instant, duration and location, never by zone.

#### Scenario: Placement written by resolution
- **WHEN** a resolution is selected for an intention
- **THEN** the intention gains a `placement` with a datetime `start` and its `window` is preserved unchanged

#### Scenario: Resolution records its zone
- **WHEN** a placement is selected by a resolution run with `resolver.timezone: Australia/Melbourne` for 10:00 local time on 15 September 2026
- **THEN** the placement's `start` is `2026-09-15T10:00:00+10:00[Australia/Melbourne]`, and the RESOLUTION record's placement carries the same value

#### Scenario: Zone does not change the version
- **WHEN** two otherwise identical intentions carry `start: 2026-09-15T10:00:00+10:00` and `start: 2026-09-15T10:00:00+10:00[Australia/Brisbane]`
- **THEN** their versions are equal

#### Scenario: Offset governs after a rule change
- **WHEN** a placement carries `start: 2027-10-03T10:00:00+10:00[Australia/Melbourne]` written under rules that kept Melbourne on `+10:00` that day, and the reader's time-zone database, updated since, gives `+11:00` at that instant
- **THEN** the placement stays at 00:00 UTC on 3 October 2027 and validation reports a warning naming both offsets and re-selection as the fix

#### Scenario: Existing placement not back-filled
- **WHEN** a placement written before this change carries `start: 2026-09-15T10:00:00+10:00`
- **THEN** it remains valid, and no operation adds a zone to it except a new selection

#### Scenario: Placement location chosen
- **WHEN** an intention with `location: [home, office]` is resolved against availability with `location: [office]`
- **THEN** the placement carries `location: office` and the intention's `location` list is unchanged

#### Scenario: All-day placement
- **WHEN** an import writes `placement: {start: 2026-09-21, duration: P5D}`
- **THEN** the placement spans the five local days from 21 to 25 September in the resolver's timezone

#### Scenario: All-day with a fractional duration rejected
- **WHEN** a placement is written with `start: 2026-09-21` and `duration: PT4H`
- **THEN** the write is refused and validation reports an error

#### Scenario: Zone on an all-day start rejected
- **WHEN** a placement is written with `start: 2026-09-21[Australia/Melbourne]`
- **THEN** the write is refused and validation reports an error naming the field
