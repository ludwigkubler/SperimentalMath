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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(n):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            if sum(clause) != 0:
                clauses.append(clause)
        return clauses
    
    def cnf_to_polynomial(cnf):
        n = len(cnf[0])
        poly = [[Fraction(0)] * n for _ in range(n)]
        for clause in cnf:
            for literal in clause:
                var, sign = abs(literal), -1 if literal < 0 else 1
                for j in range(n):
                    if j != var - 1:
                        poly[j][var - 1] += Fraction(sign)
                    else:
                        poly[var - 1][j] += Fraction(sign)
        return poly
    
    def matrix_multiplication(A, B):
        n = len(A)
        C = [[Fraction(0)] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C
    
    def gaussian_elimination(A, b):
        n = len(A)
        for i in range(n):
            max_row = i
            for j in range(i + 1, n):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            b[i], b[max_row] = b[max_row], b[i]
            for j in range(i + 1, n):
                factor = A[j][i] / A[i][i]
                for k in range(n):
                    A[j][k] -= factor * A[i][k]
                b[j] -= factor * b[i]
        x = [Fraction(0)] * n
        for i in range(n - 1, -1, -1):
            x[i] = (b[i] - sum(A[i][j] * x[j] for j in range(i + 1, n))) / A[i][i]
        return x
    
    def discriminant(poly):
        n = len(poly)
        det = Fraction(0)
        for i in range(n):
            det += (-1) ** i * poly[0][i] * determinant([[poly[j][k] for k in range(j + 1, n)] for j in range(i + 1, n)])
        return det
    
    def determinant(matrix):
        n = len(matrix)
        if n == 1:
            return matrix[0][0]
        det = Fraction(0)
        for j in range(n):
            submatrix = [[matrix[i][k] for k in range(j + 1, n)] for i in range(1, n)]
            det += (-1) ** j * matrix[0][j] * determinant(submatrix)
        return det
    
    def frege_proof_length(cnf):
        # Placeholder function; actual implementation needed
        return len(cnf) * 5  # Simplified example
    
    log_discriminants = []
    proof_lengths = []
    
    for n in [5, 10, 15, 20, 30, 40]:
        cnf = generate_cnf(n)
        poly = cnf_to_polynomial(cnf)
        det = discriminant(poly)
        log_discriminants.append(math.log(abs(det)))
        proof_lengths.append(frege_proof_length(cnf))
    
    if not log_discriminants or not proof_lengths:
        return {
            "metric_name": "log(discriminant)",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "empty_data"
        }
    
    n = len(log_discriminants)
    mean_x = sum(log_discriminants) / n
    mean_y = sum(proof_lengths) / n
    
    numerator = sum((log_discriminants[i] - mean_x) * (proof_lengths[i] - mean_y) for i in range(n))
    denominator = sum((log_discriminants[i] - mean_x) ** 2 for i in range(n)) * sum((proof_lengths[i] - mean_y) ** 2 for i in range(n))
    
    if denominator == 0:
        return {
            "metric_name": "log(discriminant)",
            "metric_value": None,
            "instances_tested": n,
            "n_max": max(5, 10, 15, 20, 30, 40),
            "conjecture_holds": False,
            "counterexample": "zero_denominator"
        }
    
    r_squared = numerator ** 2 / denominator
    
    return {
        "metric_name": "log(discriminant)",
        "metric_value": r_squared,
        "instances_tested": n,
        "n_max": max(5, 10, 15, 20, 30, 40),
        "conjecture_holds": r_squared >= 0.9 and p_value <= 0.01,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_value = sum(result["metric_value"] for result in results) / len(results)
        std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
        support_fraction = len([result for result in results if result["conjecture_holds"]]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='<not provided>' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no_data")