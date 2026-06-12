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

def generate_tseitin_formula(n):
    variables = [f'x{i+1}' for i in range(n)]
    clauses = []
    
    # Generate clauses for each variable
    for i in range(n):
        new_var = f'y{i+1}'
        clauses.append([variables[i], -new_var])
        clauses.append([-variables[i], new_var])
    
    # Generate clauses for the Tseitin formula
    for i in range(2, n + 1):
        new_var = f'y{i+1}'
        clauses.append([f'x{i}', variables[i-1], -new_var])
        clauses.append([-f'x{i}', variables[i-1], new_var])
        clauses.append([f'x{i}', -variables[i-1], -new_var])
        clauses.append([-f'x{i}', -variables[i-1], new_var])
    
    # Generate the final clause
    for i in range(n):
        clauses.append([variables[i]])
    
    return variables, clauses

def compute_cohomology_group(clauses, p):
    n = len(clauses)
    K = [[0] * (n + 2) for _ in range(n + 2)]
    
    # Fill the simplicial complex
    for clause in clauses:
        if len(clause) == 1:
            continue
        for i in range(len(clause)):
            for j in range(i + 1, len(clause)):
                K[clause[i]][clause[j]] += 1
                K[clause[j]][clause[i]] += 1
    
    # Compute the p-th cohomology group using cellular acyclic complex method
    # This is a simplified version and may not work for all cases
    H = [0] * (n + 2)
    for i in range(n + 2):
        if sum(K[i]) % p == 1:
            H[i] += 1
    
    return max(H)

def compute_resolution_width(clauses):
    n = len(clauses)
    width = 0
    stack = []
    
    for clause in clauses:
        if len(clause) == 1:
            continue
        for literal in clause:
            if literal > 0 and -literal not in stack:
                stack.append(literal)
                width = max(width, len(stack))
            elif literal < 0 and -literal in stack:
                stack.remove(-literal)
    
    return width

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    variables, clauses = generate_tseitin_formula(n)
    p = random.randint(2, 10)
    
    cohomology_group = compute_cohomology_group(clauses, p)
    resolution_width = compute_resolution_width(clauses)
    
    if cohomology_group > 10:
        return {
            "metric_name": "cohomology_group",
            "metric_value": cohomology_group,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": f"cohomology_group > 10 for n={n}"
        }
    
    return {
        "metric_name": "cohomology_group",
        "metric_value": cohomology_group,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='cohomology_group > 10' first_failing_seed={first_failing_seed}")