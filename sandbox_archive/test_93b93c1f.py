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

def gaussian_elimination(matrix):
    n = len(matrix)
    for i in range(n):
        # Find pivot row
        max_row = i
        for j in range(i + 1, n):
            if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                max_row = j
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        
        # Eliminate non-pivot elements
        pivot = matrix[i][i]
        for j in range(n):
            if j != i:
                factor = matrix[j][i] / pivot
                for k in range(n + 1):
                    matrix[j][k] -= factor * matrix[i][k]

    rank = sum(1 for row in matrix if any(row))
    return rank

def generate_random_3cnf(n, m):
    clauses = []
    variables = set()
    for _ in range(m):
        clause = random.sample(range(-n, 0), 3) + random.sample(range(1, n + 1), 3)
        clauses.append(clause)
        variables.update(abs(x) for x in clause)
    return clauses, list(variables)

def generate_kclique_3cnf(n, k):
    if k > n:
        raise ValueError("k must be less than or equal to n")
    
    edges = set()
    while len(edges) < k * (k - 1) // 2:
        u, v = random.sample(range(1, n + 1), 2)
        if u != v and (u, v) not in edges and (v, u) not in edges:
            edges.add((u, v))
    
    clauses = []
    for u in range(1, n + 1):
        for v in range(u + 1, n + 1):
            if (u, v) not in edges:
                clauses.append([-u, -v])
                clauses.append([u, v])
                clauses.append([-u, v])
                clauses.append([u, -v])
    
    variables = list(range(1, n + 1))
    return clauses, variables

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):  # Ensure at least 30 instances per seed
            if n == 1:  # Trivial case enumeration is allowed
                continue
            
            if random.random() < 0.5:
                clauses, variables = generate_kclique_3cnf(n, n // 2)
            else:
                clauses, variables = generate_random_3cnf(n, 3 * n)
            
            matrix = [[int(abs(clause) == var) for var in variables] for clause in clauses]
            rank = gaussian_elimination(matrix)
            
            results.append((n, rank))
    
    total_rank = sum(rank for _, rank in results)
    avg_rank = total_rank / len(results)
    max_rank = max(rank for _, rank in results)
    min_rank = min(rank for _, rank in results)
    
    if max_rank >= 2 * math.log(n):
        conjecture_holds = True
        counterexample = ""
    else:
        conjecture_holds = False
        counterexample = f"max_rank={max_rank} < 2*log({n})"
    
    return {
        "metric_name": "max_matroid_rank",
        "metric_value": avg_rank,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]]
    if not seeds:
        from sympy.ntheory import primerange
        seeds = list(primerange(2, 30))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    avg_rank = sum(res["metric_value"] for res in results) / len(results)
    max_rank = max(res["metric_value"] for res in results)
    min_rank = min(res["metric_value"] for res in results)
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={avg_rank:.2f} std={max_rank - min_rank:.2f} support_fraction={support_fraction:.2f}")
    elif any(not res["conjecture_holds"] for res in results):
        first_failing_seed = next(seed for seed, res in enumerate(results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"max_rank<{max_rank} < 2*log(n)\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_support")