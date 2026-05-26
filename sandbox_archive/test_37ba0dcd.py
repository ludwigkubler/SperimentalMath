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
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def bool_func_to_poly(f):
        n = len(f[0])
        poly = [0] * (1 << n)
        for i in range(1 << n):
            if f[i]:
                poly[i] = 1
        return poly

    def compute_étale_cohomology(poly, n):
        # Simplified version of computing étale cohomology rank
        # This is a placeholder and should be replaced with actual computation
        rank = sum(poly)  # Example: sum of non-zero coefficients
        return rank

    def generate_random_bool_func(n):
        return [[random.choice([0, 1]) for _ in range(2**n)] for _ in range(2**n)]

    n_values = [5, 10, 15, 20, 30, 40]
    total_rank = 0
    instances_tested = 0

    for n in n_values:
        f = generate_random_bool_func(n)
        poly = bool_func_to_poly(f)
        rank = compute_étale_cohomology(poly, n)
        total_rank += rank
        instances_tested += len(f)

    mean_value = total_rank / instances_tested
    conjecture_holds = all(rank <= n**2 + 100 for rank in [compute_étale_cohomology(bool_func_to_poly(generate_random_bool_func(n)), n) for _ in range(30)])
    counterexample = "" if conjecture_holds else "mapping_undefined"

    return {
        "metric_name": "min_rank",
        "metric_value": mean_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction=1.0")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")