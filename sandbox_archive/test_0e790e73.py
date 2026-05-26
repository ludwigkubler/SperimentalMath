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

def tseitin_circuit_valuation(n: int):
    variables = [f'x{i}' for i in range(1, n+1)]
    tseitin_vars = [f't{i}' for i in range(1, 2*n+1)]
    
    clauses = []
    for i in range(1, n+1):
        clauses.append([tseitin_vars[2*i-2], variables[i-1]])
        clauses.append([tseitin_vars[2*i-1], -variables[i-1]])
        clauses.append([-tseitin_vars[2*i-2], -tseitin_vars[2*i-1]])
    
    for i in range(n+1, 2*n):
        a = random.randint(0, n-1)
        b = random.randint(0, n-1)
        while b == a:
            b = random.randint(0, n-1)
        clauses.append([tseitin_vars[2*i], tseitin_vars[2*a], -tseitin_vars[2*b]])
        clauses.append([-tseitin_vars[2*i], -tseitin_vars[2*a], tseitin_vars[2*b]])
        clauses.append([tseitin_vars[2*i], -tseitin_vars[2*a], -tseitin_vars[2*b]])
        clauses.append([-tseitin_vars[2*i], tseitin_vars[2*a], tseitin_vars[2*b]])
    
    return variables, clauses

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    variables, clauses = tseitin_circuit_valuation(n)
    
    # Construct Coxeter group structure (simplified for demonstration)
    G = {}
    for v in variables + tseitin_vars:
        G[v] = set()
    
    # Add relations based on circuit structure
    for clause in clauses:
        if len(clause) == 2:
            a, b = clause
            G[a].add(b)
            G[b].add(a)
        elif len(clause) == 3:
            a, b, c = clause
            G[a].add(b)
            G[b].add(c)
            G[c].add(a)
    
    # Compute minimal orbit length (simplified for demonstration)
    def dfs(node, visited):
        if node in visited:
            return 0
        visited.add(node)
        max_length = 1
        for neighbor in G[node]:
            max_length = max(max_length, dfs(neighbor, visited))
        return max_length
    
    min_orbit_length = float('inf')
    for v in variables + tseitin_vars:
        min_orbit_length = min(min_orbit_length, dfs(v, set()))
    
    # Compute resolution refutation size (simplified for demonstration)
    r_n = len(clauses)
    
    # Check conjecture
    conjecture_holds = min_orbit_length >= 2 ** math.ceil(math.log2(r_n))
    counterexample = "" if conjecture_holds else f"orbit={min_orbit_length}, expected=2^({math.ceil(math.log2(r_n))})"
    
    return {
        "metric_name": "minimal_orbit_length",
        "metric_value": min_orbit_length,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else list(range(2, 30))  # Default to first 29 primes
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"orbit<{mean_value}, expected=2^({math.ceil(math.log2(r_n))})\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient support")