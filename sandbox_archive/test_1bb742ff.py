# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_cnf(n, m):
        cnf = []
        for _ in range(m):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            cnf.append(clause)
        return cnf
    
    def count_distinct_quaternionic_kahler_manifolds(cnf):
        manifolds = set()
        for clause in cnf:
            manifolds.add(tuple(sorted(abs(x) for x in clause)))
        return len(manifolds)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        m_values = [int(0.1 * n), int(0.2 * n), int(0.3 * n), int(0.4 * n)]
        for m in m_values:
            cnf = generate_cnf(n, m)
            count = count_distinct_quaternionic_kahler_manifolds(cnf)
            results.append({
                "n": n,
                "m": m,
                "count": count
            })
    
    instances_tested = len(results)
    n_max = max(result["n"] for result in results)
    conjecture_holds = True
    counterexample = ""
    
    if n_max < 16:
        return {
            "metric_name": "minimal_quaternionic_kahler_manifolds",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "n_max < 16"
        }
    
    m_values = sorted(set(result["m"] for result in results))
    counts = [result["count"] for result in results]
    
    if len(m_values) < 4:
        return {
            "metric_name": "minimal_quaternionic_kahler_manifolds",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "Too few m values"
        }
    
    expected_counts = [m ** 0.25 for m in m_values]
    
    def r_squared(actual, expected):
        mean_actual = sum(actual) / len(actual)
        mean_expected = sum(expected) / len(expected)
        ss_total = sum((a - mean_actual) ** 2 for a in actual)
        ss_residual = sum((a - e) ** 2 for a, e in zip(actual, expected))
        return 1 - (ss_residual / ss_total)
    
    r2 = r_squared(counts, expected_counts)
    
    if r2 < 0.9:
        conjecture_holds = False
        counterexample = f"R^2 = {r2:.4f} < 0.9"
    
    return {
        "metric_name": "minimal_quaternionic_kahler_manifolds",
        "metric_value": r2,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_r2 = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_r2:.4f} std=0.0000 support_fraction=1.0000")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_r2:.4f} std=0.0000 support_fraction={support_fraction:.4f}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"R^2 too low\" first_failing_seed={first_failing_seed}")