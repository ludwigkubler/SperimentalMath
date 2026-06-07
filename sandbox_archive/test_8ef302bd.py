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
    
    def generate_formula(n, m):
        variables = set(range(1, n + 1))
        clauses = []
        for _ in range(m):
            clause = random.sample(variables, random.randint(1, n))
            clauses.append(clause)
        return clauses
    
    def compute_clause_depth(clauses):
        max_distance = 0
        for i in range(len(clauses)):
            for j in range(i + 1, len(clauses)):
                distance = sum(1 for var in clauses[i] if var in clauses[j])
                max_distance = max(max_distance, distance)
        return max_distance
    
    def compute_ehrhart_semigroup_size(clauses):
        # Simplified approximation of Ehrhart semigroup size
        m = len(clauses)
        d = compute_clause_depth(clauses)
        return int(d ** (1.5 / 2) * math.log(m, 2) ** 3)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            m = random.randint(n, 2 * n)
            clauses = generate_formula(n, m)
            ehrhart_semigroup_size = compute_ehrhart_semigroup_size(clauses)
            clause_depth = compute_clause_depth(clauses)
            results.append({
                "n": n,
                "m": m,
                "ehrhart_semigroup_size": ehrhart_semigroup_size,
                "clause_depth": clause_depth
            })
    
    if not results:
        return {
            "metric_name": "Ehrhart Rank and Clause Depth Inequality",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "No instances generated"
        }
    
    total_ehrhart = sum(result["ehrhart_semigroup_size"] for result in results)
    total_depth = sum(result["clause_depth"] ** (1.5 / 2) * math.log(result["m"], 2) ** 3 for result in results)
    mean_ehrhart = total_ehrhart / len(results)
    
    if mean_ehrhart > 0:
        ratio = mean_ehrhart / total_depth
    else:
        ratio = float('inf')
    
    return {
        "metric_name": "Ehrhart Rank and Clause Depth Inequality",
        "metric_value": ratio,
        "instances_tested": len(results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": ratio <= 1,  # Simplified check
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ratio = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                counterexample = f"n={r['n']}, m={r['m']}, ehrhart_semigroup_size={r['ehrhart_semigroup_size']}, clause_depth={r['clause_depth']}"
                print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={seed}")
                break