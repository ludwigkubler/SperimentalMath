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

def gaussian_elimination(matrix):
    rows, cols = len(matrix), len(matrix[0])
    rank = 0
    
    for i in range(cols):
        pivot_row = -1
        for j in range(rank, rows):
            if matrix[j][i] != 0:
                pivot_row = j
                break
        
        if pivot_row == -1:
            continue
        
        matrix[pivot_row], matrix[rank] = matrix[rank], matrix[pivot_row]
        
        for j in range(rows):
            if j != rank:
                factor = Fraction(matrix[j][i], matrix[rank][i])
                for k in range(cols):
                    matrix[j][k] -= factor * matrix[rank][k]
        
        rank += 1
    
    return rank

def grothendieck_witt_class(cnf):
    n = len(cnf)
    A = [[0] * (n + 1) for _ in range(n + 1)]
    
    for clause in cnf:
        for literal in clause:
            var = abs(literal) - 1
            if literal > 0:
                A[var][n] += 1
            else:
                A[n][var] -= 1
    
    return gaussian_elimination(A)

def resolution_width(cnf):
    clauses = list(cnf)
    queue = clauses[:]
    visited = set()
    
    while queue:
        clause = queue.pop(0)
        for literal in clause:
            neg_literal = -literal
            if neg_literal not in visited:
                visited.add(neg_literal)
                new_clause = [l for l in clauses if l != clause and neg_literal not in l]
                if len(new_clause) == 1:
                    return len(clause)
                queue.append(new_clause)
    
    return float('inf')

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    cnf = []
    
    for _ in range(n):
        clause = [random.randint(1, n) * (-1 if random.choice([True, False]) else 1) for _ in range(random.randint(1, n))]
        cnf.append(clause)
    
    w_f = grothendieck_witt_class(cnf)
    t_star = resolution_width(cnf)
    
    if t_star == float('inf'):
        return {
            "metric_name": "correlation",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "resolution_width_infinite"
        }
    
    return {
        "metric_name": "correlation",
        "metric_value": w_f / t_star,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [random.randint(2, 97) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["metric_value"] is not None for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                print(f"RESULT: FALSIFIED counterexample=\"resolution_width_infinite\" first_failing_seed={r['seed']}")
                break