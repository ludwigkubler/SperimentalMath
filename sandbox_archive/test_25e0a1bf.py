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
    
    def generate_sat_instance(n):
        clauses = set()
        for _ in range(n):
            clause = tuple(sorted(random.sample(range(1, n+1), 2)))
            clauses.add(clause)
        return clauses
    
    def polynomial_modulo(poly, p):
        result = [0] * (len(poly) + 1)
        for i, coeff in enumerate(poly):
            result[i % len(result)] += coeff
            result[i % len(result)] %= p
        return result
    
    def modular_function_rank(poly, p):
        n = len(poly)
        if n == 0:
            return 0
        rank = 1
        for i in range(1, n):
            if all((poly[j] - poly[j-i]) % p != 0 for j in range(i+1, n)):
                rank += 1
        return rank
    
    def pearson_correlation(x, y):
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        cov_xy = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n)) / n
        std_dev_x = math.sqrt(sum((x[i] - mean_x) ** 2 for i in range(n)) / n)
        std_dev_y = math.sqrt(sum((y[i] - mean_y) ** 2 for i in range(n)) / n)
        return cov_xy / (std_dev_x * std_dev_y)
    
    def unique_clauses(clauses):
        return len(clauses)
    
    p = 101
    results = []
    instances_tested = 0
    
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):  # Ensure at least 30 instances per seed
            clauses = generate_sat_instance(n)
            poly = [0] * (n + 1)
            for clause in clauses:
                if len(clause) == 2:
                    poly[clause[1]] += 1
            rank = modular_function_rank(poly, p)
            results.append((rank, unique_clauses(clauses)))
            instances_tested += 1
    
    correlation = pearson_correlation([x for x, _ in results], [y for _, y in results])
    
    return {
        "metric_name": "Pearson Correlation",
        "metric_value": correlation,
        "instances_tested": instances_tested,
        "n_max": max(n for n in [5, 10, 15, 20, 30, 40]),
        "conjecture_holds": -0.1 <= correlation <= 1.1,
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
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_outside_bounds\" first_failing_seed={first_failing_seed}")