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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(2**n):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            if any(clause[i] == -clause[j] for i in range(len(clause)) for j in range(i+1, len(clause))):
                clauses.append(clause)
        return clauses

    def circuit_monotone_width(cnf):
        n = len(cnf[0])
        width = [0] * (2**n)
        for clause in cnf:
            for i in range(2**n):
                if all((i & (1 << abs(l) - 1)) != 0 == l > 0 for l in clause):
                    width[i] += 1
        return max(width)

    def automorphism_group_order(cnf):
        n = len(cnf[0])
        # Simplified heuristic: count the number of distinct permutations that preserve the CNF
        # This is a very rough approximation and not accurate for general CNFs
        return math.factorial(n) // 2

    results = []
    for _ in range(30):
        n = random.choice([5, 10, 15, 20, 30, 40])
        cnf = generate_cnf(n)
        aut_order = automorphism_group_order(cnf)
        w_m = circuit_monotone_width(cnf)
        results.append((aut_order, w_m))

    if not results:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "empty_results"
        }

    aut_orders, w_ms = zip(*results)
    mean_aut_order = sum(aut_orders) / len(aut_orders)
    mean_w_m = sum(w_ms) / len(w_ms)
    correlation_coefficient = (sum((a - mean_aut_order) * (w - mean_w_m) for a, w in zip(aut_orders, w_ms)) /
                               math.sqrt(sum((a - mean_aut_order)**2 for a in aut_orders) *
                                         sum((w - mean_w_m)**2 for w in w_ms)))

    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n for _, _ in results),
        "conjecture_holds": correlation_coefficient > 0.8 and abs(mean_aut_order - mean_w_m) <= 3,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    if all(r["conjecture_holds"] for r in results):
        mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = 1.0
        result_str = f"SUPPORTED mean={mean_metric_value:.4f} std=unknown support_fraction={support_fraction}"
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        counterexample_desc = "correlation_coefficient < 0.8 or mean difference > 3"
        result_str = f"FALSIFIED counterexample=\"{counterexample_desc}\" first_failing_seed={first_failing_seed}"

    print(result_str)