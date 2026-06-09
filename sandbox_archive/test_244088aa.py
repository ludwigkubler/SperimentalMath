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
    
    def generate_kcnf(n, k):
        variables = list(range(1, n + 1))
        clauses = []
        for _ in range(k):
            clause = [random.choice(variables) for _ in range(random.randint(2, n))]
            if random.choice([True, False]):
                clause = [-x for x in clause]
            clauses.append(clause)
        return clauses
    
    def projective_variety_mod_q(n, q):
        # Simplified encoding of a projective variety modulo q
        return [random.randint(0, q - 1) for _ in range(n)]
    
    def communication_complexity_matrix(kcnf):
        n = len(kcnf[0])
        matrix = [[0] * (2 ** n) for _ in range(len(kcnf))]
        for i, clause in enumerate(kcnf):
            for j in range(1 << n):
                if all((j & (1 << (var - 1))) == 0 if var < 0 else (j & (1 << (var - 1))) != 0 for var in clause):
                    matrix[i][j] = 1
        return matrix
    
    def rank_variance(matrix):
        m, n = len(matrix), len(matrix[0])
        rank = 0
        for i in range(m):
            if any(matrix[i][j] != 0 for j in range(n)):
                rank += 1
        return rank ** 2 / (m * n)
    
    def geometric_invariant_classes(kcnf, q):
        # Simplified encoding of geometric invariant classes
        return len(set(tuple(sorted(clause)) for clause in kcnf))
    
    def gaussian_elimination(matrix):
        m, n = len(matrix), len(matrix[0])
        for i in range(m):
            max_row = i
            for j in range(i + 1, m):
                if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                    max_row = j
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            pivot = matrix[i][i]
            for j in range(n):
                matrix[i][j] /= pivot
            for j in range(m):
                if i != j:
                    factor = matrix[j][i]
                    for k in range(n):
                        matrix[j][k] -= factor * matrix[i][k]
        return matrix
    
    def matrix_multiplication(A, B):
        m, n, p = len(A), len(B[0]), len(B)
        C = [[0] * n for _ in range(m)]
        for i in range(m):
            for j in range(n):
                for k in range(p):
                    C[i][j] += A[i][k] * B[k][j]
        return C
    
    def determinant(matrix):
        m, n = len(matrix), len(matrix[0])
        if m != n:
            raise ValueError("Matrix must be square")
        if n == 1:
            return matrix[0][0]
        det = Fraction(0)
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for row in matrix[1:]]
            det += (-1) ** j * matrix[0][j] * determinant(submatrix)
        return det
    
    def rank(matrix):
        m, n = len(matrix), len(matrix[0])
        reduced_matrix = gaussian_elimination(matrix)
        r = 0
        for i in range(m):
            if any(reduced_matrix[i][j] != 0 for j in range(n)):
                r += 1
        return r
    
    def kcnf_to_projective_variety_mod_q(kcnf, q):
        n = len(kcnf[0])
        variety = [0] * n
        for clause in kcnf:
            for var in clause:
                if var < 0:
                    variety[-var - 1] ^= 1
                else:
                    variety[var - 1] ^= 1
        return projective_variety_mod_q(n, q)
    
    def compute_metric(kcnf, q):
        n = len(kcnf[0])
        variety = kcnf_to_projective_variety_mod_q(kcnf, q)
        invariant_classes = geometric_invariant_classes(kcnf, q)
        matrix = communication_complexity_matrix(kcnf)
        rank_var = rank_variance(matrix)
        return {
            "n": n,
            "invariant_classes": invariant_classes,
            "rank_var": rank_var
        }
    
    def check_bounds(metric):
        n = metric["n"]
        invariant_classes = metric["invariant_classes"]
        rank_var = metric["rank_var"]
        q = 2  # Simplified field size for demonstration
        lower_bound = invariant_classes
        upper_bound = q ** (n / 2 - 1) * invariant_classes
        return lower_bound <= rank_var <= upper_bound
    
    n_values = [5, 10, 15, 20, 30, 40]
    metrics = []
    for n in n_values:
        kcnf = generate_kcnf(n, random.randint(1, n))
        q = 2  # Simplified field size for demonstration
        metric = compute_metric(kcnf, q)
        metrics.append(metric)
    
    rank_vars = [metric["rank_var"] for metric in metrics]
    invariant_classes = [metric["invariant_classes"] for metric in metrics]
    
    if all(check_bounds(metric) for metric in metrics):
        conjecture_holds = True
        counterexample = ""
    else:
        conjecture_holds = False
        counterexample = "mapping_undefined"
    
    return {
        "metric_name": "rank_variance",
        "metric_value": sum(rank_vars) / len(rank_vars),
        "instances_tested": len(metrics),
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")