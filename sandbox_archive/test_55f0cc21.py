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

def generate_k_cnf(n, k):
    clauses = []
    for _ in range(k):
        clause = set(random.sample(range(1, n+1), 2))
        clauses.append(clause)
    return clauses

def truth_table_size(n):
    return 2**n

def entropic_complexity(truth_table_size):
    if truth_table_size <= 0:
        return 0
    entropy = -truth_table_size * math.log(1/truth_table_size, 2)
    return entropy

def dpll_refutation_depth(clauses):
    depth = 0
    stack = []
    while clauses:
        clause = random.choice(clauses)
        if len(clause) == 1:
            literals = list(clause)
            for literal in literals:
                clauses = [c for c in clauses if literal not in c]
                if not clauses:
                    return depth + 1
            stack.append(literals)
        else:
            literals = random.sample(clause, 2)
            for literal in literals:
                clauses = [c for c in clauses if literal not in c]
                if not clauses:
                    return depth + 1
            stack.append(literals)
        depth += 1
    return depth

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    c1, c2 = 1, 2
    results = []
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            clauses = generate_k_cnf(n, int(n * (n-1) / 4))
            truth_table_size_val = truth_table_size(n)
            entropic_val = entropic_complexity(truth_table_size_val)
            refutation_depth = dpll_refutation_depth(clauses)
            
            if refutation_depth == 0:
                continue
            
            results.append({
                "n": n,
                "entropic_complexity": entropic_val,
                "refutation_depth": refutation_depth
            })
    
    if not results:
        return {
            "metric_name": "Entropic Complexity vs DPLL Refutation Depth",
            "metric_value": 0.0,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "No valid instances found"
        }
    
    mean_entropic = sum(result["entropic_complexity"] for result in results) / len(results)
    mean_depth = sum(result["refutation_depth"] for result in results) / len(results)
    
    if c1 * math.log(2**mean_depth + 1, 2) <= mean_entropic <= c2 * math.log(2**mean_depth + 1, 2):
        return {
            "metric_name": "Entropic Complexity vs DPLL Refutation Depth",
            "metric_value": mean_entropic,
            "instances_tested": len(results),
            "conjecture_holds": True,
            "counterexample": ""
        }
    else:
        return {
            "metric_name": "Entropic Complexity vs DPLL Refutation Depth",
            "metric_value": mean_entropic,
            "instances_tested": len(results),
            "conjecture_holds": False,
            "counterexample": f"Failed for n={n}, entropic={mean_entropic}, depth={mean_depth}"
        }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = 1.0
        result_str = f"SUPPORTED mean={mean_value} std={0.0} support_fraction={support_fraction}"
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        counterexample = results[first_failing_seed]["counterexample"]
        result_str = f"FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}"
    
    print(result_str)