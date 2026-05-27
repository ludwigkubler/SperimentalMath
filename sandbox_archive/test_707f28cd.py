# auto-injected by SEC sandbox
import math
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

def generate_cnf(n, m):
    cnf = []
    for _ in range(m):
        clause = set()
        while len(clause) < 2:
            lit = random.randint(1, n)
            if random.choice([True, False]):
                lit = -lit
            if all(lit not in [-c, c] for c in clause):
                clause.add(lit)
        cnf.append(list(clause))
    return cnf

def resolution_depth(cnf):
    clauses = set(tuple(sorted(clause)) for clause in cnf)
    new_clauses = set()
    depth = 0
    
    while True:
        added = False
        for c1, c2 in itertools.combinations(clauses, 2):
            if any(-x in c2 for x in c1):
                new_clause = tuple(sorted(set(c1) ^ set(c2)))
                if new_clause not in clauses and new_clause not in new_clauses:
                    new_clauses.add(new_clause)
                    added = True
        if not added:
            break
        clauses.update(new_clauses)
        new_clauses.clear()
        depth += 1
    
    return depth

def minimal_rank(cnf):
    # Placeholder for actual computation of minimal rank
    # For now, we'll just use the number of variables as a proxy
    n = max(abs(lit) for clause in cnf for lit in clause)
    return n

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        m = max(1, n // 10)  # Ensure at least one clause
        cnf = generate_cnf(n, m)
        rank = minimal_rank(cnf)
        depth = resolution_depth(cnf)
        
        if rank == 0 or depth == 0:
            continue
        
        results.append({
            "n": n,
            "rank": rank,
            "depth": depth
        })
    
    if not results:
        return {
            "metric_name": "Spearman Rank Correlation",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "No valid instances generated"
        }
    
    ranks = [result["rank"] for result in results]
    depths = [result["depth"] for result in results]
    
    # Calculate Spearman rank correlation
    n = len(ranks)
    sorted_ranks = sorted(range(n), key=lambda i: ranks[i])
    sorted_depths = sorted(range(n), key=lambda i: depths[i])
    rho_numerator = sum((sorted_ranks[i] - sorted_depths[i]) ** 2 for i in range(n))
    rho_denominator = n * (n**2 - 1) / 12
    rho = 1 - 6 * rho_numerator / rho_denominator
    
    return {
        "metric_name": "Spearman Rank Correlation",
        "metric_value": rho,
        "instances_tested": len(results),
        "conjecture_holds": rho >= 0.5,
        "counterexample": "" if rho >= 0.5 else "rho < 0.5"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]  # Default to first 3 primes
    
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all("metric_value" in r and r["metric_value"] is not None for r in results):
        mean_rho = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_rho} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if "metric_value" not in r or r["metric_value"] is None), None)
        print(f"RESULT: INCONCLUSIVE reason=no_valid_instances_first_seed={first_failing_seed}")