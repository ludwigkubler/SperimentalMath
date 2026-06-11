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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def tseitin_formula(f, n):
        literals = {i: f[i] for i in range(n)}
        clauses = []
        for i in range(n):
            clauses.append((literals[i],))
        for i in range(n):
            for j in range(i+1, n):
                clauses.append((-literals[i], -literals[j]))
                clauses.append((literals[i], literals[j]))
        return clauses
    
    def gaussian_elimination(matrix):
        m, n = len(matrix), len(matrix[0])
        rank = 0
        for i in range(n):
            pivot_row = None
            for j in range(rank, m):
                if matrix[j][i] != 0:
                    pivot_row = j
                    break
            if pivot_row is None:
                continue
            matrix[pivot_row], matrix[rank] = matrix[rank], matrix[pivot_row]
            for j in range(n):
                if j == i:
                    continue
                factor = -matrix[rank][j] / matrix[rank][i]
                for k in range(n):
                    matrix[rank][k] += factor * matrix[j][k]
            rank += 1
        return rank
    
    def br(f, n):
        clauses = tseitin_formula(f, n)
        matrix = [[0] * (n + len(clauses)) for _ in range(n)]
        for i in range(n):
            matrix[i][i] = 1
        for j, clause in enumerate(clauses):
            for var in clause:
                if var < 0:
                    row = -var - 1
                    col = n + j
                else:
                    row = var - 1
                    col = i
                matrix[row][col] = 1
        return gaussian_elimination(matrix)
    
    def resolution_width(clauses):
        queue = set()
        for clause in clauses:
            queue.add(tuple(sorted(clause)))
        while True:
            new_clauses = []
            for c1, c2 in itertools.combinations(queue, 2):
                if len(c1) + len(c2) - 2 == 0 and any(-x in c2 for x in c1):
                    continue
                new_clause = tuple(sorted(set(c1) | set(c2)))
                if len(new_clause) > 3:
                    return len(new_clause)
                new_clauses.append(new_clause)
            queue.update(new_clauses)
    
    n_values = [5, 10, 15, 20, 30, 40]
    metrics = []
    for n in n_values:
        f = generate_boolean_function(n)
        br_order = br(f, n)
        width = resolution_width(tseitin_formula(f, n))
        metrics.append((br_order, width))
    
    if any(x > 10 or y > 100 for x, y in metrics):
        return {
            "metric_name": "correlation",
            "metric_value": None,
            "instances_tested": len(metrics),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "Br(f) > 10 or w(φ_f) > 100"
        }
    
    correlation = sum((x - mean_x) * (y - mean_y) for x, y in metrics) / len(metrics)
    return {
        "metric_name": "correlation",
        "metric_value": correlation,
        "instances_tested": len(metrics),
        "n_max": max(n_values),
        "conjecture_holds": correlation >= 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(x["metric_value"] for x in results if x["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((x["metric_value"] - mean_value)**2 for x in results if x["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for x in results if x["conjecture_holds"]) / len(results)
    
    if all(x["conjecture_holds"] for x in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not x["conjecture_holds"] for x in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Br(f) > 10 or w(φ_f) > 100\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")