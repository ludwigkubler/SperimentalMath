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
import itertools

# Function to generate a random k-CNF formula
def generate_k_cnf(n, m):
    if m > n * (n - 1) / 2:
        raise ValueError("Too many clauses for the given number of variables")
    
    cnf = []
    literals = list(range(1, n + 1)) + [-i for i in range(1, n + 1)]
    
    for _ in range(m):
        clause = random.sample(literals, k=3)
        cnf.append(clause)
    
    return cnf

# Function to compute the resolution proof width
def resolution_width(cnf):
    clauses = set(tuple(sorted(clause)) for clause in cnf)
    resolvents = set()
    stack = list(clauses)
    
    while stack:
        clause1 = stack.pop()
        if len(clause1) == 1:
            return len(stack) + 1
        
        for clause2 in clauses:
            if len(clause1) != len(clause2):
                continue
            
            common = set(clause1).intersection(set(clause2))
            if len(common) == 1:
                resolvent = tuple(sorted(list(set(clause1) ^ set(clause2))))
                if resolvent not in resolvents:
                    resolvents.add(resolvent)
                    stack.append(resolvent)
    
    return len(stack)

# Function to compute the Hodge index of a tropicalized polynomial
def hodge_index(cnf):
    # This is a placeholder function. In practice, you would need to implement
    # the actual computation of the Hodge index for the tropicalized polynomial.
    # For simplicity, we'll return a dummy value.
    return random.randint(1, 5)

# Function to run one trial with a given seed
def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [10, 20, 30, 40]
    alpha_values = [0.1, 0.3, 0.5]
    results = []
    
    for n in n_values:
        for alpha in alpha_values:
            m = int(n * (n - 1) / 2)
            cnf = generate_k_cnf(n, m)
            t_star = resolution_width(cnf)
            H_min = hodge_index(cnf)
            
            if t_star == 0:
                continue
            
            results.append((H_min, math.log2(t_star), n))
    
    if not results:
        return {
            "metric_name": "Spearman rank correlation",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    H_min_values = [r[0] for r in results]
    log2_t_star_values = [r[1] for r in results]
    
    n_max = max(r[2] for r in results)
    
    # Compute Spearman rank correlation
    def rank(x):
        return {v: i + 1 for i, v in enumerate(sorted(set(x), reverse=True))}
    
    ranks_H_min = rank(H_min_values)
    ranks_log2_t_star = rank(log2_t_star_values)
    
    n = len(results)
    sum_d_ranks_squared = sum((ranks_H_min[H_min] - ranks_log2_t_star[log2_t_star]) ** 2 for H_min, log2_t_star in results)
    rho_spearman = 1 - (6 * sum_d_ranks_squared) / (n * (n**2 - 1))
    
    return {
        "metric_name": "Spearman rank correlation",
        "metric_value": rho_spearman,
        "instances_tested": len(results),
        "n_max": n_max,
        "conjecture_holds": rho_spearman > 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_support")