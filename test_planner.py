from itertools import combinations, permutations
import unittest
from monitor import CURRENT, TARGET, EXPECTED
from planner import plan_reorder as plan


def brute(current, target):
    for length in range(len(current), -1, -1):
        for indices in combinations(range(len(current)), length):
            keep = tuple(current[i] for i in indices)
            wanted = set(keep)
            if tuple(x for x in target if x in wanted) == keep:
                return keep


class PlannerTests(unittest.TestCase):
    def check(self, current, target, expected):
        actual = plan(current, target)
        self.assertIs(type(actual), tuple)
        self.assertEqual(actual, expected)

    def test_incident(self):
        self.check(CURRENT, TARGET, EXPECTED)

    def test_same(self):
        current = ("z", "A", "b")
        self.check(current, current, current)

    def test_empty_and_single(self):
        self.check((), (), ())
        self.check(("one",), ("one",), ("one",))

    def test_reverse_prefers_first_original(self):
        current = ("z", "x", "d", "a")
        self.check(current, tuple(reversed(current)), ("z",))

    def test_tie_not_numeric_id_or_target_order(self):
        self.check(("Z", "A", "Y", "B"), ("A", "Z", "B", "Y"), ("Z", "Y"))

    def test_tie_after_same_prefix(self):
        self.check(("X", "Z", "A", "B"), ("X", "A", "Z", "B"), ("X", "Z", "B"))

    def test_earliest_locally_eligible_may_not_finish(self):
        self.check(("A","B","C","D","E"), ("A","C","D","E","B"), ("A","C","D","E"))

    def test_noncontiguous_in_both_orders(self):
        self.check(("a","x","b","y","c"), ("y","a","b","c","x"), ("a","b","c"))

    def test_fixed_positions_not_automatically_untouched(self):
        self.check(("a","b","c","d","e"), ("d","e","c","a","b"), ("a","b"))

    def test_unicode_case_whitespace_literal(self):
        current = ("é","e\u0301","a","A"," a"," ","😀"*80)
        self.check(current, current, current)

    def test_nearly_full_rotation(self):
        current = tuple(map(str, range(1000)))
        self.check(current, current[1:]+current[:1], current[1:])

    def test_full_reverse(self):
        current = tuple(map(str, range(1000)))
        self.check(current, tuple(reversed(current)), ("0",))

    def test_small_permutations(self):
        current = ("z","x","v","d","b")
        for target in permutations(current):
            self.check(current, target, brute(current, target))

    def test_repeated_input_and_isolation(self):
        inputs = (CURRENT, TARGET)
        self.check(*inputs, EXPECTED)
        self.check(TARGET, CURRENT, EXPECTED)
        self.check(*inputs, EXPECTED)
        self.assertEqual(inputs, (("A","B","C","D"),("B","C","D","A")))

    def test_invalid_container(self):
        class TupleChild(tuple):
            pass
        for bad in (None, ["a"], "a", 7, iter(("a",)), TupleChild(("a",))):
            with self.subTest(bad=bad):
                with self.assertRaises(ValueError):
                    plan(bad, ("a",))
                with self.assertRaises(ValueError):
                    plan(("a",), bad)

    def test_invalid_ids(self):
        class StrChild(str):
            pass
        for bad in (("",), ("a"*81,), (1,), (False,), (None,), (["a"],), (StrChild("a"),)):
            with self.subTest(bad=bad):
                with self.assertRaises(ValueError):
                    plan(bad, bad)

    def test_duplicates_and_unequal_sets(self):
        cases = [(("a","a"),("a","a")), (("a","a"),("a",)), (("a",),("a","a")),
                 (("a",),("b",)), ((),("a",)), (("a",),()), (("a","b"),("a",))]
        for current,target in cases:
            with self.subTest(current=current,target=target), self.assertRaises(ValueError):
                plan(current,target)

    def test_too_many(self):
        large=tuple(map(str,range(1001)))
        for case in ((large,large), (large,()), ((),large)):
            with self.assertRaises(ValueError):
                plan(*case)


if __name__ == "__main__":
    unittest.main()
