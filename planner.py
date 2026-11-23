"""Preview which entries can remain untouched during a reorder."""
from contract import validate


def plan_reorder(current, target):
    validate(current, target)
    return tuple(original for original, wanted in zip(current, target) if original == wanted)
