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
            for j in range(i+1, n):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            b[i], b[max_row] = b[max_row], b[i]
            for j in range(i+1, n):
                factor = A[j][i] / A[i][i]
                for k in range(i, n):
                    A[j][k] -= factor * A[i][k]
                b[j] -= factor * b[i]
        x = [0] * n
        for i in range(n-1, -1, -1):
            x[i] = (b[i] - sum(A[i][j] * x[j] for j in range(i+1, n))) / A[i][i]
        return x
    
    def matrix_multiply(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[0] * p for _ in range(m)]
        for i in range(m):
            for j in range(p):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C
    
    def determinant(A):
        n = len(A)
        if n == 1:
            return A[0][0]
        det = 0
        sign = 1
        for j in range(n):
            submatrix = [[A[i][k] for k in range(n) if k != j] for i in range(1, n)]
            det += sign * A[0][j] * determinant(submatrix)
            sign *= -1
        return det
    
    def inverse(A):
        n = len(A)
        det_A = determinant(A)
        if det_A == 0:
            raise ValueError("Matrix is not invertible")
        adjugate = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                submatrix = [[A[m][k] for k in range(n) if k != j] for m in range(n) if m != i]
                cofactor = determinant(submatrix)
                adjugate[i][j] = (-1)**(i+j) * cofactor
        inv_A = matrix_multiply(adjugate, [[Fraction(1, det_A)] * n for _ in range(n)])
        return inv_A
    
    def gaussian_elimination_fraction(A, b):
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
            x[i] = (b[i] - sum(A[i][j] * x[j] for j in range(i+1, n))) / A[i][i]
        return x
    
    def matrix_multiply_fraction(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[Fraction(0)] * p for _ in range(m)]
        for i in range(m):
            for j in range(p):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C
    
    def determinant_fraction(A):
        n = len(A)
        if n == 1:
            return A[0][0]
        det = Fraction(0)
        sign = 1
        for j in range(n):
            submatrix = [[A[i][k] for k in range(n) if k != j] for i in range(1, n)]
            det += sign * A[0][j] * determinant_fraction(submatrix)
            sign *= -1
        return det
    
    def inverse_fraction(A):
        n = len(A)
        det_A = determinant_fraction(A)
        if det_A == Fraction(0):
            raise ValueError("Matrix is not invertible")
        adjugate = [[Fraction(0)] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                submatrix = [[A[m][k] for k in range(n) if k != j] for m in range(n) if m != i]
                cofactor = determinant_fraction(submatrix)
                adjugate[i][j] = (-1)**(i+j) * cofactor
        inv_A = matrix_multiply_fraction(adjugate, [[Fraction(1, det_A)] * n for _ in range(n)])
        return inv_A
    
    def generate_cnf(n):
        clauses = []
        for i in range(n):
            clause = [random.choice([-1, 1]) * (j+1) for j in range(n)]
            clauses.append(clause)
        return clauses
    
    def clause_complexity(cnf):
        return sum(len(clause) for clause in cnf)
    
    def local_cohomological_defect(cnf):
        n = len(cnf[0])
        A = [[Fraction(0)] * n for _ in range(n)]
        b = [Fraction(0)] * n
        for i in range(n):
            for j in range(n):
                if cnf[i][j] != 0:
                    A[i][j] = Fraction(1, abs(cnf[i][j]))
            b[i] = Fraction(1)
        inv_A = inverse_fraction(A)
        x = gaussian_elimination_fraction(inv_A, b)
        return sum(x[i] * abs(cnf[i][i]) for i in range(n))
    
    def check_property_P(cnf):
        n = len(cnf[0])
        for i in range(n):
            if all(cnf[j][i] == 0 for j in range(n)):
                return False
        return True
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        instances_tested = 0
        n_max = n
        total_metric_value = 0
        for _ in range(50):
            cnf = generate_cnf(n)
            if not check_property_P(cnf):
                continue
            instances_tested += 1
            metric_value = local_cohomological_defect(cnf)
            total_metric_value += metric_value
            results.append({"n": n, "metric_value": metric_value})
    
    if len(results) < 30:
        return {"seed": seed, "conjecture_holds": False, "counterexample": "insufficient_instances"}
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["metric_value"] > 0.7 * mean_metric_value) / len(results)
    
    return {
        "seed": seed,
        "metric_name": "local_cohomological_defect",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": support_fraction >= 0.8,
        "counterexample": "" if support_fraction >= 0.8 else "support_fraction < 0.8"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(result["seed"] for result in results if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"support_fraction < 0.8\" first_failing_seed={first_failing_seed}")