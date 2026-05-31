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
    
    def generate_cnf(k, m):
        cnf = []
        for _ in range(m):
            clause = [random.choice([-i, i]) for i in range(1, k+1)]
            cnf.append(clause)
        return cnf
    
    def compute_clause_complexity(cnf):
        return sum(len(clause) for clause in cnf)
    
    # Placeholder function to simulate computing p-adic Hodge theory rank
    def compute_p_adic_hodge_rank(cnf):
        # This is a dummy implementation. Replace with actual computation.
        return len(cnf)
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        cnf = generate_cnf(n, random.randint(1, 40))
        clause_complexity = compute_clause_complexity(cnf)
        p_adic_hodge_rank = compute_p_adic_hodge_rank(cnf)
        results.append((clause_complexity, p_adic_hodge_rank))
    
    if not results:
        return {
            "metric_name": "p-adic Hodge Theory Rank",
            "metric_value": 0,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    clause_complexities = [r[0] for r in results]
    p_adic_hodge_ranks = [r[1] for r in results]
    
    mean_C = sum(clause_complexities) / len(clause_complexities)
    mean_h = sum(p_adic_hodge_ranks) / len(p_adic_hodge_ranks)
    
    covariance = sum((clause_complexities[i] - mean_C) * (p_adic_hodge_ranks[i] - mean_h) for i in range(len(results))) / len(results)
    variance_C = sum((clause_complexities[i] - mean_C) ** 2 for i in range(len(results))) / len(results)
    
    if variance_C == 0:
        return {
            "metric_name": "p-adic Hodge Theory Rank",
            "metric_value": 0,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    correlation_coefficient = covariance / (mean_C * variance_C)
    
    return {
        "metric_name": "p-adic Hodge Theory Rank",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n for _, n in results),
        "conjecture_holds": abs(correlation_coefficient) >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_value = sum(result["metric_value"] for result in results) / len(results)
        std_value = (sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results)) ** 0.5
        support_fraction = 1.0
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        counterexample = "mapping_undefined"
        mean_value = sum(result["metric_value"] for result in results) / len(results)
        std_value = (sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results)) ** 0.5
        support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    print(f"RESULT: {'SUPPORTED' if all(result['conjecture_holds'] for result in results) else 'FALSIFIED'} mean={mean_value} std={std_value} support_fraction={support_fraction}")