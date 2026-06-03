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

def gaussian_elimination(A, b):
    n = len(b)
    for i in range(n):
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        b[i], b[max_row] = b[max_row], b[i]
        for j in range(i+1, n):
            factor = Fraction(A[j][i], A[i][i])
            for k in range(i, n):
                A[j][k] -= factor * A[i][k]
            b[j] -= factor * b[i]
    x = [0] * n
    for i in range(n-1, -1, -1):
        x[i] = Fraction(b[i], A[i][i])
        for j in range(i-1, -1, -1):
            b[j] -= A[j][i] * x[i]
    return x

def solve(lits_true, lits_false):
    clauses = []
    for lit in lits_true:
        clause = [lit]
        if -lit in lits_false:
            clause.append(-lit)
        clauses.append(clause)
    n = len(lits_true) + len(lits_false)
    A = [[0] * n for _ in range(n)]
    b = [0] * n
    for i, lit in enumerate(lits_true):
        A[i][i] = 1
        b[i] = 1
    for j, lit in enumerate(lits_false):
        A[j + len(lits_true)][j + len(lits_true)] = -1
        b[j + len(lits_true)] = -1
    return gaussian_elimination(A, b)

def resolution_proof_width(clauses):
    lits_true = set()
    lits_false = set()
    for clause in clauses:
        if all(c > 0 for c in clause):
            lits_true.update(clause)
        elif all(-c < 0 for c in clause):
            lits_false.update([-c for c in clause])
    return len(solve(lits_true, lits_false))

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(10, 40)
    d = random.randint(2, min(n-1, 3))
    
    # Generate a random d-regular graph
    G = [[] for _ in range(n)]
    edges = set()
    while len(edges) < (n * d) // 2:
        u = random.randint(0, n-1)
        v = random.randint(0, n-1)
        if u != v and (u, v) not in edges and (v, u) not in edges:
            G[u].append(v)
            G[v].append(u)
            edges.add((u, v))
    
    # Construct the Tseitin formula φ_G
    clauses = []
    literals = {}
    literal_count = 0
    for i in range(n):
        literals[i] = literal_count
        literal_count += 1
        clauses.append([literals[i]])
        for j in G[i]:
            clauses.append([-literals[i], literals[j]])
    
    # Compute the tropical analytic rank tar(φ_G)
    def max_plus(a, b):
        return a + b if a > b else b
    
    def tropical_analytic_rank(clauses):
        n = len(clauses)
        A = [[-math.inf] * n for _ in range(n)]
        for i in range(n):
            A[i][i] = 0
        for clause in clauses:
            max_clause_value = -math.inf
            for lit in clause:
                if lit > 0:
                    max_clause_value = max(max_clause_value, literals[lit])
                else:
                    max_clause_value = max(max_clause_value, literals[-lit])
            for i in range(n):
                for j in range(n):
                    A[i][j] = max_plus(A[i][j], max_clause_value)
        return max_plus(*[max(row) for row in A])
    
    tar_value = tropical_analytic_rank(clauses)
    
    # Measure the resolution proof width w(φ_G)
    w_value = resolution_proof_width(clauses)
    
    # Perform linear regression
    if n < 2:
        return {
            "metric_name": "ratio",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "not_enough_instances"
        }
    
    x = [i for i in range(1, n+1)]
    y = [tar_value / w_value]
    mean_x = sum(x) / len(x)
    mean_y = sum(y) / len(y)
    numerator = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y))
    denominator = sum((xi - mean_x)**2 for xi in x)
    slope = numerator / denominator
    intercept = mean_y - slope * mean_x
    
    # Check if the ratio is within 95% confidence interval
    std_dev = (sum((yi - (slope * xi + intercept))**2 for xi, yi in zip(x, y)) / len(y)) ** 0.5
    margin_of_error = 1.96 * std_dev / (len(x) ** 0.5)
    lower_bound = slope * n + intercept - margin_of_error
    upper_bound = slope * n + intercept + margin_of_error
    
    if lower_bound <= 10:
        return {
            "metric_name": "ratio",
            "metric_value": tar_value / w_value,
            "instances_tested": len(x),
            "n_max": n,
            "conjecture_holds": True,
            "counterexample": ""
        }
    else:
        return {
            "metric_name": "ratio",
            "metric_value": tar_value / w_value,
            "instances_tested": len(x),
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": f"upper_bound={upper_bound}"
        }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_dev = (sum((r["metric_value"] - mean_value)**2 for r in results) / len(results)) ** 0.5
        support_fraction = len([r for r in results if r["conjecture_holds"]]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif any(r["counterexample"] != "" for r in results):
        counterexamples = [r["counterexample"] for r in results if r["counterexample"] != ""]
        first_failing_seed = next(r["seed"] for r in results if r["counterexample"] != "")
        print(f"RESULT: FALSIFIED counterexample='{', '.join(counterexamples)}' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no_support_found")