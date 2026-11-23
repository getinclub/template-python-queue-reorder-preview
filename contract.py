"""Bounded validation for the synthetic reorder problem."""
MAX_ENTRIES = 1000
MAX_ID_CODEPOINTS = 80


def validate(current, target):
    if any(type(order) is not tuple or len(order) > MAX_ENTRIES
           for order in (current, target)):
        raise ValueError("both orders must be exact bounded tuples")
    for order in (current, target):
        if any(type(item) is not str or not 1 <= len(item) <= MAX_ID_CODEPOINTS
               for item in order):
            raise ValueError("invalid queue ID")
        if len(set(order)) != len(order):
            raise ValueError("duplicate queue ID")
    if set(current) != set(target):
        raise ValueError("current and target must contain identical ID sets")
