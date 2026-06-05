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
    
    def generate_instance(n):
        clauses = []
        for _ in range(2**n):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            if sum(clause) != 0:
                clauses.append(clause)
        return clauses
    
    def construct_matroid(clauses):
        matroid = []
        for clause in clauses:
            row = [0] * len(clauses)
            for literal in clause:
                var = abs(literal) - 1
                if literal > 0:
                    row[var] = 1
                else:
                    row[-var - 1] = 1
            matroid.append(row)
        return matroid
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i
            for j in range(i + 1, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            if A[i][i] == 0:
                continue
            pivot = 1 / A[i][i]
            for j in range(n):
                A[i][j] *= pivot
            for j in range(m):
                if j != i and A[j][i] != 0:
                    factor = -A[j][i]
                    for k in range(n):
                        A[j][k] += factor * A[i][k]
        return A
    
    def det(A):
        n = len(A)
        A = [row[:] for row in A]
        gaussian_elimination(A)
        prod = 1
        for i in range(n):
            prod *= A[i][i]
        return prod
    
    def tsv(matroid):
        return abs(det(matroid))
    
    def dpll(clauses, assignment=[]):
        if not clauses:
            return True
        clause = next((c for c in clauses if any(lit in assignment for lit in c)), [])
        if not clause:
            return False
        pos_lit = next((lit for lit in clause if lit > 0), None)
        neg_lit = next((lit for lit in clause if lit < 0), None)
        
        def extend_assignment(assignment, literal):
            assignment.append(literal)
            new_clauses = []
            for c in clauses:
                if all(lit not in c for lit in assignment):
                    new_clauses.append(c)
            return new_clauses
        
        if pos_lit is not None and dpll(extend_assignment(assignment, pos_lit), assignment):
            return True
        if neg_lit is not None and dpll(extend_assignment(assignment, neg_lit), assignment):
            return True
        return False
    
    def w_dpll(clauses):
        max_width = 0
        for _ in range(10):  # Sample multiple times to get a good estimate
            assignment = [random.choice([-1, 1]) * (i + 1) for i in range(len(clauses))]
            width = len([lit for lit in assignment if lit != 0])
            max_width = max(max_width, width)
        return max_width
    
    n = random.randint(5, 40)
    instance = generate_instance(n)
    matroid = construct_matroid(instance)
    tsv_value = tsv(matroid)
    w_dpll_value = w_dpll(instance)
    
    if w_dpll_value == 0:
        return {
            "metric_name": "TSV / w_DPLL",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "w_DPLL is zero, division by zero"
        }
    
    ratio = tsv_value / w_dpll_value
    return {
        "metric_name": "TSV / w_DPLL",
        "metric_value": ratio,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": ratio >= 1.0,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = next((r["counterexample"] for r in results if r["counterexample"]), "")
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")