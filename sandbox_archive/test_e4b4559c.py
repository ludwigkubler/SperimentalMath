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
    
    def generate_tseitin_formula(d):
        variables = [f'x{i}' for i in range(1, d+1)]
        clauses = []
        for i in range(1, d+1):
            clauses.append([variables[i-1]])
        for i in range(1, d+1):
            for j in range(i+1, d+1):
                clauses.append([-variables[i-1], -variables[j-1]])
                clauses.append([variables[i-1], variables[j-1]])
        return variables, clauses
    
    def adjacency_matrix(clauses):
        n = len(clauses)
        A = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i+1, n):
                if any(lit in clauses[i] and -lit in clauses[j] for lit in set(clauses[i]) | set(clauses[j])):
                    A[i][j] = 1
                    A[j][i] = 1
        return A
    
    def gaussian_elimination(A):
        n = len(A)
        for i in range(n):
            max_row = i
            for j in range(i+1, n):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            if A[i][i] == 0:
                return None
            for j in range(n):
                if j != i and A[j][i] != 0:
                    factor = -A[j][i] / A[i][i]
                    for k in range(i, n):
                        A[j][k] += factor * A[i][k]
        return [abs(A[i][i]) for i in range(n)]
    
    def minimal_order(A):
        order = gaussian_elimination(A)
        if order is None:
            return float('inf')
        return sum(order) / len(order)
    
    def resolution_proof_width(clauses):
        n = len(clauses)
        queue = clauses[:]
        level = 0
        while queue:
            new_queue = []
            for clause in queue:
                if len(clause) == 1:
                    lit = clause[0]
                    for other_clause in queue:
                        if -lit in other_clause:
                            new_queue.append([x for x in other_clause if x != -lit])
                    level += 1
                else:
                    new_queue.append(clause)
            queue = new_queue
        return level
    
    def construct_mapping(A):
        n = len(A)
        coefficients = [0] * n
        for i in range(n):
            for j in range(i+1, n):
                if A[i][j] == 1:
                    coefficients[i] += 1
                    coefficients[j] += 1
        return sum(coefficients) / (n * (n-1))
    
    d_values = [10, 20, 30, 40]
    results = []
    for d in d_values:
        variables, clauses = generate_tseitin_formula(d)
        A = adjacency_matrix(clauses)
        order = minimal_order(A)
        width = resolution_proof_width(clauses)
        mapping = construct_mapping(A)
        if order == float('inf'):
            return {
                "metric_name": "Order(m(G))",
                "metric_value": None,
                "instances_tested": 1,
                "n_max": d,
                "conjecture_holds": False,
                "counterexample": "mapping_undefined"
            }
        results.append((order, width))
    
    if len(results) < 4:
        return {
            "metric_name": "Order(m(G))",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(d_values[:len(results)]),
            "conjecture_holds": False,
            "counterexample": "insufficient_data"
        }
    
    orders = [r[0] for r in results]
    widths = [r[1] for r in results]
    correlation_coefficient = sum((orders[i] - sum(orders) / len(orders)) * (widths[i] - sum(widths) / len(widths)) for i in range(len(results))) / (len(results) * math.sqrt(sum((orders[i] - sum(orders) / len(orders)) ** 2 for i in range(len(results)))) * math.sqrt(sum((widths[i] - sum(widths) / len(widths)) ** 2 for i in range(len(results)))))
    
    return {
        "metric_name": "Order(m(G))",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(d_values[:len(results)]),
        "conjecture_holds": correlation_coefficient >= 0.7,
        "counterexample": "" if correlation_coefficient >= 0.6 else f"correlation_coefficient={correlation_coefficient:.2f}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1, 1000000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results if r["metric_value"] is not None)) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value:.2f} std={std_value:.2f} support_fraction={support_fraction:.2f}")
    elif any(r["metric_value"] < 0.6 for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if r["metric_value"] < 0.6)
        print(f"RESULT: FALSIFIED counterexample='correlation_coefficient<0.6' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction:.2f}")