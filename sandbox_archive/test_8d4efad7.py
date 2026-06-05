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
                factor = Fraction(A[j][i], A[i][i])
                for k in range(n):
                    A[j][k] -= factor * A[i][k]
        return A
    
    def matrix_multiply(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[Fraction(0, 1) for _ in range(p)] for _ in range(m)]
        for i in range(m):
            for j in range(p):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C
    
    def determinant(A):
        m, n = len(A), len(A[0])
        if m != n:
            raise ValueError("Matrix must be square")
        if n == 1:
            return A[0][0]
        det = Fraction(0, 1)
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for row in A[1:]]
            det += (-1)**j * A[0][j] * determinant(submatrix)
        return det
    
    def is_invertible(A):
        return determinant(A) != Fraction(0, 1)
    
    def construct_groupoid(clauses):
        n = len(clauses[0])
        groupoid = [[Fraction(0, 1)] * (2**n) for _ in range(2**n)]
        for clause in clauses:
            mask = 0
            for var in clause:
                if var > 0:
                    mask |= 1 << (var - 1)
                else:
                    mask |= 1 << (-var - 1)
            groupoid[mask][mask] = Fraction(1, 1)
        return groupoid
    
    def resolution_width(clauses):
        n = len(clauses[0])
        clauses = [tuple(sorted(c)) for c in clauses]
        clauses = list(set(clauses))
        
        queue = set()
        for clause in clauses:
            if len(clause) == 1:
                queue.add(clause)
        
        width = 0
        while queue:
            new_queue = set()
            for clause in queue:
                if len(clause) == 1:
                    continue
                var, rest = clause[0], clause[1:]
                for other_clause in clauses:
                    if var not in other_clause and -var in other_clause:
                        new_clause = tuple(sorted(set(other_clause) ^ {var}))
                        if new_clause not in queue:
                            new_queue.add(new_clause)
            queue.update(new_queue)
            width += 1
        
        return width
    
    def min_categorical_dimension(groupoid):
        m, n = len(groupoid), len(groupoid[0])
        for i in range(m):
            for j in range(n):
                if groupoid[i][j] != Fraction(0, 1) and groupoid[j][i] != Fraction(0, 1):
                    return max(i, j)
        return m
    
    def generate_formula(n):
        clauses = []
        for _ in range(n * n):
            clause = random.sample(range(-n, n+1), 2)
            if clause[0] == -clause[1]:
                continue
            clauses.append(clause)
        return clauses
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        for _ in range(5):
            formula = generate_formula(n)
            groupoid = construct_groupoid(formula)
            dim = min_categorical_dimension(groupoid)
            width = resolution_width(formula)
            results.append((dim, width))
    
    if not results:
        return {
            "metric_name": "min_categorical_dimension vs resolution_width",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    dim_values = [r[0] for r in results]
    width_values = [r[1] for r in results]
    
    mean_dim = sum(dim_values) / len(dim_values)
    mean_width = sum(width_values) / len(width_values)
    
    if any(d > 5 * mean_width for d in dim_values):
        return {
            "metric_name": "min_categorical_dimension vs resolution_width",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "dim > 5 * mean_width"
        }
    
    return {
        "metric_name": "min_categorical_dimension vs resolution_width",
        "metric_value": None,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"dim > 5 * mean_width\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no seeds tested")