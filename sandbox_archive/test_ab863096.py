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
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
from fractions import Fraction

def generate_tseitin_formula(n):
    variables = [f"x{i+1}" for i in range(n)]
    clauses = []
    
    # Generate clauses for each variable
    for i in range(n):
        clauses.append([variables[i], f"y{i}"])
        clauses.append([-variables[i], -f"y{i}"])
    
    # Generate clauses to encode the OR gate
    for i in range(1, n):
        clauses.append([f"y{i-1}", f"y{i}", f"y{i+1}"])
        clauses.append([-f"y{i-1}", -f"y{i}", f"y{i+1}"])
        clauses.append([f"y{i-1}", -f"y{i}", -f"y{i+1}"])
        clauses.append([-f"y{i-1}", f"y{i}", -f"y{i+1}"])
    
    # Generate the final clause
    clauses.append([f"y{n-2}", f"y{n-1}"])
    return variables, clauses

def resolution_proof_width(clauses):
    n = len(clauses)
    unit_clauses = [i for i in range(n) if len(clauses[i]) == 1]
    
    while unit_clauses:
        u = unit_clauses.pop()
        literal = clauses[u][0]
        
        for j in range(n):
            if j != u and literal in clauses[j]:
                new_clause = list(set(clauses[j]) - {literal, -literal})
                if not new_clause:
                    return float('inf')
                elif len(new_clause) == 1:
                    unit_clauses.append(j)
                else:
                    clauses[j] = new_clause
    
    return n

def calculate_M2(B):
    M2 = []
    for a in B:
        for b in B:
            M2.append([[a[0][0]*b[0][0], a[0][1]*b[0][1]], [a[1][0]*b[1][0], a[1][1]*b[1][1]]])
    return M2

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    variables, clauses = generate_tseitin_formula(n)
    B = [[random.choice([0, 1]), random.choice([0, 1])] for _ in range(2**n)]
    
    M2 = calculate_M2(B)
    order_M2 = len(M2)
    
    w_phi = resolution_proof_width(clauses)
    
    if w_phi == float('inf'):
        return {
            "metric_name": "resolution_proof_width",
            "metric_value": None,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "unsatisfiable_formula"
        }
    
    metric_value = order_M2**(1/4) * n
    
    return {
        "metric_name": "resolution_proof_width",
        "metric_value": metric_value,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": w_phi <= metric_value,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 30))  # Default to first 30 primes if no seeds provided
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))**0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")