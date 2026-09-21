# Portal submission - Hysteresis Condition Watcher

## Title

Hysteresis Condition Watcher

## Notes under 1000 chars

```text
A GenLayer IC that evaluates a fixed condition repeatedly and changes state only
after a configured run of matching determinations. HOLDS and CLEAR advance
opposite streaks; unavailable or non-convergent checks are audited but leave both
streaks untouched, so missing signal cannot trigger or clear the watch. Recent
history is bounded. Calls are permissionless but a committed 60-to-86400-second
minimum interval is enforced from deterministic transaction time. Scheduling is
explicitly an external keeper responsibility rather than a claimed capability.
```

## Evidence checklist

- GitHub: https://github.com/Zhekinmaksim/genlayer-hysteresis-condition-watcher
- Commit: pending
- Explorer contract: pending
- Deploy transaction: pending
- Offline verification: `python3 sim/check.py`, 5/5 pass on 2026-09-12
- Hosted Studio checks: pending
