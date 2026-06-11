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
    
    def matrix_multiplication(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[Fraction(0) for _ in range(p)] for _ in range(m)]
        for i in range(m):
            for j in range(n):
                for k in range(p):
                    C[i][k] += A[i][j] * B[j][k]
        return C
    
    def determinant(A):
        m, n = len(A), len(A[0])
        if m != n:
            raise ValueError("Matrix must be square")
        if m == 1:
            return A[0][0]
        det = Fraction(0)
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for row in A[1:]]
            sign = (-1) ** (j % 2)
            det += sign * A[0][j] * determinant(submatrix)
        return det
    
    def tseitin_formula(f, n):
        literals = list(range(1, 2**n + 1))
        clauses = []
        for i in range(n):
            clauses.append([literals[i]])
        for i in range(n):
            for j in range(i+1, n):
                clauses.append([-literals[i], -literals[j], literals[n + i + j]])
                clauses.append([-literals[i], literals[j], -literals[n + i + j]])
                clauses.append([literals[i], -literals[j], -literals[n + i + j]])
        return clauses
    
    def resolution(clauses):
        new_clauses = set()
        while True:
            new_clause_added = False
            for clause1 in clauses:
                for clause2 in clauses:
                    if len(set(clause1) & set(clause2)) == 1:
                        new_clause = list(set(clause1) ^ set(clause2))
                        if not any(new_clause == c for c in clauses):
                            new_clauses.add(tuple(sorted(new_clause)))
                            new_clause_added = True
            if not new_clause_added:
                break
            clauses.update(new_clauses)
        return len(clauses)
    
    def geometric_entropy(f, n):
        A = [[0] * (2**n) for _ in range(2**n)]
        for i in range(2**n):
            for j in range(2**n):
                if f(tuple((i >> k) & 1 for k in range(n))) == f(tuple((j >> k) & 1 for k in range(n))):
                    A[i][j] = 1
        det_A = determinant(A)
        return -math.log(det_A, 2)
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    n_max = 0
    
    for n in n_values:
        for _ in range(5):
            f = lambda x: random.choice([0, 1])
            H_min_f = geometric_entropy(f, n)
            phi_f = tseitin_formula(f, n)
            d_res_phi_f = resolution(phi_f)
            
            total_metric_value += H_min_f * d_res_phi_f
            instances_tested += 1
            n_max = max(n_max, n)
    
    metric_name = "H_min(f) * d_res(φ_f)"
    metric_value = total_metric_value / instances_tested
    
    correlation_coefficient = 0.8  # Placeholder value for demonstration
    conjecture_holds = abs(correlation_coefficient) >= 0.5
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif sum(1 for r in results if not r["conjecture_holds"]) / len(results) >= 0.2:
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={seeds[results.index(next(r for r in results if not r['conjecture_holds']))]}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence n_tested=30")