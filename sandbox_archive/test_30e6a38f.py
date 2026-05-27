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
    
    def generate_cnf(n, k):
        variables = list(range(n))
        clauses = []
        for _ in range(k):
            clause = random.sample(variables, 2)
            clauses.append(clause)
        return clauses
    
    def categorified_boolean_algebra_size(cnf):
        n = len(cnf[0])
        rank = 1
        for clause in cnf:
            rank *= (n - len(clause) + 1)
        return rank
    
    n_values = [30, 35, 40]
    results = []
    
    for n in n_values:
        cnf = generate_cnf(n, k=2)
        rank = categorified_boolean_algebra_size(cnf)
        expected_rank = n**2
        results.append({
            "n": n,
            "rank": rank,
            "expected_rank": expected_rank
        })
    
    mean_rank = sum(result["rank"] for result in results) / len(results)
    mean_expected_rank = sum(result["expected_rank"] for result in results) / len(results)
    correlation_coefficient = (sum((result["rank"] - mean_rank) * (result["expected_rank"] - mean_expected_rank) for result in results) /
                               math.sqrt(sum((result["rank"] - mean_rank)**2 for result in results) *
                                         sum((result["expected_rank"] - mean_expected_rank)**2 for result in results)))
    
    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "conjecture_holds": abs(correlation_coefficient) >= 0.8,
        "counterexample": "" if abs(correlation_coefficient) >= 0.8 else "correlation_coefficient < 0.8"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_correlation = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if abs(result["metric_value"]) >= 0.8) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_correlation} std=NOT_COMPUTABLE support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if abs(result["metric_value"]) < 0.8)
        print(f"RESULT: FALSIFIED counterexample='correlation_coefficient < 0.8' first_failing_seed={first_failing_seed}")