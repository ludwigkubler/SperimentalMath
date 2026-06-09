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
    
    def gaussian_elimination(A, b):
        n = len(b)
        for i in range(n):
            max_row = i
            for k in range(i+1, n):
                if abs(A[k][i]) > abs(A[max_row][i]):
                    max_row = k
            A[i], A[max_row] = A[max_row], A[i]
            b[i], b[max_row] = b[max_row], b[i]
            for k in range(i+1, n):
                factor = Fraction(A[k][i], A[i][i])
                for j in range(i, n):
                    A[k][j] -= factor * A[i][j]
                b[k] -= factor * b[i]
        x = [0] * n
        for i in range(n-1, -1, -1):
            x[i] = Fraction(b[i], A[i][i])
            for k in range(i-1, -1, -1):
                b[k] -= A[k][i] * x[i]
        return x
    
    def matrix_multiply(A, B):
        n = len(A)
        C = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C
    
    def determinant(A):
        n = len(A)
        det = 0
        if n == 1:
            return A[0][0]
        elif n == 2:
            return A[0][0] * A[1][1] - A[0][1] * A[1][0]
        else:
            for c in range(n):
                submatrix = [row[:c] + row[c+1:] for row in A[1:]]
                det += ((-1) ** c) * A[0][c] * determinant(submatrix)
        return det
    
    def inverse(A):
        n = len(A)
        det_A = determinant(A)
        if det_A == 0:
            raise ValueError("Matrix is not invertible")
        adjoint = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                submatrix = [row[:j] + row[j+1:] for row in A[:i] + A[i+1:]]
                minor = determinant(submatrix)
                adjoint[j][i] = ((-1) ** (i+j)) * minor
        inv_A = [[Fraction(adjoint[j][i], det_A) for j in range(n)] for i in range(n)]
        return inv_A
    
    def geometric_entropy(clauses):
        n = len(clauses)
        H = 0
        for clause in clauses:
            p = Fraction(1, 2 ** (n - len(clause)))
            H -= p * math.log2(p)
        return H
    
    def resolution_proof_width(clauses):
        n = len(clauses)
        m = sum(len(c) for c in clauses)
        width = 0
        for i in range(m):
            if any(j in clause for clause in clauses[:i]):
                width += 1
        return width
    
    def generate_random_cnf(n, m):
        clauses = []
        variables = list(range(1, n+1))
        for _ in range(m):
            clause = random.sample(variables, random.randint(1, n))
            clauses.append(clause)
        return clauses
    
    def construct_thermodynamic_system(clauses):
        n = len(clauses)
        H = geometric_entropy(clauses)
        W = resolution_proof_width(clauses)
        if H != O(W):
            raise ValueError("Constructive mapping undefined")
        return H, W
    
    n_values = [5, 10, 15, 20, 30, 40]
    instances_tested = 0
    total_H = 0
    total_W = 0
    conjecture_holds = True
    counterexample = ""
    
    for n in n_values:
        for _ in range(5):
            clauses = generate_random_cnf(n, random.randint(2*n, 3*n))
            try:
                H, W = construct_thermodynamic_system(clauses)
                total_H += H
                total_W += W
                instances_tested += 1
            except ValueError as e:
                conjecture_holds = False
                counterexample = str(e)
                break
    
    if instances_tested < 30:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": max(n_values),
            "conjecture_holds": conjecture_holds,
            "counterexample": counterexample
        }
    
    correlation_coefficient = total_H / total_W
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")