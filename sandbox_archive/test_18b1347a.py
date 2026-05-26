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
    k = 3  # Fixed constant for k-SAT
    n = random.randint(5, 40)  # Random number of variables between 5 and 40
    instances_tested = 1
    
    # Generate a random k-SAT instance
    clauses = []
    for _ in range(n):
        clause = [random.choice([-1, 1]) * (i + 1) for i in range(k)]
        if len(set(clause)) == k:  # Ensure no duplicate literals in the same clause
            clauses.append(clause)
    
    # Construct the conflict set
    conflict_set = []
    for i in range(n):
        for j in range(i + 1, n):
            if any(lit1 != -lit2 for lit1, lit2 in zip(clauses[i], clauses[j])):
                conflict_set.append((i, j))
    
    # Compute the tropicalized Hodge structure (simplified)
    rank = len(conflict_set)  # Simplified rank as number of conflicts
    
    # Calculate the ratio
    if n <= 0:
        return {
            "metric_name": "ratio",
            "metric_value": None,
            "instances_tested": instances_tested,
            "conjecture_holds": False,
            "counterexample": "n is non-positive"
        }
    
    log_n = math.log(n)
    log_k = math.log(k)
    expected_rank = (log_n / log_k) * 1.2  # Upper bound for the conjecture
    
    if rank > expected_rank:
        return {
            "metric_name": "ratio",
            "metric_value": rank,
            "instances_tested": instances_tested,
            "conjecture_holds": False,
            "counterexample": f"Rank {rank} exceeds upper bound {expected_rank}"
        }
    
    ratio = rank / log_n
    if abs(ratio - (log_n / log_k)) > 0.2 * (log_n / log_k):
        return {
            "metric_name": "ratio",
            "metric_value": ratio,
            "instances_tested": instances_tested,
            "conjecture_holds": False,
            "counterexample": f"Ratio {ratio} outside ±20% of Θ(log(n)/log(k))"
        }
    
    return {
        "metric_name": "ratio",
        "metric_value": ratio,
        "instances_tested": instances_tested,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_value = sum(result["metric_value"] for result in results) / len(results)
        std_value = math.sqrt(sum((x - mean_value) ** 2 for x in [result["metric_value"] for result in results]) / len(results))
        support_fraction = 1.0
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        mean_value = None
        std_value = None
        support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    print(f"RESULT: {'SUPPORTED' if all(result['conjecture_holds'] for result in results) else 'FALSIFIED'} mean={mean_value} std={std_value} support_fraction={support_fraction}")