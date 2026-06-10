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
    
    def generate_tseitin_formula(n):
        variables = [f"x{i}" for i in range(1, n+1)]
        clauses = []
        for i in range(1, n+1):
            clauses.append([variables[i-1]])
            clauses.append([-variables[i-1], f"y{i}"])
            clauses.append([f"y{i}", -i])
        return variables, clauses
    
    def gaussian_elimination(matrix):
        rows, cols = len(matrix), len(matrix[0])
        for i in range(rows):
            max_row = i
            for j in range(i+1, rows):
                if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                    max_row = j
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            for j in range(i+1, rows):
                factor = matrix[j][i] / matrix[i][i]
                for k in range(cols):
                    matrix[j][k] -= factor * matrix[i][k]
        return matrix
    
    def determinant(matrix):
        if len(matrix) == 2:
            return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
        det = 0
        for i in range(len(matrix)):
            submatrix = [row[:i] + row[i+1:] for row in matrix[1:]]
            det += ((-1) ** i) * matrix[0][i] * determinant(submatrix)
        return det
    
    def order_M2(B):
        n = len(B)
        count = 0
        for a in range(2**n):
            A = [[B[(a >> j) & 1][(b >> j) & 1] for j in range(n)] for b in range(2**n)]
            if determinant(A) != 0:
                count += 1
        return count
    
    def resolution_width(clauses):
        queue = clauses.copy()
        while queue:
            clause = queue.pop(0)
            if len(clause) == 1:
                literal = clause[0]
                for other_clause in queue:
                    if -literal in other_clause:
                        new_clause = [l for l in other_clause if l != -literal]
                        if not new_clause:
                            return float('inf')
                        queue.append(new_clause)
            else:
                literal = clause[0]
                for other_clause in queue:
                    if literal in other_clause and -other_clause[1] in clause:
                        new_clause = [l for l in clause if l != literal] + [l for l in other_clause if l != -other_clause[1]]
                        if not new_clause:
                            return float('inf')
                        queue.append(new_clause)
        return len(queue)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        variables, clauses = generate_tseitin_formula(n)
        B = [[(i >> j) & 1 for j in range(n)] for i in range(2**n)]
        order_M2_value = order_M2(B)
        width = resolution_width(clauses)
        results.append({
            "n": n,
            "order_M2_value": order_M2_value,
            "width": width
        })
    
    if not results:
        return {
            "metric_name": "resolution_width",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    order_M2_values = [r["order_M2_value"] for r in results]
    widths = [r["width"] for r in results]
    n_max = max(r["n"] for r in results)
    
    if len(widths) < 30:
        return {
            "metric_name": "resolution_width",
            "metric_value": None,
            "instances_tested": len(widths),
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    mean_width = sum(widths) / len(widths)
    std_width = math.sqrt(sum((w - mean_width) ** 2 for w in widths) / len(widths))
    correlation_coefficient = sum((order_M2_values[i] ** 0.25 * n_values[i] - mean_width) * (widths[i] - mean_width) for i in range(len(n_values))) / (len(n_values) * std_width * std_width)
    
    return {
        "metric_name": "resolution_width",
        "metric_value": correlation_coefficient,
        "instances_tested": len(widths),
        "n_max": n_max,
        "conjecture_holds": correlation_coefficient >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 10**9) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len([r for r in results if r["metric_value"] is not None])
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results if r["metric_value"] is not None) / len([r for r in results if r["metric_value"] is not None]))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient < 0.8\" first_failing_seed={first_failing_seed}")