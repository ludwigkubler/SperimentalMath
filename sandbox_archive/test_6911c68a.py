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
        for _ in range(2**n - 1):
            clause = [random.randint(-n, n-1) for _ in range(random.randint(1, n))]
            clauses.append(clause)
        return clauses
    
    def resolution(tree):
        while True:
            new_clauses = set()
            for i in range(len(tree)):
                for j in range(i + 1, len(tree)):
                    if -tree[i][0] in tree[j]:
                        new_clause = [lit for lit in tree[i] if lit != -tree[j][0]]
                        new_clause.extend([lit for lit in tree[j] if lit != -tree[i][0]])
                        new_clauses.add(tuple(sorted(new_clause)))
            if not new_clauses:
                break
            tree.extend(list(new_clauses))
        return len(tree)
    
    def euler_characteristic(n):
        return n
    
    def width(tree):
        return resolution(tree)
    
    metrics = []
    instances_tested = 0
    n_max = 5
    
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):  # Ensure at least 30 instances per seed
            cnf = generate_cnf(n)
            tree = [(lit,) for lit in cnf]
            chi = euler_characteristic(n)
            w = width(tree)
            metrics.append((chi, w))
            instances_tested += 1
            n_max = max(n_max, n)
    
    if not metrics:
        return {
            "metric_name": "Euler characteristic vs Width",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    chi_values = [m[0] for m in metrics]
    w_values = [m[1] for m in metrics]
    correlation_coefficient = sum((chi - mean(chi_values)) * (w - mean(w_values)) for chi, w in zip(chi_values, w_values)) / (len(metrics) * std_dev(chi_values) * std_dev(w_values))
    difference_mean = abs(mean(chi_values) - 0.5 * mean(w_values))
    
    return {
        "metric_name": "Euler characteristic vs Width",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": correlation_coefficient >= 0.8 and difference_mean <= 3,
        "counterexample": ""
    }

def mean(values):
    return sum(values) / len(values)

def std_dev(values):
    avg = mean(values)
    return math.sqrt(sum((x - avg) ** 2 for x in values) / len(values))

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [random.getrandbits(32) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = mean([r["metric_value"] for r in results if r["metric_value"] is not None])
    std_value = std_dev([r["metric_value"] for r in results if r["metric_value"] is not None])
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=unknown")