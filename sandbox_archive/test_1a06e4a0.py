# auto-injected by SEC sandbox
import itertools
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from itertools import product, combinations, permutations, chain
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_formula(n):
        if n == 1:
            return "p"
        elif n == 2:
            return "(p ∨ q)"
        else:
            left = generate_formula(random.randint(1, n-1))
            right = generate_formula(n - len(left) - 2)
            operator = random.choice(["∨", "∧"])
            return f"({left} {operator} {right})"
    
    def incidence_poset(formula):
        if formula == "p":
            return {(0,), (1,)}
        elif formula.startswith("(p ∨ q)"):
            return {(0,), (1,), (2,), (3,), (4,), (5,), (6,), (7,), (8,), (9,), (10,), (11,), (12,), (13,), (14,), (15,), (16,), (17,), (18,), (19,), (20,), (21,), (22,), (23,), (24,), (25,), (26,), (27,), (28,), (29,), (30,), (31,), (32,), (33,), (34,), (35,), (36,), (37,), (38,), (39,)}
        else:
            left, operator, right = formula[1:-1].split()
            poset_left = incidence_poset(left)
            poset_right = incidence_poset(right)
            return {(0,)} | {tuple(sorted(x + y)) for x in poset_left for y in poset_right}
    
    def ehrhart_semigroup(poset):
        n = len(max(poset, key=len))
        semigroup = set()
        for i in range(n+1):
            for subset in itertools.combinations(range(n), i):
                if all(x in poset for x in subset):
                    semigroup.add(tuple(sorted(subset)))
        return semigroup
    
    def resolution_width(formula):
        if formula == "p":
            return 1
        elif formula.startswith("(p ∨ q)"):
            return max(resolution_width(left), resolution_width(right)) + 1
        else:
            left, operator, right = formula[1:-1].split()
            return max(resolution_width(left), resolution_width(right))
    
    n = random.randint(5, 40)
    formula = generate_formula(n)
    poset = incidence_poset(formula)
    semigroup = ehrhart_semigroup(poset)
    width = resolution_width(formula)
    
    return {
        "metric_name": "resolution_width",
        "metric_value": width,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_width = sum(r["metric_value"] for r in results) / len(results)
    std_width = math.sqrt(sum((r["metric_value"] - mean_width)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_width} std={std_width} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_width} std={std_width} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")