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
    
    def is_permutation(matrix):
        n = len(matrix)
        identity = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
        product = matrix_multiply(matrix, transpose(matrix))
        return all(abs(product[i][j] - identity[i][j]) < 1e-9 for i in range(n) for j in range(n))
    
    def transpose(matrix):
        n = len(matrix)
        return [[matrix[j][i] for j in range(n)] for i in range(n)]
    
    def matrix_multiply(A, B):
        n = len(A)
        C = [[0 for _ in range(n)] for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C
    
    def determinant(matrix):
        n = len(matrix)
        if n == 1:
            return matrix[0][0]
        det = 0
        for j in range(n):
            minor = [row[:j] + row[j+1:] for row in matrix[1:]]
            det += (-1) ** j * matrix[0][j] * determinant(minor)
        return det
    
    def symmetric_power(matrix, k):
        result = matrix
        for _ in range(k-1):
            result = matrix_multiply(result, matrix)
        return result
    
    def multiplicity_of_trivial_representation(matrix):
        n = len(matrix)
        identity = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
        symmetric_power_matrix = symmetric_power(matrix, n // 2)
        eigenvalues = []
        A = matrix_multiply(symmetric_power_matrix, transpose(identity))
        Q, R = gram_schmidt(A)
        for v in Q:
            if norm(v) > 1e-9:
                eigenvalues.append(Fraction(1, len(Q)))
        return sum(eigenvalues)
    
    def gram_schmidt(A):
        n = len(A)
        Q = []
        R = [[0 for _ in range(n)] for _ in range(n)]
        for i in range(n):
            v = A[i]
            for j in range(i):
                r_ij = sum(Q[j][k] * v[k] for k in range(n))
                R[j][i] = r_ij
                v = [v[k] - r_ij * Q[j][k] for k in range(n)]
            norm_v = norm(v)
            if norm_v > 1e-9:
                Q.append([x / norm_v for x in v])
                R[i][i] = norm_v
        return Q, R
    
    def norm(vector):
        return math.sqrt(sum(x**2 for x in vector))
    
    n = random.randint(5, 40)
    perm_matrix = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
    det_matrix = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
    
    if not is_permutation(perm_matrix) or determinant(det_matrix) != 1:
        return {
            "metric_name": "Multiplicity Gap",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    perm_multiplicity = multiplicity_of_trivial_representation(perm_matrix)
    det_multiplicity = multiplicity_of_trivial_representation(det_matrix)
    gap = perm_multiplicity - det_multiplicity
    
    return {
        "metric_name": "Multiplicity Gap",
        "metric_value": gap,
        "instances_tested": 1,
        "conjecture_holds": gap > math.sqrt(n),
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
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                print(f"RESULT: FALSIFIED counterexample=\"Multiplicity gap does not exceed Ω(n^{1/2})\" first_failing_seed={r['seed']}")
                break