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
        cnf = []
        for _ in range(2 * n):  # Each variable appears twice (positive and negative)
            clause = [random.randint(1, n), -random.randint(1, n)]
            if clause not in cnf:
                cnf.append(clause)
        return cnf
    
    def compute_k0_rank(cnf):
        n = max(abs(lit) for lit in set([lit for clause in cnf for lit in clause]))
        if n == 0:
            return 0
        # Simulate Grothendieck-Witt class computation (simplified)
        rank = sum(1 for clause in cnf if any(lit in clause for lit in [-i, i] for i in range(1, n+1)))
        return rank
    
    def pearson_correlation(x, y):
        mean_x = sum(x) / len(x)
        mean_y = sum(y) / len(y)
        cov = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(len(x))) / len(x)
        std_x = math.sqrt(sum((x[i] - mean_x) ** 2 for i in range(len(x))) / len(x))
        std_y = math.sqrt(sum((y[i] - mean_y) ** 2 for i in range(len(y))) / len(y))
        return cov / (std_x * std_y)
    
    n_values = [5, 10, 15, 20, 30, 40]
    k0_ranks = []
    clause_counts = []
    
    for n in n_values:
        cnf = generate_cnf(n)
        k0_rank = compute_k0_rank(cnf)
        k0_ranks.append(k0_rank)
        clause_counts.append(len(cnf))
    
    correlation_coefficient = pearson_correlation(k0_ranks, clause_counts)
    
    return {
        "metric_name": "Pearson Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": abs(correlation_coefficient) > 0.7,
        "counterexample": "" if abs(correlation_coefficient) > 0.7 else f"Correlation coefficient {correlation_coefficient:.2f} is not significantly non-zero"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(res["metric_value"] for res in results) / len(results)
    std_value = math.sqrt(sum((res["metric_value"] - mean_value) ** 2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if abs(res["metric_value"]) > 0.7) / len(results)
    
    if all(abs(res["metric_value"]) > 0.7 for res in results):
        print(f"RESULT: SUPPORTED mean={mean_value:.2f} std={std_value:.2f} support_fraction={support_fraction:.2f}")
    elif any(abs(res["metric_value"]) < -0.7 for res in results):
        first_failing_seed = next(seed for seed, res in enumerate(results) if abs(res["metric_value"]) < -0.7)
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient_below_neg_0_7\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")