"""Informational monitor. Unittest is the acceptance gate."""
from planner import plan_reorder

CURRENT = ("A", "B", "C", "D")
TARGET = ("B", "C", "D", "A")
EXPECTED = ("B", "C", "D")

if __name__ == "__main__":
    retained = plan_reorder(CURRENT, TARGET)
    print(f"Imported two orders of {len(CURRENT)} synthetic queue entries")
    print("Preview relocations:", len(CURRENT) - len(retained))
    print("Trusted baseline:", len(CURRENT) - len(EXPECTED))
    print("MATCH" if retained == EXPECTED else "MISMATCH: preview moves too much")
