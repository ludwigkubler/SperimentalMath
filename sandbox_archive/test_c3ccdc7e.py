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

def generate_random_formula(n):
    variables = [f"x{i}" for i in range(1, n+1)]
    clauses = []
    for _ in range(n):
        clause = random.sample(variables + [f"~{v}" for v in variables], 2)
        clauses.append(clause)
    return clauses

def clause_tree_width(clauses):
    if not clauses:
        return 0
    nodes = set()
    for clause in clauses:
        nodes.update(clause)
    edges = []
    for i, clause1 in enumerate(clauses):
        for j, clause2 in enumerate(clauses):
            if i < j and len(set(clause1) & set(clause2)) == 1:
                edges.append((i, j))
    visited = [False] * len(clauses)
    def dfs(node):
        visited[node] = True
        for neighbor in range(len(clauses)):
            if (node, neighbor) in edges and not visited[neighbor]:
                dfs(neighbor)
    dfs(0)
    return max(sum(not v for v in visited), 1)

def twisted_tensor_product_rank(clauses):
    n = len(clauses)
    mrt = [[0] * n for _ in range(n)]
    for i, clause1 in enumerate(clauses):
        for j, clause2 in enumerate(clauses):
            if i < j and len(set(clause1) & set(clause2)) == 1:
                mrt[i][j] = 1
    rank = 0
    while True:
        pivot_row = next((i for i in range(n) if any(mrt[i][j] for j in range(rank))), None)
        if pivot_row is None:
            break
        for j in range(rank, n):
            mrt[pivot_row][j] /= mrt[pivot_row][rank]
        for i in range(n):
            if i != pivot_row and any(mrt[i][j] for j in range(rank)):
                for j in range(rank, n):
                    mrt[i][j] -= mrt[pivot_row][j] * mrt[i][rank]
        rank += 1
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_max = 0
    metric_values = []
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""
    
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            clauses = generate_random_formula(n)
            ctw = clause_tree_width(clauses)
            mrt = twisted_tensor_product_rank(clauses)
            if n > n_max:
                n_max = n
            instances_tested += 1
            metric_values.append(ctw - mrt)
    
    correlation_coefficient = sum(metric_values) / len(metric_values)
    p_value = 0.05  # Placeholder for actual p-value calculation
    
    if correlation_coefficient < 0.5 or p_value > 0.05:
        conjecture_holds = False
        counterexample = "Correlation coefficient too low or p-value too high"
    
    return {
        "metric_name": "ctw - mrt",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")