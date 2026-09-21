# Test plan - Hysteresis Condition Watcher

## Offline checks

1. `n_confirm` consecutive `HOLDS` results flip clear to triggered.
2. A `CLEAR` result resets the confirmation streak.
3. `n_confirm` consecutive `CLEAR` results flip triggered to clear.
4. An undetermined result increments its audit counter but changes no streak.
5. History remains bounded at twenty results.
6. Invalid ids, sources, confirmation counts, and intervals revert before judgment.
7. Prompt failures and URL pin failures are recorded as undetermined.
8. A second check before `min_interval_seconds` elapses reverts with
   `CHECK_TOO_SOON` and does not consume a judgment.

## Hosted Studio checks

Use a stable HTTPS status page and an external keeper with an explicit cadence.
Verify at least one flip in each direction and record every check transaction.
The contract does not schedule itself. It enforces the configured minimum
interval, while the external keeper remains responsible for initiating calls.
