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
    
    def generate_instance(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def clause_indicator_polynomial(instance):
        n = len(instance)
        poly = [0] * (n + 1)
        for i in range(2**n):
            if sum(instance[j] for j in range(n) if i & (1 << j)) % 2 == 1:
                poly[i] += 1
        return poly
    
    def twisted_quotient_algebra(poly, n):
        algebra = []
        for i in range(2**n):
            row = [0] * (2**n)
            for j in range(2**n):
                if sum(poly[k] for k in range(n) if i & (1 << k)) % 2 == poly[j]:
                    row[j] += 1
            algebra.append(row)
        return algebra
    
    def min_rank(algebra):
        n = len(algebra)
        rank = 0
        for row in algebra:
            if any(row[i] != 0 for i in range(n)):
                rank += 1
        return rank
    
    def dpll_proof_length(instance):
        # Simplified DPLL algorithm to estimate proof length
        stack = [(instance, [])]
        while stack:
            instance, path = stack.pop()
            if all(x == 0 for x in instance):
                return len(path)
            i = next(j for j, x in enumerate(instance) if x != 0)
            stack.append((instance[:i] + [0] + instance[i+1:], path + ['F']))
            stack.append((instance[:i] + [1] + instance[i+1:], path + ['T']))
        return float('inf')
    
    def spearman_correlation(rho, l):
        n = len(rho)
        rank_rho = sorted(range(n), key=lambda i: rho[i])
        rank_l = sorted(range(n), key=lambda i: l[i])
        sum_diff_squared = sum((rank_rho[i] - rank_l[i]) ** 2 for i in range(n))
        return 1 - (6 * sum_diff_squared) / (n * (n**2 - 1))
    
    n_values = [5, 10, 15, 20, 30, 40]
    results_rho = []
    results_l = []
    
    for n in n_values:
        instances_tested = 30
        for _ in range(instances_tested):
            instance = generate_instance(n)
            poly = clause_indicator_polynomial(instance)
            algebra = twisted_quotient_algebra(poly, n)
            rho = min_rank(algebra)
            l = dpll_proof_length(instance)
            results_rho.append(rho)
            results_l.append(l)
    
    if len(results_rho) == 0 or len(results_l) == 0:
        return {
            "metric_name": "Spearman's Rank Correlation",
            "metric_value": None,
            "instances_tested": instances_tested,
            "conjecture_holds": False,
            "counterexample": "empty_results"
        }
    
    correlation = spearman_correlation(results_rho, results_l)
    return {
        "metric_name": "Spearman's Rank Correlation",
        "metric_value": correlation,
        "instances_tested": instances_tested * len(n_values),
        "conjecture_holds": correlation > 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else list(range(2, 30*40+2, 2))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"not_enough_support\" first_failing_seed={first_failing_seed}")