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
- Deployed source commit: `a4c003db46f6ae5860887097eddae6f4502910c3`
- Explorer contract: https://explorer-studio.genlayer.com/address/0xb3f72989B8D674f6465B35b83673Aa73F65e74b9
- Deploy transaction: https://explorer-studio.genlayer.com/tx/0xa53cdf8f43c4d01090fbe26b22e1c0c02cbaad48ff6deed01f15567bc4877c26
- Offline verification: `python3 sim/check.py`, 5/5 pass on 2026-09-21
- Hosted Studio checks: deployment accepted in Normal (Full Consensus) mode;
  schema verified. Live repeated-check/keeper flow not run.
