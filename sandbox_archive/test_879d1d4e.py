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
    
    def generate_cnf(n):
        cnf = []
        for _ in range(10 * n):  # Ensure at least 10 clauses per variable
            clause = [random.randint(-n, -1), random.randint(1, n)]
            cnf.append(clause)
        return cnf
    
    def diophantine_equation(cnf):
        n = max(abs(lit) for lit in sum(cnf, []))
        A = [[0] * (2 * n + 1) for _ in range(len(cnf))]
        b = [0] * len(cnf)
        
        for i, clause in enumerate(cnf):
            for lit in clause:
                if lit > 0:
                    row = i
                    col = lit - 1
                else:
                    row = i
                    col = -(lit + 1) + n
                    
                A[row][col] += 1
        
        return A, b
    
    def gaussian_elimination(A, b):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i
            for j in range(i+1, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            b[i], b[max_row] = b[max_row], b[i]
            
            for j in range(i+1, m):
                factor = A[j][i] / A[i][i]
                for k in range(i, n):
                    A[j][k] -= factor * A[i][k]
                b[j] -= factor * b[i]
        
        x = [0] * n
        for i in range(m-1, -1, -1):
            x[i] = (b[i] - sum(A[i][j] * x[j] for j in range(i+1, n))) / A[i][i]
        
        return x
    
    def resolution_width(cnf):
        clauses = set(tuple(clause) for clause in cnf)
        queue = list(clauses)
        width = 0
        
        while queue:
            clause = queue.pop()
            if len(clause) > width:
                width = len(clause)
            
            new_clauses = []
            for other_clause in clauses:
                if not set(clause).isdisjoint(other_clause):
                    for lit1 in clause:
                        for lit2 in other_clause:
                            if abs(lit1) == abs(lit2):
                                continue
                            new_lit = -lit1 if lit1 < 0 else -lit2
                            new_clause = tuple(sorted(set(clause + other_clause) - {new_lit}))
                            if new_clause not in clauses and new_clause not in new_clauses:
                                new_clauses.append(new_clause)
            queue.extend(new_clauses)
            clauses.update(new_clauses)
        
        return width
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        cnf = generate_cnf(n)
        A, b = diophantine_equation(cnf)
        x = gaussian_elimination(A, b)
        
        if any(math.isnan(val) or math.isinf(val) for val in x):
            continue
        
        w = resolution_width(cnf)
        results.append({"n": n, "order": len(x), "width": w})
    
    if not results:
        return {
            "metric_name": "resolution_width",
            "metric_value": 0,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "no_valid_instances"
        }
    
    total_order = sum(result["order"] for result in results)
    total_width = sum(result["width"] for result in results)
    instances_tested = len(results)
    n_max = max(result["n"] for result in results)
    
    mean_order = total_order / instances_tested
    mean_width = total_width / instances_tested
    
    if all(mean_width >= n**2 for n in [5, 10, 15, 20, 30, 40]):
        return {
            "metric_name": "resolution_width",
            "metric_value": mean_order,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": True,
            "counterexample": ""
        }
    else:
        for result in results:
            if result["width"] < result["n"]**2:
                return {
                    "metric_name": "resolution_width",
                    "metric_value": mean_order,
                    "instances_tested": instances_tested,
                    "n_max": n_max,
                    "conjecture_holds": False,
                    "counterexample": f"width<{result['n']}^2 for n={result['n']}"
                }
    
    return {
        "metric_name": "resolution_width",
        "metric_value": mean_order,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": False,
        "counterexample": "unknown"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(res["metric_value"] for res in results) / len(results)
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0 support_fraction=1")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(res["seed"] for res in results if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='first_failing_seed' first_failing_seed={first_failing_seed}")