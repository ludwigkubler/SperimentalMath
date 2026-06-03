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
        for _ in range(2 * n):
            clause = [random.randint(-n, -1), random.randint(1, n)]
            cnf.append(clause)
        return cnf
    
    def compute_k0_rank(cnf):
        n = max(abs(lit) for lit in set(lit for clause in cnf for lit in clause))
        rank = sum(1 for clause in cnf if any(lit in clause for lit in [-i, i] for i in range(1, n+1)))
        return rank
    
    def compute_clause_set_complexity(cnf):
        return len(cnf)
    
    n_values = [5, 10, 15, 20, 30, 40]
    ranks = []
    complexities = []
    
    for n in n_values:
        cnf = generate_cnf(n)
        rank = compute_k0_rank(cnf)
        complexity = compute_clause_set_complexity(cnf)
        
        if rank is None or complexity is None:
            return {
                "metric_name": "K0 Rank vs Clause Set Complexity",
                "metric_value": None,
                "instances_tested": 1,
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": "mapping_undefined"
            }
        
        ranks.append(rank)
        complexities.append(complexity)
    
    if len(ranks) < 30:
        return {
            "metric_name": "K0 Rank vs Clause Set Complexity",
            "metric_value": None,
            "instances_tested": len(ranks),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    mean_rank = sum(ranks) / len(ranks)
    mean_complexity = sum(complexities) / len(complexities)
    correlation_coefficient = 0.0
    
    if mean_complexity != 0:
        numerator = sum((r - mean_rank) * (c - mean_complexity) for r, c in zip(ranks, complexities))
        denominator = math.sqrt(sum((r - mean_rank)**2 for r in ranks)) * math.sqrt(sum((c - mean_complexity)**2 for c in complexities))
        correlation_coefficient = numerator / denominator
    
    return {
        "metric_name": "K0 Rank vs Clause Set Complexity",
        "metric_value": correlation_coefficient,
        "instances_tested": len(ranks),
        "n_max": max(n_values),
        "conjecture_holds": abs(correlation_coefficient) > 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(r["counterexample"] == "mapping_undefined" for r in results):
        print("RESULT: INCONCLUSIVE mapping_undefined")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")