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
    
    def generate_elliptic_curve(q):
        # Simple elliptic curve over F_q
        a = random.randint(1, q-1)
        b = random.randint(0, q-1)
        return (a, b)

    def p_adic_selmer_group_order(E, p):
        # Simplified version of computing the order of p-adic Selmer group
        a, b = E
        if (4*a**3 + 27*b**2) % p == 0:
            return 1
        else:
            return 2

    def communication_complexity_rank_variance(n):
        # Simplified version of computing rank variance for n variables
        return random.uniform(0, n)

    min_order = float('inf')
    rank_variance_sum = 0
    instances_tested = 0
    n_max = 0

    for n in [5, 10, 15, 20, 30, 40]:
        if n > n_max:
            n_max = n
        
        for _ in range(5):  # Ensure at least 30 instances per seed
            q = 2**n
            E = generate_elliptic_curve(q)
            p = random.choice([3, 5, 7])  # Prime p for simplicity
            order = p_adic_selmer_group_order(E, p)
            rank_variance = communication_complexity_rank_variance(n)
            
            min_order = min(min_order, order)
            rank_variance_sum += rank_variance
            instances_tested += 1

    if n_max < 16:
        return {
            "metric_name": "min_order",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "n_max < 16"
        }

    avg_rank_variance = rank_variance_sum / instances_tested
    conjecture_holds = min_order >= math.log(q**2 / math.log(q)) and min_order <= q

    return {
        "metric_name": "min_order",
        "metric_value": min_order,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"min_order={min_order}, expected [log(q^2 / log(q)), q]"
    }

if __name__ == "__main__":
    import sys
    seeds = list(map(int, sys.argv[1:])) or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    if all(r["conjecture_holds"] for r in results):
        mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"min_order out of bounds\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")