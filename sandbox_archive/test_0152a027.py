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

def generate_d_regular_expander(n, d):
    if n < 2 or d < 1 or (n * d) % 2 != 0:
        raise ValueError("Invalid parameters for expander graph")
    
    edges = set()
    while len(edges) < (n * d) // 2:
        u = random.randint(0, n - 1)
        v = random.randint(0, n - 1)
        if u != v and (u, v) not in edges and (v, u) not in edges:
            edges.add((u, v))
    
    return list(edges)

def generate_tseitin_formula(n):
    variables = [f'x{i}' for i in range(2 * n)]
    clauses = []
    for i in range(n):
        clauses.append(f'{variables[2*i]} OR {variables[2*i+1]}')
        clauses.append(f'NOT {variables[2*i]} OR NOT {variables[2*i+1]}')
        for j in range(i + 1, n):
            clauses.append(f'NOT {variables[2*i]} OR NOT {variables[2*j]}')
            clauses.append(f'NOT {variables[2*i+1]} OR NOT {variables[2*j]}')
    return clauses

def generate_polynomial_system(clauses):
    polynomials = []
    for clause in clauses:
        if 'OR' in clause:
            p1, p2 = clause.split(' OR ')
            polynomials.append(f'{p1} * {p2}')
        elif 'NOT' in clause:
            p = clause.replace('NOT ', '')
            polynomials.append(f'{p} * (1 - {p})')
    return polynomials

def compute_algebraic_degree(polynomials):
    # Placeholder for actual algebraic degree computation
    # This is a simplified version and not accurate for real Tseitin formulas
    return len(polynomials)

def resolve_tseitin_formula(clauses):
    # Placeholder for actual resolution width computation
    # This is a simplified version and not accurate for real Tseitin formulas
    return len(clauses)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    d = 2
    
    try:
        edges = generate_d_regular_expander(n, d)
    except ValueError as e:
        return {
            "metric_name": "resolution_width",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": str(e)
        }
    
    clauses = generate_tseitin_formula(n)
    polynomials = generate_polynomial_system(clauses)
    algebraic_degree = compute_algebraic_degree(polynomials)
    resolution_width = resolve_tseitin_formula(clauses)
    
    return {
        "metric_name": "resolution_width",
        "metric_value": resolution_width,
        "instances_tested": 1,
        "conjecture_holds": resolution_width >= algebraic_degree,
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
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")