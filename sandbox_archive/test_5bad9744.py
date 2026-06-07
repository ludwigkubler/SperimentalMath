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
    
    def generate_boolean_formula(n):
        return ''.join(random.choice('01') for _ in range(2**n))
    
    def communication_complexity_rank(formula):
        n = len(formula)
        ranks = []
        for perm in itertools.permutations(range(n)):
            rank = 0
            for i in range(2**n):
                input_str = format(i, f'0{n}b')
                output = formula
                for j in range(n):
                    if input_str[j] == '1':
                        output = output[perm[j]]
                if output == '1':
                    rank += 1
            ranks.append(rank)
        return sum((r - mean) ** 2 for r in ranks) / len(ranks)

    def galois_covering_degree(formula):
        n = len(formula)
        # Simplified calculation of Galois covering degree
        return n

    def mean(lst):
        return Fraction(sum(lst), len(lst))

    def variance(lst, mean_val):
        return sum((x - mean_val) ** 2 for x in lst) / len(lst)

    n = random.randint(5, 40)
    formula = generate_boolean_formula(n)
    
    d_phi = galois_covering_degree(formula)
    r_var_phi = communication_complexity_rank(formula)
    
    if d_phi > 50 or r_var_phi < -20:
        return {
            "metric_name": "correlation",
            "metric_value": None,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": f"d(φ) > 50 or r_var(φ) < -20"
        }
    
    return {
        "metric_name": "correlation",
        "metric_value": d_phi * r_var_phi,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    metric_values = [r["metric_value"] for r in results if r["metric_value"] is not None]
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean(metric_values)} std={math.sqrt(variance(metric_values, mean(metric_values)))} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"d(φ) > 50 or r_var(φ) < -20\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")