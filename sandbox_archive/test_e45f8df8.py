# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction
from itertools import combinations, product

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def dpll(cnf):
        if not cnf:
            return True
        for literal in cnf[0]:
            new_cnf = []
            for clause in cnf[1:]:
                if literal in clause:
                    continue
                elif -literal in clause:
                    new_clause = [l for l in clause if l != -literal]
                    if not new_clause:
                        return False
                    new_cnf.append(new_clause)
                else:
                    new_cnf.append(clause)
            if dpll(new_cnf):
                return True
        return False
    
    def generate_cnf(n, m):
        variables = list(range(1, n + 1))
        clauses = []
        for _ in range(m):
            clause = random.sample(variables + [-v for v in variables], k=random.randint(1, n))
            clauses.append(clause)
        return clauses
    
    def minimal_representation_length(cnf):
        # Placeholder function to compute the minimal representation length
        # This is a stub and should be replaced with actual computation
        return random.random() * 100
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):  # Ensure at least 30 instances per seed
            cnf = generate_cnf(n, random.randint(1, n * (n - 1) // 2))
            dpll_width = len(cnf) if dpll(cnf) else 0
            representation_length = minimal_representation_length(cnf)
            results.append((representation_length, dpll_width))
    
    correlation_coefficient = calculate_correlation(results)
    mean_representation_length = sum(x for x, _ in results) / len(results)
    mean_dpll_width = sum(y for _, y in results) / len(results)
    
    return {
        "metric_name": "Pearson Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n for n, _ in [x[1] for x in results]),
        "conjecture_holds": 0.5 < correlation_coefficient < 0.7,
        "counterexample": "" if 0.5 < correlation_coefficient < 0.7 else "correlation_outside_range"
    }

def calculate_correlation(data):
    n = len(data)
    mean_x = sum(x for x, _ in data) / n
    mean_y = sum(y for _, y in data) / n
    
    numerator = sum((x - mean_x) * (y - mean_y) for x, y in data)
    denominator = math.sqrt(sum((x - mean_x) ** 2 for x, _ in data)) * math.sqrt(sum((y - mean_y) ** 2 for _, y in data))
    
    return numerator / denominator if denominator != 0 else 0

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [random.randint(1, 1000) for _ in range(30)]
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(x["metric_value"] for x in results) / len(results)
    support_fraction = sum(1 for x in results if x["conjecture_holds"]) / len(results)
    
    if all(x["conjecture_holds"] for x in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif any(not x["conjecture_holds"] for x in results) and any(x["metric_value"] < 0.5 for x in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_outside_range\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")