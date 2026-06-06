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

def generate_cnf(n):
    cnf = []
    for _ in range(2 * n):
        clause = set()
        while len(clause) < 3:
            lit = random.choice([-i, i] for i in range(1, n + 1))
            if lit not in clause and -lit not in clause:
                clause.add(lit)
        cnf.append(tuple(sorted(clause)))
    return cnf

def hodge_norm(cnf):
    m = len(cnf)
    n = max(abs(lit) for clause in cnf for lit in clause)
    A = [[0] * (n + 1) for _ in range(n + 1)]
    for clause in cnf:
        for lit in clause:
            A[abs(lit)][abs(lit)] += 1
    det = determinant(A, n + 1)
    return abs(det)

def determinant(matrix, n):
    if n == 1:
        return matrix[0][0]
    det = 0
    for j in range(n):
        det += ((-1) ** j) * matrix[0][j] * determinant(minor(matrix, 0, j), n - 1)
    return det

def minor(matrix, i, j):
    return [row[:j] + row[j+1:] for row in matrix[1:]]

def resolution_width(cnf):
    stack = []
    assignment = {}
    for clause in cnf:
        if all(lit not in assignment for lit in clause):
            stack.append(clause)
        else:
            resolved = False
            while stack and not resolved:
                top_clause = stack.pop()
                for lit in top_clause:
                    if -lit in assignment:
                        resolved = True
                        break
                if resolved:
                    new_assignment = {**assignment, -lit: True}
                    new_clause = [l for l in top_clause if l != -lit]
                    if not all(lit in new_assignment for lit in new_clause):
                        stack.append(new_clause)
    return len(stack)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    metrics = []
    
    for n in n_values:
        cnf = generate_cnf(n)
        hodge_norm_value = hodge_norm(cnf)
        width_value = resolution_width(cnf)
        metrics.append((hodge_norm_value, width_value))
        
        if len(metrics) >= 30:
            break
    
    if len(metrics) < 10:
        return {
            "metric_name": "Hodge Norm vs Resolution Width",
            "metric_value": None,
            "instances_tested": len(metrics),
            "n_max": max(n_values[:len(metrics)]),
            "conjecture_holds": False,
            "counterexample": "Not enough instances tested"
        }
    
    hodge_norms = [m[0] for m in metrics]
    widths = [m[1] for m in metrics]
    mean_hodge_norm = sum(hodge_norms) / len(hodge_norms)
    mean_width = sum(widths) / len(widths)
    correlation = (sum((h - mean_hodge_norm) * (w - mean_width) for h, w in zip(hodge_norms, widths)) /
                    (len(metrics) * (sum((h - mean_hodge_norm) ** 2 for h in hodge_norms) / len(hodge_norms)) *
                     sum((w - mean_width) ** 2 for w in widths) / len(widths))) if len(metrics) > 1 else 0
    
    return {
        "metric_name": "Hodge Norm vs Resolution Width",
        "metric_value": correlation,
        "instances_tested": len(metrics),
        "n_max": max(n_values[:len(metrics)]),
        "conjecture_holds": correlation >= 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{'seed': {seed}, **result}}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_metric_value = (sum((r["metric_value"] - mean_metric_value) ** 2 for r in results if r["metric_value"] is not None) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                print(f"RESULT: FALSIFIED counterexample=\"Not enough instances tested\" first_failing_seed={r['seed']}")
                break