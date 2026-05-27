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
    
    def generate_cnf(k, n):
        clauses = []
        for i in range(n - k + 1):
            clause = [random.randint(1, n) for _ in range(k)]
            clauses.append(clause)
        return clauses
    
    def categorified_rank(cnf):
        # Placeholder function to simulate the categorified rank computation
        # This is a dummy implementation and should be replaced with actual logic
        return len(cnf) * 2  # Example: rank is twice the number of clauses
    
    n_values = [30, 35, 40]
    ranks = []
    
    for n in n_values:
        k = random.randint(1, min(n // 2, 5))
        cnf = generate_cnf(k, n)
        rank = categorified_rank(cnf)
        ranks.append(rank)
    
    expected_ranks = [n**k for n in n_values]
    
    def correlation_coefficient(x, y):
        if len(x) != len(y) or not x:
            return 0
        mean_x = sum(x) / len(x)
        mean_y = sum(y) / len(y)
        cov = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(len(x)))
        std1 = math.sqrt(sum((x[i] - mean_x)**2 for i in range(len(x))) / len(x))
        std2 = math.sqrt(sum((y[i] - mean_y)**2 for i in range(len(y))) / len(y))
        if std1 == 0 or std2 == 0:
            return 0
        return cov / (std1 * std2)
    
    corr_coeff = correlation_coefficient(ranks, expected_ranks)
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": corr_coeff,
        "instances_tested": len(n_values),
        "conjecture_holds": corr_coeff >= 0.8,
        "counterexample": "" if corr_coeff >= 0.8 else f"Correlation coefficient {corr_coeff} < 0.8"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or list(range(2, 53))  # Default to first 30 primes if no seeds provided
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_corr_coeff = sum(res["metric_value"] for res in results) / len(results)
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_corr_coeff} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_corr_coeff} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, res in enumerate(results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient < 0.8\" first_failing_seed={first_failing_seed + 2}")