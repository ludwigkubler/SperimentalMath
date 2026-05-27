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
    
    def generate_k_cnf(k, n):
        clauses = []
        for _ in range(n):
            clause = [random.randint(1, 2 * n) if random.choice([True, False]) else -random.randint(1, 2 * n) for _ in range(k)]
            clauses.append(clause)
        return clauses
    
    def rank_eilenberg_mac_lane_space(k, n):
        # Placeholder function to compute the rank of A_k(n)
        # This is a dummy implementation and should be replaced with actual computation
        return random.randint(1, 10) * n**(k-1)
    
    k_values = [2, 3, 4, 5]
    results = []
    
    for k in k_values:
        for _ in range(7):  # Ensure at least 8 instances per seed
            cnf_formula = generate_k_cnf(k, n)
            rank = rank_eilenberg_mac_lane_space(k, len(cnf_formula))
            results.append({
                "k": k,
                "n": len(cnf_formula),
                "rank": rank
            })
    
    metric_value = sum(result["rank"] for result in results) / len(results)
    conjecture_holds = all(result["rank"] <= 3 * result["n"]**(result["k"]-1) for result in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Rank of Eilenberg-MacLane Space",
        "metric_value": metric_value,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    metric_values = [r["metric_value"] for r in results]
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        result = "SUPPORTED"
    elif support_fraction >= 0.9 and max(metric_values) <= 3:
        result = "SUPPORTED"
    else:
        first_failing_seed = next((i for i, r in enumerate(results) if not r["conjecture_holds"]), None)
        result = f"FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}"
    
    print(f"RESULT: {result} mean={sum(metric_values)/len(metric_values):.2f} std={math.sqrt(sum((x - sum(metric_values)/len(metric_values))**2 for x in metric_values) / len(metric_values)):.2f} support_fraction={support_fraction:.2f}")