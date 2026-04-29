# auto-injected by SEC sandbox
import math
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

def sipser_function(n, x):
    return sum(1 if (i & (1 << j)) else 0 for j in range(n) if i % (2 * (j + 1)) == 0)

def additive_energy(n):
    E = 0
    for a in range(2**n):
        for b in range(a, 2**n):
            for c in range(b, 2**n):
                d = a + b - c
                if 0 <= d < 2**n:
                    E += sipser_function(n, a) + sipser_function(n, b) == sipser_function(n, c) + sipser_function(n, d)
    return E

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 10, 15, 20, 30, 40])
    instances_tested = n * (n - 1) * (n - 2) // 6
    E = additive_energy(n)
    conjecture_holds = E >= n**2
    counterexample = "" if conjecture_holds else f"Additive energy {E} is less than {n**2}"
    return {
        "metric_name": "additive_energy",
        "metric_value": E,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i - 1 for i in range(5, 8)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_E = sum(r["metric_value"] for r in results) / len(results)
    std_E = (sum((r["metric_value"] - mean_E)**2 for r in results) / len(results))**0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_E:.2f} std={std_E:.2f} support_fraction={support_fraction:.2f}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Additive energy less than n^2\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")