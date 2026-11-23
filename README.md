# The Queue Preview That Moved Too Much

A reorder preview imports the current work queue and the operator's desired order. It reports four relocations for four entries, even though an independently checked baseline needs fewer. The preview overstates the work and makes small queue changes look disruptive.

Repair only `plan_reorder` in `planner.py`, preserving the validator, monitor and tests. Python 3.11+ standard library only.

```sh
python monitor.py
python -m unittest discover -v
```

The monitor is informational; unit tests are the local acceptance gate. Open a PR against main with the corrected preview and regression evidence.

## Exact contract

`plan_reorder(current, target) -> tuple[str, ...]`

- `current` and `target` are both exact built-in tuples of 0 to 1,000 entries. Each entry is an exact built-in nonempty str of at most 80 Unicode code points. IDs are case-sensitive and compared exactly; do not trim, normalize or sort the ID text.
- Every ID is unique within each tuple, and both contain the same set of IDs. Empty tuples are supported together. Validate both inputs before any shortcut; invalid input raises `ValueError`, with no graded requirement for exact error text or validation precedence.
- Return the IDs that can be left untouched, in their original relative order. They must also appear in that same relative order in the target, but may occupy different absolute positions. They need not be adjacent.
- Choose the greatest possible number of untouched IDs. If several choices are equally long, choose the lexicographically smallest **tuple of original zero-based indices**. Compare the entire index sequence from left to right, not sorted IDs or target indices. Output only the exact built-in tuple of corresponding IDs (not indices, count, or move instructions).
- For example, with current `("Z", "A", "Y", "B")` and target `("A", "Z", "B", "Y")`, the earliest maximal original indices are `(0, 2)`, so return `("Z", "Y")`.
- No mutation, persistent state, wall clock, I/O, queue access, or third-party dependencies. A quadratic algorithm is sufficient at the stated bound; exponential enumeration is not suitable for the learner implementation.

## What the metric means

One relocation removes one existing entry and reinserts it anywhere. Entries that are not explicitly moved retain relative order; their absolute positions can shift. The preview forecasts `len(current) - len(untouched)` relocations under this model, not adjacent swaps. It does not generate the actual operation sequence, alter priorities, enforce dependencies, accept different ID sets, or change a live queue. All fixtures are synthetic.
