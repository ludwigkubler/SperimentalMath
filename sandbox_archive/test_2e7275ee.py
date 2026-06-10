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
    
    def generate_clause_set(n, k):
        clauses = []
        for _ in range(k):
            clause = [random.randint(1, n), random.randint(1, n)]
            if clause not in clauses:
                clauses.append(clause)
        return clauses
    
    def construct_lie_algebroid(clauses):
        n = max(max(clause) for clause in clauses)
        A = [[0] * (n + 1) for _ in range(n + 1)]
        for u, v in clauses:
            A[u][v] += 1
            A[v][u] += 1
        return A
    
    def resolution_width(clauses):
        n = max(max(clause) for clause in clauses)
        queue = [set([tuple(clause) for clause in clauses])]
        visited = set()
        width = 0
        
        while queue:
            level = len(queue)
            if level > width:
                width = level
            new_queue = []
            for clause_set in queue:
                for clause in clause_set:
                    if clause not in visited:
                        visited.add(clause)
                        new_clauses = [c for c in clauses if c != clause]
                        new_queue.append(set(new_clauses))
            queue = new_queue
        
        return width
    
    def matrix_order(A):
        n = len(A)
        rank = 0
        for i in range(n):
            pivot = None
            for j in range(i, n):
                if A[j][i] != 0:
                    pivot = j
                    break
            if pivot is not None:
                rank += 1
                for j in range(n):
                    A[i][j], A[pivot][j] = A[pivot][j], A[i][j]
                for k in range(n):
                    if k != i:
                        factor = A[k][i] / A[i][i]
                        for j in range(n):
                            A[k][j] -= factor * A[i][j]
        return rank
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        for _ in range(4):
            clauses = generate_clause_set(n, random.randint(1, n))
            A = construct_lie_algebroid(clauses)
            order = matrix_order(A)
            width = resolution_width(clauses)
            results.append((order, width))
    
    if len(results) < 24:
        return {
            "metric_name": "correlation",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "insufficient_data"
        }
    
    order_sum = sum(order for order, _ in results)
    width_sum = sum(width for _, width in results)
    order_mean = order_sum / len(results)
    width_mean = width_sum / len(results)
    
    correlation = 0
    for order, width in results:
        correlation += (order - order_mean) * (width - width_mean)
    correlation /= math.sqrt((sum((order - order_mean) ** 2 for order, _ in results)) * 
                              (sum((width - width_mean) ** 2 for _, width in results)))
    
    return {
        "metric_name": "correlation",
        "metric_value": correlation,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": 0.5 <= correlation <= 1,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 
                                              31, 37, 41, 43, 47, 53, 59, 61, 67, 
                                              71, 73, 79, 83, 89, 97, 101, 103, 107, 
                                              109, 113]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all("conjecture_holds" not in result or result["conjecture_holds"] for result in results):
        support_fraction = sum(1 for result in results if "conjecture_holds" in result and result["conjecture_holds"]) / len(results)
        mean_correlation = sum(result["metric_value"] for result in results) / len(results)
        std_deviation = math.sqrt(sum((result["metric_value"] - mean_correlation) ** 2 for result in results) / len(results))
        
        if support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={mean_correlation} std={std_deviation} support_fraction={support_fraction}")
        else:
            print("RESULT: INCONCLUSIVE insufficient_support")
    elif any("conjecture_holds" in result and not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if "conjecture_holds" in result and not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_outside_bounds\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")