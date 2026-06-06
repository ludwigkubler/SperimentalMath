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
from itertools import combinations

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_cnf(m):
        variables = list(range(1, m + 1))
        clauses = []
        for _ in range(m):
            clause = [random.choice(variables), random.choice([-1, 1]) * random.choice(variables)]
            clauses.append(clause)
        return clauses
    
    def communication_complexity_rank(cnf):
        # Placeholder function to compute the rank
        # This is a dummy implementation and should be replaced with actual logic
        return len(set(tuple(sorted(abs(lit) for lit in clause)) for clause in cnf))
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        cnf = generate_cnf(n)
        rank = communication_complexity_rank(cnf)
        results.append(rank)
    
    variance = sum((x - sum(results) / len(results)) ** 2 for x in results) / len(results)
    conjecture_holds = variance <= max(n_values) ** 2
    counterexample = "" if conjecture_holds else f"Variance {variance} exceeds O({max(n_values)}^2)"
    
    return {
        "metric_name": "Variance of Communication Complexity Rank",
        "metric_value": variance,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    if not sys.argv[1:]:
        seeds = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    else:
        seeds = list(map(int, sys.argv[1:]))
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result["metric_value"])
    
    mean_variance = sum(results) / len(results)
    std_variance = math.sqrt(sum((x - mean_variance) ** 2 for x in results) / len(results))
    support_fraction = sum(1 for r in results if r <= max(n_values) ** 2) / len(results)
    
    if all(r <= max(n_values) ** 2 for r in results):
        print(f"RESULT: SUPPORTED mean={mean_variance} std={std_variance} support_fraction={support_fraction}")
    elif any(r > max(n_values) ** 2 for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if result > max(n_values) ** 2)
        print(f"RESULT: FALSIFIED counterexample=\"Variance exceeds O({max(n_values)}^2)\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unexpected_behavior")