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
    
    def generate_random_sat_instance(n, d):
        clauses = []
        for _ in range(d):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            if all(clause[i] != -clause[j] for j in range(i)):
                clauses.append(clause)
        return clauses
    
    def compute_root_lattice_symmetric_entropy(clauses):
        n = len(clauses[0])
        # Simplified computation of symmetric entropy (placeholder)
        return n * math.log2(n)
    
    def compute_subset_entropy(clauses):
        if not clauses:
            return 0
        n = len(clauses[0])
        subset = random.sample(range(1, n + 1), n // 2)
        # Simplified computation of subset entropy (placeholder)
        return sum(math.log2(i) for i in subset)
    
    def compute_spearman_correlation(data):
        if len(data) < 2:
            return 0
        ranks = {x: rank for rank, x in enumerate(sorted(set(data)), start=1)}
        n = len(data)
        numerator = sum((ranks[x] - (n + 1) / 2) ** 2 for x in data)
        denominator = n * (n**2 - 1) / 12
        return 1 - (6 * numerator) / denominator
    
    results = []
    for _ in range(30):
        n = random.choice([5, 10, 15, 20, 30, 40])
        d = random.randint(1, min(n * 2, 100))
        clauses = generate_random_sat_instance(n, d)
        se = compute_root_lattice_symmetric_entropy(clauses)
        sh = compute_subset_entropy(clauses)
        results.append((se, sh))
    
    if not results:
        return {
            "metric_name": "Spearman's rank correlation",
            "metric_value": 0,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "empty_results"
        }
    
    se_values, sh_values = zip(*results)
    correlation_coefficient = compute_spearman_correlation(sh_values)
    p_value = 1  # Placeholder for actual p-value calculation
    
    return {
        "metric_name": "Spearman's rank correlation",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(len(clauses[0]) for clauses, _ in results),
        "conjecture_holds": correlation_coefficient > 0 and p_value <= 0.05,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_value = sum(result["metric_value"] for result in results) / len(results)
        std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")