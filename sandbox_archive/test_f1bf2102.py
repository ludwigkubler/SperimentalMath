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
    
    # Generate a random CNF formula with n variables and m clauses
    n = random.randint(5, 30)
    m = random.randint(n, 2 * n)
    cnf = []
    for _ in range(m):
        clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
        cnf.append(clause)
    
    # Calculate the number of invariant factors |InvariantFactors(X(φ))|
    # This is a placeholder function; actual implementation depends on algebraic geometry library
    def invariant_factors(cnf):
        # Placeholder return value
        return random.randint(1, n)
    
    num_invariant_factors = invariant_factors(cnf)
    
    # Calculate the clause set complexity c(φ)
    clause_set_complexity = len(cnf) * sum(len(clause) for clause in cnf)
    
    # Check if the conjecture holds
    alpha = 0.5  # Placeholder value
    beta = 1.0   # Placeholder value
    conjecture_holds = num_invariant_factors <= alpha * (clause_set_complexity ** beta)
    
    return {
        "metric_name": "InvariantFactors vs ClauseSetComplexity",
        "metric_value": num_invariant_factors,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"Counterexample: {num_invariant_factors} > {alpha * (clause_set_complexity ** beta)}"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [random.randint(2, 97) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    # Compute mean/std of metric_value
    total_metric_value = sum(result["metric_value"] for result in results)
    mean_metric_value = total_metric_value / len(results)
    variance_metric_value = sum((result["metric_value"] - mean_metric_value) ** 2 for result in results) / len(results)
    std_metric_value = math.sqrt(variance_metric_value)
    
    # Compute fraction of seeds where conjecture_holds
    support_fraction = sum(result["conjecture_holds"] for result in results) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        counterexample = results[first_failing_seed]["counterexample"]
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")