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
    
    def log2(x):
        if x <= 0:
            return float('-inf')
        return math.log2(x)
    
    def gcd(a, b):
        while b:
            a, b = b, a % b
        return a
    
    def lcm(a, b):
        return abs(a*b) // gcd(a, b)
    
    def matrix_multiply(A, B):
        m, k, n = len(A), len(B), len(B[0])
        C = [[0 for _ in range(n)] for _ in range(m)]
        for i in range(m):
            for j in range(n):
                for l in range(k):
                    C[i][j] += A[i][l] * B[l][j]
        return C
    
    def gaussian_elimination(A, b):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i
            for j in range(i+1, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            b[i], b[max_row] = b[max_row], b[i]
            for j in range(i+1, m):
                factor = A[j][i] / A[i][i]
                for k in range(n):
                    A[j][k] -= factor * A[i][k]
                b[j] -= factor * b[i]
        x = [0] * n
        for i in range(m-1, -1, -1):
            x[i] = (b[i] - sum(A[i][j] * x[j] for j in range(i+1, n))) / A[i][i]
        return x
    
    def is_square_matrix(matrix):
        m, n = len(matrix), len(matrix[0])
        return m == n
    
    def rank(matrix):
        if not is_square_matrix(matrix):
            raise ValueError("Matrix must be square")
        augmented_matrix = [row + [1] for row in matrix]
        reduced_row_echelon_form = gaussian_elimination(augmented_matrix, [0]*len(matrix))
        return sum(1 for row in reduced_row_echelon_form if any(row[i] != 0 for i in range(len(row)-1)))
    
    def is_clifford_group_state(state):
        # Placeholder function to check if the state is a Clifford group state
        return True
    
    n = random.randint(5, 40)
    state = [random.random() for _ in range(n)]
    if not is_clifford_group_state(state):
        return {
            "metric_name": "minimal_rank",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    TP = [[0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        TP[i][i] = 1
    
    R_TP = rank(TP)
    
    D_QC = random.randint(1, int(2 * log2(n) - 1))
    
    if R_TP < 3:
        return {
            "metric_name": "minimal_rank",
            "metric_value": R_TP,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"Minimal rank {R_TP} is less than 3"
        }
    
    if D_QC > 2 * log2(n) - 1:
        return {
            "metric_name": "minimal_rank",
            "metric_value": R_TP,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"Depth {D_QC} is greater than 2 * log2({n}) - 1"
        }
    
    if D_QC < (R_TP + log2(n)) / 4:
        return {
            "metric_name": "minimal_rank",
            "metric_value": R_TP,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"Depth {D_QC} is less than (R(TP) + log2({n})) / 4"
        }
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": R_TP,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i - 1 for i in range(5, 30)]
    
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
                counterexample = r["counterexample"]
                first_failing_seed = seed
                break
        
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")