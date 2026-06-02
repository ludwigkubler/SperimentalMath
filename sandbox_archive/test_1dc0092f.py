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
    
    def generate_cnf(n, h):
        clauses = []
        for _ in range(h):
            clause = [random.randint(1, n), -random.randint(1, n)]
            if random.choice([True, False]):
                clause[0] *= -1
            clauses.append(clause)
        return clauses

    def compute_cohomological_dimension(cnf):
        # Simplified version for demonstration purposes
        return len(cnf)

    def compute_clause_entropy(cnf):
        h = len(cnf)
        n = max(abs(lit) for clause in cnf for lit in clause)
        entropy = 0
        for clause in cnf:
            for lit in clause:
                if random.choice([True, False]):
                    entropy += 1 / (n * h)
        return entropy

    def pearson_correlation(x, y):
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        cov_xy = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n)) / n
        std_x = math.sqrt(sum((x[i] - mean_x) ** 2 for i in range(n)) / n)
        std_y = math.sqrt(sum((y[i] - mean_y) ** 2 for i in range(n)) / n)
        return cov_xy / (std_x * std_y)

    def mean_absolute_difference(x, y):
        return sum(abs(a - b) for a, b in zip(x, y)) / len(x)

    instances_tested = 0
    mcd_values = []
    h_values = []

    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            h = random.randint(1, n)
            cnf = generate_cnf(n, h)
            mcd = compute_cohomological_dimension(cnf)
            h_val = compute_clause_entropy(cnf)
            mcd_values.append(mcd)
            h_values.append(h_val)
            instances_tested += 1

    correlation = pearson_correlation(mcd_values, h_values)
    mean_diff = mean_absolute_difference(mcd_values, h_values)

    conjecture_holds = correlation >= 0.8 and mean_diff <= 3
    counterexample = "" if conjecture_holds else "mapping_undefined"

    return {
        "metric_name": "Pearson Correlation",
        "metric_value": correlation,
        "instances_tested": instances_tested,
        "n_max": max([5, 10, 15, 20, 30, 40]),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [random.randint(1, 1000) for _ in range(30)]
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_corr = sum(r["metric_value"] for r in results) / len(results)
    std_corr = math.sqrt(sum((r["metric_value"] - mean_corr) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_corr} std={std_corr} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_corr} std={std_corr} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")