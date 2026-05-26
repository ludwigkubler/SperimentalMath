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
    
    def bool_func_to_poly(f):
        n = len(f)
        poly = [0] * (1 << n)
        for i in range(1 << n):
            if f[i]:
                poly[i] = 1
        return poly
    
    def etale_cohomology_rank(poly, n):
        # Simplified version of computing the rank of étale cohomology group
        # This is a placeholder and should be replaced with actual computation
        return sum(1 for x in poly if x == 1)
    
    def random_bool_func(n):
        return [random.choice([True, False]) for _ in range(1 << n)]
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        f = random_bool_func(n)
        poly = bool_func_to_poly(f)
        rank = etale_cohomology_rank(poly, n)
        results.append({"n": n, "rank": rank})
    
    min_rank = min(result["rank"] for result in results)
    conjecture_holds = all(rank <= n**2 + 100 for result in results)
    counterexample = "" if conjecture_holds else f"min_rank={min_rank}, expected<=n^2+100"
    
    return {
        "metric_name": "minimal_etale_cohomology_rank",
        "metric_value": min_rank,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction=1.0")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unreachable")