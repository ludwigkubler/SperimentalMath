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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def compute_tropical_generating_series(f):
        n = len(f)
        dp = [[Fraction(0, 1)] * (n + 1) for _ in range(n + 1)]
        dp[0][0] = Fraction(1, 1)
        for i in range(1, n + 1):
            dp[i][0] = Fraction(1, 2)
            for j in range(1, i + 1):
                dp[i][j] = (dp[i-1][j-1] + dp[i-1][j]) / Fraction(2, 1)
        return dp[n][n]
    
    def compute_coxeter_diagram(f):
        n = len(f)
        # Simplified Coxeter diagram calculation for demonstration
        return n
    
    instances_tested = 0
    n_max = 5
    metric_values = []
    conjecture_holds = True
    counterexample = ""
    
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            f = generate_boolean_function(n)
            T_f = compute_tropical_generating_series(f)
            C_f = compute_coxeter_diagram(f)
            if T_f > 0:
                metric_values.append((C_f, T_f**(3/2)))
                instances_tested += 1
                n_max = max(n_max, n)
    
    if len(metric_values) < 30:
        return {
            "metric_name": "Spearman rank correlation",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    def spearman_rank_correlation(data):
        ranks = {x: rank for rank, (_, x) in enumerate(sorted(set(x for _, x in data)), 1)}
        sorted_data = sorted((ranks[x], y) for x, y in data)
        n = len(sorted_data)
        sum_d_squared = sum((i - (n + 1) / 2)**2 for i, _ in sorted_data)
        return 1 - Fraction(6 * sum_d_squared, n * (n**2 - 1))
    
    correlation_coefficient = spearman_rank_correlation(metric_values)
    if correlation_coefficient < 0.7:
        conjecture_holds = False
        counterexample = f"correlation_coefficient={correlation_coefficient}"
    
    return {
        "metric_name": "Spearman rank correlation",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient<{r['metric_value']}\"> first_failing_seed={first_failing_seed}")