## Why

`hold-placed-intentions` (#34) stops an intention's own calendar hold being imported as a commitment from now on, but it can't find one that was imported before. A harness that wrote holds before the field existed, an importer older than the check, or a merge, can leave an intention and an unretired commitment that share one `external` `system` and `uid`. They overlap, `check` reports a `window-clash`, and nothing names the cause. That is the self-inflicted clash the hold change exists to prevent (issue #36).

## What Changes

- **A new validation warning.** An intention whose `external` `system` and `uid` match an unretired commitment's `external` is reported at warning level, naming both objects.
- **The warning names the fix.** If the commitment is the intention's own hold imported before it was recognised, retire the commitment as `cancelled`. If the commitment is a real event that happens to share the UID, clear the intention's `external`.
- **A warning, not an error.** The workspace is still consistent as data, and only the person can tell which of the two cases it is. A write that sets `external` to a UID an unretired commitment already carries is accepted and reports the warning, as with any other warning.
- **The import rule is unchanged.** Recognising a hold on import still prevents the case from now on. The warning finds the cases that got past it.

### Non-goals

- Retiring the commitment automatically. A commitment's retirement is the person's act, and the UID match doesn't prove the commitment is the hold.
- Suppressing the `window-clash` between the two. The clash stays until the person acts or acknowledges it. The warning explains it; it doesn't replace it.
- How a solo event imported from someone else (a venue's ticket invite) should be modelled. That is #35.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `object-model`: Validation gains a warning for an intention and an unretired commitment sharing an `external` `system` and `uid`.
- `intention`: Calendar hold says what happens when a link matches a commitment that already exists, and points to the warning.

## Impact

- README: the Validation paragraph, and the Calendar hold paragraph under INTENTION.
- Lands within `intentions/0.2` (and applies under 0.1). `external` on an intention is outside the projection, so no hash moves, and no workspace needs migrating.
- intentions-cli (v0.17.0 reports nothing here) needs the warning in `validate`, and needs the write path that sets `external` to report it.
- Closes issue #36.
