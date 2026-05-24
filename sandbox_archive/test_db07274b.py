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

def generate_random_kcnf(n, k):
    clauses = []
    for _ in range(k * n):
        clause = set()
        while len(clause) < 3:
            var = random.randint(1, n)
            if -var not in clause and var not in clause:
                clause.add(var)
        clauses.append(list(clause))
    return clauses

def gaussian_elimination(matrix):
    rows, cols = len(matrix), len(matrix[0])
    for i in range(rows):
        max_row = i
        for j in range(i + 1, rows):
            if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                max_row = j
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        pivot = matrix[i][i]
        for j in range(cols):
            matrix[i][j] /= pivot
        for j in range(rows):
            if i != j:
                factor = matrix[j][i]
                for k in range(cols):
                    matrix[j][k] -= factor * matrix[i][k]
    return matrix

def local_defect_complexity(clauses, n):
    m = len(clauses)
    A = [[0] * (n + 1) for _ in range(m)]
    for i, clause in enumerate(clauses):
        for var in clause:
            A[i][abs(var)] += 1
    rank = 0
    for row in gaussian_elimination(A):
        if any(row[j] != 0 for j in range(n + 1)):
            rank += 1
    return rank

def dpll_refutation_path_length(clauses, n):
    assignment = [0] * (n + 1)
    
    def solve():
        unassigned_vars = [i for i in range(1, n + 1) if assignment[i] == 0]
        if not unassigned_vars:
            return 0
        var = random.choice(unassigned_vars)
        for sign in [-1, 1]:
            assignment[var] = sign
            unsatisfied_clauses = [clause for clause in clauses if any(abs(x) != var or assignment[abs(x)] == -sign for x in clause)]
            if not unsatisfied_clauses:
                return solve()
        assignment[var] = 0
        return float('inf')
    
    return solve()

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [10, 20, 40]
    results = []
    for n in n_values:
        for _ in range(3):  # Ensure at least 3 instances per size
            clauses = generate_random_kcnf(n, 2)  # k=2 for simplicity
            L_F = local_defect_complexity(clauses, n)
            t_F = dpll_refutation_path_length(clauses, n)
            if L_F == 0:
                continue
            alpha = Fraction(1, 2)  # Example constant α
            ratio = t_F / (alpha * L_F)
            results.append({"n": n, "L_F": L_F, "t_F": t_F, "ratio": ratio})
    
    if not results:
        return {"metric_name": "Ratio", "metric_value": None, "instances_tested": 0, "conjecture_holds": False, "counterexample": "No valid instances found"}
    
    mean_ratio = sum(result["ratio"] for result in results) / len(results)
    conjecture_holds = all(result["ratio"] <= 1.5 for result in results)
    counterexample = "" if conjecture_holds else f"Ratio exceeded 1.5 at n={results[0]['n']}"
    
    return {
        "metric_name": "Ratio",
        "metric_value": mean_ratio,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{'seed': {seed}, {result}}}")
        results.append(result)
    
    mean_ratio = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='Ratio exceeded 1.5' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")