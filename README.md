# Watcher - consensus across repeated runs

A GenLayer Intelligent Contract that confirms a condition is real and persistent
before flipping a stored flag. Consensus is reached over time with hysteresis,
not in one pass.

## Consensus mechanism

Each `check` judges whether the condition currently holds, one bit, via
`prompt_non_comparative`. The stored TRIGGERED flag flips only after N
consecutive confirming checks, and flips back only after N consecutive clears.
The consensus object at each run is a small state transition; the contract
accumulates confirmations across calls. A committed interval of 60 to 86400
seconds is enforced between accepted checks using deterministic transaction
time, so repeated calls cannot compress a confirmation run into one instant.

## Key safety property

An UNDETERMINED run (source down, or judgment did not converge) neither
increments nor resets the streak. It is skipped and recorded. So an outage can
never by itself trigger or clear the flag. Only genuine, sustained readings move
state.

## Honest limitation

GenLayer contracts do not self-schedule. `check` must be called by an external
keeper or a user. This contract is the judgment, interval gate, and hysteresis;
the trigger cadence is external. It does not claim autonomy.

## Outcomes

- State is CLEAR (0) or TRIGGERED (1), read via `get_state`.
- `get_status` returns the streaks, total checks, and undetermined count so the
  trajectory is auditable.

## API

- `open_watch(id, condition_text, source, is_url, n_confirm, min_interval_seconds)` -> condition hash
- `check(id)` - permissionless; call on a schedule via keeper or user
- `get_state(id)` -> 0 clear, 1 triggered
- `get_status(id)` -> streaks and counters

## Test plan (run in hosted Studio)

1. Condition holds for N consecutive checks -> flips to TRIGGERED at the Nth.
2. Condition holds N-1 times then clears -> does NOT trigger.
3. Triggered, then clears for N consecutive -> flips back to CLEAR.
4. Dead source mid-run -> undetermined checks, streak untouched, no flip.
5. Injection in source -> judged on merit or the run is undetermined.
6. History exceeds the bound -> oldest rolls off, counters stay correct.
7. Cost: note the per-check consensus cost and a sane minimum interval.

## Notes

The contract deployed in hosted Studio with the expected method schema. The
hysteresis counter is deterministic and covered by offline simulation; live
repeated checks with an external keeper have not been exercised.

## Deployment

- GitHub: https://github.com/Zhekinmaksim/genlayer-hysteresis-condition-watcher
- Studio contract: https://explorer-studio.genlayer.com/address/0xb3f72989B8D674f6465B35b83673Aa73F65e74b9
- Deploy transaction: https://explorer-studio.genlayer.com/tx/0xa53cdf8f43c4d01090fbe26b22e1c0c02cbaad48ff6deed01f15567bc4877c26
- Deployed source commit: `a4c003db46f6ae5860887097eddae6f4502910c3`
