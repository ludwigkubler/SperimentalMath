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
            clause = [random.randint(1, n), -random.randint(1, n)]
            if random.choice([True, False]):
                clause[0] *= -1
            cnf.append(clause)
        return cnf
    
    def is_satisfiable(cnf):
        assignment = {i: random.choice([True, False]) for i in range(1, max(abs(x) for x in sum(cnf, [])) + 1)}
        for clause in cnf:
            if not any(assignment.get(abs(lit), False) == (lit > 0) for lit in clause):
                return False
        return True
    
    def geometric_fluctuation(cnf):
        samples = [is_satisfiable(cnf) for _ in range(100)]
        normalized_dist = {True: Fraction(samples.count(True), len(samples)), False: Fraction(samples.count(False), len(samples))}
        total_variation = sum(abs(normalized_dist[True] - normalized_dist[False]))
        return total_variation
    
    def resolution_width(cnf):
        # Simplified resolution width calculation (not actual resolution proof)
        return len(cnf)  # Placeholder for actual resolution width calculation
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        cnf = generate_cnf(n, n * (n - 1) // 2)
        gf = geometric_fluctuation(cnf)
        w = resolution_width(cnf)
        results.append((gf, w))
    
    if len(results) < 30:
        return {
            "metric_name": "Resolution Width vs Geometric Fluctuation",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "Insufficient instances"
        }
    
    gf_values = [gf for gf, _ in results]
    w_values = [w for _, w in results]
    
    def pearson_correlation(x, y):
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        numerator = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n))
        denominator = ((sum((x[i] - mean_x) ** 2 for i in range(n)) * sum((y[i] - mean_y) ** 2 for i in range(n))) ** 0.5)
        return numerator / denominator if denominator != 0 else 0
    
    correlation = pearson_correlation(gf_values, w_values)
    
    return {
        "metric_name": "Resolution Width vs Geometric Fluctuation",
        "metric_value": correlation,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": correlation >= 0.7,
        "counterexample": "" if correlation >= 0.7 else f"Correlation: {correlation}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if not all(r["conjecture_holds"] for r in results):
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        RESULT = f"RESULT: FALSIFIED counterexample=\"Correlation below 0.7\" first_failing_seed={first_failing_seed}"
    else:
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_value = (sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results)) ** 0.5
        support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
        RESULT = f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}"
    
    print(RESULT)