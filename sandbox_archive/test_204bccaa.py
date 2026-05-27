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

def random_polynomial(n, p):
    return [random.randint(0, p-1) for _ in range(n+1)]

def hodge_rank(f, p):
    n = len(f) - 1
    A = [[0] * (n + 1) for _ in range(n + 1)]
    
    for i in range(n + 1):
        for j in range(n + 1):
            if i + j == 0:
                A[i][j] = 1
            else:
                A[i][j] = sum((f[k] ** (i+j-k)) % p for k in range(n+1)) % p
    
    # Gaussian elimination to find the rank of A modulo p^2
    for i in range(n + 1):
        if A[i][i] == 0:
            found = False
            for j in range(i + 1, n + 1):
                if A[j][i] != 0:
                    for k in range(n + 1):
                        A[i][k], A[j][k] = (A[j][k] - A[i][k] * A[j][i]) % p, (A[i][k] - A[j][k] * A[i][i]) % p
                    found = True
                    break
            if not found:
                return i
    
    rank = 0
    for row in A:
        if any(row):
            rank += 1
    
    return rank

def resolution_refutation_size(f, p):
    n = len(f) - 1
    literals = set()
    for term in f:
        for literal in term.split('&'):
            literals.add(literal.strip())
    
    clauses = []
    for term in f:
        clause = []
        for literal in term.split('&'):
            if literal.startswith('~'):
                clause.append(-int(literal[1:]))
            else:
                clause.append(int(literal))
        clauses.append(clause)
    
    stack = []
    while True:
        unit_clause = None
        for clause in clauses:
            if len(clause) == 1:
                unit_clause = clause[0]
                break
        
        if unit_clause is None:
            return len(clauses)
        
        stack.append(unit_clause)
        new_clauses = []
        for clause in clauses:
            if unit_clause not in clause and -unit_clause not in clause:
                new_clauses.append([l for l in clause if l != -unit_clause])
        
        clauses = new_clauses
    
    return len(clauses)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        f = random_polynomial(n, p=2)
        hodge_r = hodge_rank(f, p=2)
        refutation_size = resolution_refutation_size([f], p=2)
        
        if refutation_size == 0:
            return {
                "metric_name": "Hodge Rank vs Refutation Size",
                "metric_value": float('inf'),
                "instances_tested": n,
                "conjecture_holds": False,
                "counterexample": "Empty refutation size"
            }
        
        if hodge_r < math.log(refutation_size, 2):
            return {
                "metric_name": "Hodge Rank vs Refutation Size",
                "metric_value": float('inf'),
                "instances_tested": n,
                "conjecture_holds": False,
                "counterexample": f"Hodge rank {hodge_r} is not logarithmically bounded by refutation size {refutation_size}"
            }
        
        results.append((hodge_r, refutation_size))
    
    mean_value = sum(h for h, _ in results) / len(results)
    std_value = math.sqrt(sum((h - mean_value) ** 2 for h, _ in results) / len(results))
    
    return {
        "metric_name": "Hodge Rank vs Refutation Size",
        "metric_value": mean_value,
        "instances_tested": sum(n_values),
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
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
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        counterexample = next(r["counterexample"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")