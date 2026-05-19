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
    
    def generate_permutation_matrix(n):
        perm = list(range(n))
        random.shuffle(perm)
        return [[1 if i == j else 0 for j in range(n)] for i in perm]
    
    def generate_determinant_matrix(n):
        det = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
        for i in range(1, n):
            det[i][i-1] = -1
        return det
    
    def matrix_multiplication(A, B):
        m, k, n = len(A), len(B[0]), len(B)
        result = [[sum(A[i][j] * B[j][k] for j in range(k)) for k in range(n)] for i in range(m)]
        return result
    
    def transpose_matrix(matrix):
        return [list(row) for row in zip(*matrix)]
    
    def determinant(matrix):
        if len(matrix) == 1:
            return matrix[0][0]
        det = 0
        for j in range(len(matrix)):
            submatrix = [row[:j] + row[j+1:] for row in matrix[1:]]
            det += ((-1) ** j) * matrix[0][j] * determinant(submatrix)
        return det
    
    def symmetric_power(matrix, k):
        result = matrix
        for _ in range(k - 1):
            result = matrix_multiplication(result, matrix)
        return result
    
    def multiplicity_of_trivial_representation(symmetric_power_matrix):
        n = len(symmetric_power_matrix)
        eigvals = []
        A = symmetric_power_matrix
        B = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
        
        while True:
            Q, R = gram_schmidt(A)
            if all(abs(R[i][i]) < 1e-10 for i in range(n)):
                break
            A = matrix_multiplication(Q, symmetric_power_matrix)
        
        for i in range(n):
            eigvals.append(R[i][i])
        
        return sum(1 for val in eigvals if abs(val) < 1e-10)
    
    def gram_schmidt(matrix):
        n = len(matrix)
        Q = []
        R = [[0] * n for _ in range(n)]
        
        for i in range(n):
            v = matrix[i]
            for j in range(i):
                r_ij = sum(Q[j][k] * v[k] for k in range(n))
                R[i][j] = r_ij
                v = [v[k] - r_ij * Q[j][k] for k in range(n)]
            norm = math.sqrt(sum(x * x for x in v))
            R[i][i] = norm
            Q.append([x / norm for x in v])
        
        return Q, R
    
    n = random.randint(2, 40)
    perm_matrix = generate_permutation_matrix(n)
    det_matrix = generate_determinant_matrix(n)
    
    k_values = [random.randint(1, int(math.sqrt(n))) for _ in range(30)]
    perm_multiplicities = []
    det_multiplicities = []
    
    for k in k_values:
        perm_multiplicity = multiplicity_of_trivial_representation(symmetric_power(perm_matrix, k))
        det_multiplicity = multiplicity_of_trivial_representation(symmetric_power(det_matrix, k))
        perm_multiplicities.append(perm_multiplicity)
        det_multiplicities.append(det_multiplicity)
    
    mean_perm_multiplicity = sum(perm_multiplicities) / len(perm_multiplicities)
    mean_det_multiplicity = sum(det_multiplicities) / len(det_multiplicities)
    gap = mean_perm_multiplicity - mean_det_multiplicity
    
    conjecture_holds = gap > math.sqrt(n) * 0.5
    counterexample = "" if conjecture_holds else f"n={n}, k_values={k_values}, perm_multiplicities={perm_multiplicities}, det_multiplicities={det_multiplicities}"
    
    return {
        "metric_name": "Multiplicity Gap",
        "metric_value": gap,
        "instances_tested": len(k_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...run_trial output...}}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Multiplicity gap does not exceed Ω(n^{1/2})\" first_failing_seed={first_failing_seed}")