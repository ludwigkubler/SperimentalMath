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

def sipser_function(n, i):
    return sum(1 if (i & (1 << j)) else 0 for j in range(n) if i % (2 * (j + 1)) == 0)

def additive_energy(n):
    E = 0
    for a in range(2**n):
        for b in range(2**n):
            for c in range(2**n):
                for d in range(2**n):
                    if sipser_function(n, a) + sipser_function(n, b) == sipser_function(n, c) + sipser_function(n, d):
                        E += 1
    return E

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 10, 15, 20, 30, 40])
    E = additive_energy(n)
    expected_E = n**2
    metric_value = E / expected_E if expected_E != 0 else float('inf')
    conjecture_holds = abs(metric_value - 1) < 0.1
    counterexample = "" if conjecture_holds else f"n={n}, E={E}, expected_E={expected_E}"
    return {
        "metric_name": "Additive Energy Ratio",
        "metric_value": metric_value,
        "instances_tested": n**4,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 8)]  # Default to first 30 primes if no seeds provided
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Additive energy does not scale quadratically\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient data or conflicting results")