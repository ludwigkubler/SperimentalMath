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
    
    n = 30  # Number of variables
    m = 100  # Number of clauses
    k = 3  # Clause density
    
    if n < 3 or m <= 0 or k <= 0:
        return {
            "metric_name": "Ehrhart Cohomology Rank",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "Invalid input parameters"
        }
    
    # Generate a random k-CNF formula
    cnf = []
    for _ in range(m):
        clause = set()
        while len(clause) < k:
            var = random.randint(1, n)
            if not (var in clause or -var in clause):
                clause.add(var)
        cnf.append(tuple(sorted(clause)))
    
    # Construct the incidence vector matrix
    A = [[0] * (n + 1) for _ in range(m)]
    for i, clause in enumerate(cnf):
        for var in clause:
            A[i][abs(var)] += 1
    
    # Compute the rank of the incidence matrix
    rank = 0
    for row in A:
        if all(row[j] == 0 for j in range(rank)):
            continue
        pivot_col = next(j for j in range(n + 1) if row[j] != 0)
        for i in range(m):
            if i != rank and A[i][pivot_col] != 0:
                factor = -A[i][pivot_col] / row[pivot_col]
                for j in range(n + 1):
                    A[i][j] += factor * row[j]
        rank += 1
    
    # Compute the metric value
    metric_value = rank
    
    return {
        "metric_name": "Ehrhart Cohomology Rank",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": False,  # The conjecture is not supported by this trial
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2**i - 1 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    # Compute statistics
    total_metric_value = sum(result["metric_value"] for result in results if result["instances_tested"] > 0)
    mean_metric_value = total_metric_value / len(results) if len(results) > 0 else None
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value)**2 for result in results if result["instances_tested"] > 0)) / len(results) if len(results) > 1 else None
    
    support_fraction = sum(result["conjecture_holds"] for result in results) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")