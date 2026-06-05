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
    
    def generate_sat_instance(n):
        clauses = []
        for _ in range(n):
            variables = [random.choice([1, -1]) for _ in range(2)]
            clause = sum(variables)
            clauses.append(clause)
        return clauses
    
    def tropical_polynomial(clauses):
        degree = 0
        for clause in clauses:
            degree = max(degree, abs(clause))
        return degree
    
    def entropy(clauses):
        n = len(clauses)
        if n == 0: return 0
        counts = [clauses.count(c) for c in set(clauses)]
        probabilities = [c / n for c in counts]
        return -sum(p * math.log2(p) for p in probabilities if p > 0)
    
    def spearman_correlation(x, y):
        rank_x = {v: i+1 for i, v in enumerate(sorted(set(x)))}
        rank_y = {v: i+1 for i, v in enumerate(sorted(set(y)))}
        n = len(x)
        sum_diff_squares = sum((rank_x[x[i]] - rank_y[y[i]]) ** 2 for i in range(n))
        return 1 - (6 * sum_diff_squares) / (n * (n**2 - 1))
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    instances_tested = 0
    n_max = 0
    
    for n in n_values:
        for _ in range(5):
            clauses = generate_sat_instance(n)
            degree = tropical_polynomial(clauses)
            ent = entropy(clauses)
            results.append((degree, ent))
            instances_tested += 1
            n_max = max(n_max, n)
    
    if len(results) < 30:
        return {
            "metric_name": "Spearman's rank correlation",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "not_enough_instances"
        }
    
    degrees, ents = zip(*results)
    corr = spearman_correlation(degrees, ents)
    
    return {
        "metric_name": "Spearman's rank correlation",
        "metric_value": corr,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": corr >= 0.8,
        "counterexample": "" if corr >= 0.8 else f"Spearman's rank correlation = {corr}"
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
        mean_corr = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = 1.0
        result = f"RESULT: SUPPORTED mean={mean_corr} std=0 support_fraction={support_fraction}"
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        result = f"RESULT: FALSIFIED counterexample=\"Spearman's rank correlation < 0.8\" first_failing_seed={first_failing_seed}"
    else:
        result = "RESULT: INCONCLUSIVE insufficient_data"
    
    print(result)