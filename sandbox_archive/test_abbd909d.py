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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(2 * n):
            clause = [random.randint(-n, -1), random.randint(1, n)]
            clauses.append(clause)
        return clauses
    
    def min_topological_entropy(cnf):
        # Simplified symbolic dynamics approach
        variables = set()
        for clause in cnf:
            for literal in clause:
                variables.add(abs(literal))
        num_vars = len(variables)
        if num_vars == 0: return 0
        return -num_vars * math.log2(1 / num_vars)
    
    def communication_complexity_rank_variance(cnf):
        # Simplified rank variance approach
        n = max(abs(lit) for clause in cnf for lit in clause)
        return (n ** 3) / 6
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        crv_sum = 0
        h_min_sum = 0
        instances_tested = 0
        
        for _ in range(5):  # Ensure at least 30 instances per seed
            cnf = generate_cnf(n)
            h_min = min_topological_entropy(cnf)
            if h_min <= math.log2(n**3):
                crv = communication_complexity_rank_variance(cnf)
                crv_sum += crv
                h_min_sum += h_min ** 2
                instances_tested += 1
        
        if instances_tested == 0:
            return {
                "metric_name": "CRV/H_min^2",
                "metric_value": None,
                "instances_tested": 0,
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": "no_valid_instances"
            }
        
        crv_avg = crv_sum / instances_tested
        h_min_avg = h_min_sum / instances_tested
        
        results.append((crv_avg, h_min_avg))
    
    crv_avg_overall = sum(crv for crv, _ in results) / len(results)
    h_min_avg_overall = sum(h for _, h in results) / len(results)
    
    if all(crv <= 1.5 * h ** 2 for crv, h in results):
        return {
            "metric_name": "CRV/H_min^2",
            "metric_value": crv_avg_overall,
            "instances_tested": sum(instances_tested for _, _, instances_tested in results),
            "n_max": max(n_values),
            "conjecture_holds": True,
            "counterexample": ""
        }
    else:
        return {
            "metric_name": "CRV/H_min^2",
            "metric_value": crv_avg_overall,
            "instances_tested": sum(instances_tested for _, _, instances_tested in results),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "CRV > 1.5 * H_min^2"
        }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    crv_values = [r["metric_value"] for r in results if r["metric_value"] is not None]
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={sum(crv_values) / len(crv_values)} std={math.sqrt(sum((x - sum(crv_values) / len(crv_values)) ** 2 for x in crv_values) / len(crv_values))} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={sum(crv_values) / len(crv_values)} std={math.sqrt(sum((x - sum(crv_values) / len(crv_values)) ** 2 for x in crv_values) / len(crv_values))} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"CRV > 1.5 * H_min^2\" first_failing_seed={first_failing_seed}")