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

def generate_cnf(n):
    cnf = []
    for _ in range(random.randint(1, n * 2)):
        clause = []
        for i in range(n):
            clause.append(random.choice([f'x{i}', f'-x{i}']))
        cnf.append(clause)
    return cnf

def calculate_entropy(cnf):
    total_clauses = len(cnf)
    counts = {}
    for clause in cnf:
        key = tuple(sorted(clause))
        if key in counts:
            counts[key] += 1
        else:
            counts[key] = 1
    entropy = 0.0
    for count in counts.values():
        p = Fraction(count, total_clauses)
        entropy -= p * math.log2(p)
    return entropy

def minimal_p_adic_valuation(x):
    if x == 0:
        return 0
    while x % 2 == 0:
        x //= 2
    return int(math.log2(x))

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        cnf = generate_cnf(n)
        entropy = calculate_entropy(cnf)
        p_adic_valuation = minimal_p_adic_valuation(entropy)
        results.append((n, p_adic_valuation))
    
    if len(results) < 30:
        return {
            "metric_name": "p-adic Valuation",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(n for n, _ in results),
            "conjecture_holds": False,
            "counterexample": "not_enough_instances"
        }
    
    n_values = [n for n, _ in results]
    p_adic_valuations = [p for _, p in results]
    
    mean_n = sum(n_values) / len(n_values)
    mean_p_adic_valuation = sum(p_adic_valuations) / len(p_adic_valuations)
    
    covariance = 0
    n_variance = 0
    p_adic_variance = 0
    
    for i in range(len(n_values)):
        covariance += (n_values[i] - mean_n) * (p_adic_valuations[i] - mean_p_adic_valuation)
        n_variance += (n_values[i] - mean_n) ** 2
        p_adic_variance += (p_adic_valuations[i] - mean_p_adic_valuation) ** 2
    
    correlation_coefficient = covariance / math.sqrt(n_variance * p_adic_variance)
    
    return {
        "metric_name": "p-adic Valuation",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n for n, _ in results),
        "conjecture_holds": correlation_coefficient > 0.95 and all(corr >= 0.5 for corr in [correlation_coefficient]),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = list(map(int, sys.argv[1:])) or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
    
    results = [run_trial(seed) for seed in seeds]
    
    supported_count = sum(1 for r in results if r["conjecture_holds"])
    support_fraction = supported_count / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={sum(r['metric_value'] for r in results) / len(results)} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")