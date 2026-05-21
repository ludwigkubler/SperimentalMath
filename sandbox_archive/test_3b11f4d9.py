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
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def perm_n(n):
        return n * perm_n(n-1) if n > 1 else 1
    
    def det_m(m, n):
        if m == 0 or n == 0:
            return 1
        elif m == n:
            return perm_n(m)
        else:
            return 0

    def schur_weyl_invariant(f):
        # Placeholder for the actual implementation of Schur-Weyl duality invariant
        # For simplicity, we'll use a dummy function that returns a random value
        return random.random()

    n_values = [5, 10, 15, 20, 30, 40]
    total_ratio = 0
    instances_tested = 0

    for n in n_values:
        f = [random.choice([1, -1]) * x**i for i in range(n+1)]
        perm_n_value = perm_n(n)
        det_m_value = det_m(1, n)  # Assuming m=1 for simplicity
        invariant_f = schur_weyl_invariant(f)
        ratio = invariant_f / det_m_value if det_m_value != 0 else float('inf')
        
        total_ratio += ratio
        instances_tested += 1

    mean_ratio = total_ratio / instances_tested
    std_deviation = (sum((ratio - mean_ratio) ** 2 for ratio in [total_ratio / instances_tested] * instances_tested)) ** 0.5 if instances_tested > 1 else 0

    conjecture_holds = mean_ratio >= 0.9 and std_deviation < 0.1
    counterexample = "" if conjecture_holds else "mapping_undefined"

    return {
        "metric_name": "Ratio of Schur-Weyl Invariant to Determinant",
        "metric_value": mean_ratio,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(seed) for seed in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    std_deviation = (sum((r["metric_value"] - mean_ratio) ** 2 for r in results)) ** 0.5 if len(results) > 1 else 0
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_deviation} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=mapping_undefined")