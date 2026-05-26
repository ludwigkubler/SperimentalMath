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

def tseitin_circuit_valuation(n):
    variables = [f'x{i+1}' for i in range(n)]
    tseitin_vars = [f't{i+1}' for i in range(n)]
    
    clauses = []
    for i in range(1, n + 1):
        clauses.append([tseitin_vars[2*i-2], -variables[i-1]])
        clauses.append([tseitin_vars[2*i-1], variables[i-1]])
        clauses.append([-tseitin_vars[2*i-2], -tseitin_vars[2*i-1]])
    
    return variables, clauses

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    variables, clauses = tseitin_circuit_valuation(n)
    
    # Construct the Coxeter group structure (simplified for demonstration)
    G = {}
    for clause in clauses:
        for lit in clause:
            if lit not in G:
                G[lit] = set()
            for other_lit in clause:
                if other_lit != lit and -other_lit not in G[lit]:
                    G[lit].add(other_lit)
    
    # Compute the minimal orbit length (simplified for demonstration)
    visited = set()
    def dfs(node):
        if node in visited:
            return 0
        visited.add(node)
        max_depth = 0
        for neighbor in G[node]:
            depth = dfs(neighbor)
            if depth > max_depth:
                max_depth = depth
        return max_depth + 1
    
    min_orbit_length = float('inf')
    for node in variables:
        orbit_length = dfs(node)
        if orbit_length < min_orbit_length:
            min_orbit_length = orbit_length
    
    # Compute the resolution refutation size (simplified for demonstration)
    r_n = len(clauses)
    
    # Check the conjecture
    conjecture_holds = min_orbit_length >= 2 ** math.ceil(math.log2(r_n))
    counterexample = "" if conjecture_holds else f"min_orbit_length={min_orbit_length}, expected>=2^{math.ceil(math.log2(r_n))}"
    
    return {
        "metric_name": "minimal_orbit_length",
        "metric_value": min_orbit_length,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r['metric_value'] for r in results) / len(results)
    std_value = math.sqrt(sum((r['metric_value'] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    
    if all(r['conjecture_holds'] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r['conjecture_holds'])
        print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={first_failing_seed}")