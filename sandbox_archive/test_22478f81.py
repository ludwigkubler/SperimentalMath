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
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i
            for j in range(i+1, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            for j in range(i+1, m):
                factor = A[j][i] / A[i][i]
                for k in range(n):
                    A[j][k] -= factor * A[i][k]
        return A
    
    def rank(A):
        A = gaussian_elimination(A)
        r = 0
        for row in A:
            if any(row):
                r += 1
        return r
    
    def dpll_search_tree_height(clauses, assignment):
        if not clauses:
            return 0
        if all(any(lit in assignment and assignment[lit] == val for lit, val in clause) for clause in clauses):
            return 0
        literals = set()
        for clause in clauses:
            literals.update(clause)
        literal = random.choice(list(literals))
        true_clauses = [c for c in clauses if any(lit in assignment and assignment[lit] == val for lit, val in c)]
        false_clauses = [c for c in clauses if all(lit not in assignment or assignment[lit] != val for lit, val in c)]
        return 1 + max(dpll_search_tree_height(true_clauses, {**assignment, literal: True}),
                      dpll_search_tree_height(false_clauses, {**assignment, literal: False}))
    
    def mls(G):
        n = len(G)
        A = [[0] * (n+1) for _ in range(n+1)]
        for i in range(1, n+1):
            A[i][i] = 1
            for j in range(i+1, n+1):
                if G[i-1][j-1]:
                    A[i][j], A[j][i] = 1, 1
        return rank(A)
    
    def generate_cnf(n):
        clauses = []
        for _ in range(2*n):
            clause = [random.choice([-1, 1]) * (i+1) for i in range(n)]
            if all(clause[i] != -clause[j] for i in range(n) for j in range(i+1, n)):
                clauses.append(clause)
        return clauses
    
    def correlation_coefficient(x, y):
        mean_x = sum(x) / len(x)
        mean_y = sum(y) / len(y)
        cov = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y)) / len(x)
        std_x = math.sqrt(sum((xi - mean_x) ** 2 for xi in x) / len(x))
        std_y = math.sqrt(sum((yi - mean_y) ** 2 for yi in y) / len(y))
        return cov / (std_x * std_y)
    
    n_max = 0
    mls_values = []
    height_values = []
    
    for _ in range(30):
        n = random.randint(5, 40)
        n_max = max(n_max, n)
        G = generate_cnf(n)
        mls_value = mls(G)
        height_value = dpll_search_tree_height(G, {})
        mls_values.append(mls_value)
        height_values.append(height_value)
    
    correlation = correlation_coefficient(mls_values, height_values)
    support_fraction = sum(1 for c in correlation_values if c >= 0.5) / len(correlation_values)
    metric_mean = sum(correlation_values) / len(correlation_values)
    
    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": correlation,
        "instances_tested": 30,
        "n_max": n_max,
        "conjecture_holds": support_fraction >= 0.8 and metric_mean <= 3,
        "counterexample": "" if support_fraction >= 0.8 else f"Correlation coefficient < 0.5 in {support_fraction * 100}% of seeds"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    metric_mean = sum(r["metric_value"] for r in results) / len(results)
    
    if support_fraction >= 0.8 and metric_mean <= 3:
        print(f"RESULT: SUPPORTED mean={metric_mean} std=NA support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Correlation coefficient < 0.5\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_support_fraction")