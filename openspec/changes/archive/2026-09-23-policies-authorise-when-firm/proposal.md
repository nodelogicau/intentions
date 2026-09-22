## Why

A policy is a terminus carrying a condition, and #26 made a terminus inert as a ground until the person firms it. It said nothing about the terminus as an authorisation, so a harness can write a tentative policy and firm or select under it the same minute, with every boundary rule holding formally (nodelogicau/intentions #27, reproduced against intentions-cli v0.12.0 with `0 errors`). That leaves a terminus inert where it matters less and live where it matters more: authorising a harness to act alone is the stronger power. The boundary was meant to make a harness's firming rest on something the person holds, and the thing it rests on here was never held by anyone.

## What Changes

- **A terminus is inert until firm: it grounds nothing and authorises nothing.** The rule is stated once, in the Terminus requirement, and Policies and Auto-selection refer to it. A tentative policy is a draft: a harness may write one, and until the person firms it, `intention_firm` and `select` refuse to act under it, naming the draft and the act that firms it.
- **`firmed_under` names a firm policy.** Naming a tentative one is a validation error, since the act it records was not authorised. A person withdrawing a policy, by setting it tentative or retiring it, withdraws what rested on it: intentions firmed under it are in error until the person re-firms them by their own act or sets them tentative. Setting a policy tentative suspends it; retiring it ends it.
- **A RESOLUTION record is history, not a live object.** A record whose `selector` names a policy since set tentative or retired is a warning, not an error: the act was authorised when it happened, and the placement it produced stands and is the person's to keep or re-resolve. The retired case was unstated; both are settled together.
- The Design Principles sentence "a terminus grounds nothing until the person, by their own act, has made it firm" gains two words: grounds nothing and authorises nothing.
- Error level from the start. Neither the site's example nor the maintainer's workspace holds a policy, and a harness-drafted policy in use is the case the rule exists to catch.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `intention`: Stability (`firmed_under` names a firm policy; withdrawal), Terminus (inert until firm), Policies (authorise only while firm; draft, suspend, end).
- `resolution`: auto-selection only under a firm policy; refusal under a draft.
- `object-model`: Validation gains the error and the warning.
- `harness-tools`: `select` and `intention_firm` require a firm policy and name the draft on refusal.

## Impact

- README: the serves-graph paragraph on the terminus as the person's word, the Policies paragraph, the Stability paragraph, the RESOLUTION `selector` prose, the Validation section, the Design Principles sentence, and the two Reference Tool Set bullets. Four spec deltas.
- No example or figure changes; no workspace known to hold a tentative policy.
- intentions-cli: the refusals, the error, the warning, and the message naming the draft and the firming command. Its v0.12.0 behaviour, accepting a draft as a policy, becomes non-conforming.
- Knowledge workspace: one claim and a qualification synthesis on the spine after archive.
