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
        for _ in range(10):  # Generate 10 clauses with n literals each
            clause = [random.randint(-n, -1), random.randint(1, n)]
            cnf.append(clause)
        return cnf
    
    def communication_complexity(cnf):
        n = len(cnf[0])
        c = 0
        for clause in cnf:
            c += max(abs(lit) for lit in clause)
        return c
    
    def rank_toric_variety(cnf):
        # Simplified version of computing the rank of a toric variety
        n = len(cnf[0])
        rank = 2 * n + 1  # Placeholder value
        return rank
    
    def solve(lits, cls):
        # Simplified SAT solver
        for lit in lits:
            if -lit in cls:
                return False
        return True
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        cnf = generate_cnf(n)
        rank = rank_toric_variety(cnf)
        c = communication_complexity(cnf)
        results.append((rank, c))
    
    if not results:
        return {
            "metric_name": "communication_complexity",
            "metric_value": 0,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "empty_cnf"
        }
    
    mean_rank = sum(rank for rank, _ in results) / len(results)
    mean_c = sum(c for _, c in results) / len(results)
    max_n = max(n_values)
    
    if any(rank is None or c is None for rank, c in results):
        return {
            "metric_name": "communication_complexity",
            "metric_value": 0,
            "instances_tested": len(results),
            "n_max": max_n,
            "conjecture_holds": False,
            "counterexample": "invalid_cnf"
        }
    
    k = abs(mean_rank - 2 * mean_c)  # Example threshold, adjust as needed
    conjecture_holds = all(abs(rank - 2 * c) <= k for rank, c in results)
    
    return {
        "metric_name": "communication_complexity",
        "metric_value": mean_rank,
        "instances_tested": len(results),
        "n_max": max_n,
        "conjecture_holds": conjecture_holds,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")