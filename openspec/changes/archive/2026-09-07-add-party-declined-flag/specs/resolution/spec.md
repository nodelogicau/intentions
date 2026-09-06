## MODIFIED Requirements

### Requirement: Candidate ranking by reconsideration cost

Candidates SHALL be ordered first by reconsideration cost, from lowest to highest:

1. Displaces no existing placed firm intention and no accepted commitment.
2. Displaces only tentative placed intentions or tentative commitments.
3. Requires retiring a firm intention or cancelling an accepted commitment.

Where a rung names a commitment's status it means the resolving subject's own party entry, never another party's. A commitment that does not occupy the subject's time, because their entry is `declined` or because it is transparent, SHALL NOT be treated as displaced by any candidate and SHALL NOT raise a candidate's rank.

Within a rank, candidates SHALL be ordered by the intention's declared `preference` if present, otherwise by that of the nearest standing intention it is an instance of, otherwise by earliest start.

#### Scenario: Firm outranks tentative
- **WHEN** candidate X overlaps a tentative placed intention and candidate Y overlaps nothing
- **THEN** Y is ranked above X

#### Scenario: Declared preference breaks ties
- **WHEN** two candidates displace nothing and the intention declares `preference: latest`
- **THEN** the later candidate is ranked first

#### Scenario: The subject's own entry decides the rung
- **WHEN** a candidate overlaps a commitment on which the subject is `tentative` and a counterparty is `accepted`
- **THEN** the candidate is ranked as displacing a tentative commitment

#### Scenario: A declined commitment is not displaced
- **WHEN** a candidate overlaps an imported commitment the subject has declined and nothing else
- **THEN** the candidate is ranked as displacing nothing, and the commitment is not listed in `displaced`
