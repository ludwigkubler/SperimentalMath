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
    
    def generate_disjointness_instance(n):
        A = [random.randint(0, 1) for _ in range(n * n)]
        B = [random.randint(0, 1) for _ in range(n * n)]
        M = [A[i*n:(i+1)*n] + B[i*n:(i+1)*n] for i in range(n)]
        return M
    
    def matrix_multiplication(A, B):
        m, k, n = len(A), len(B[0]), len(B)
        C = [[sum(A[i][j] * B[j][k] for j in range(k)) for k in range(n)] for i in range(m)]
        return C
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i
            for j in range(i+1, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            for j in range(i+1, m):
                factor = A[j][i] / A[i][i]
                for k in range(n):
                    A[j][k] -= factor * A[i][k]
        return A
    
    def determinant(A):
        n = len(A)
        if n == 1:
            return A[0][0]
        det = 0
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for row in A[1:]]
            det += (-1) ** j * A[0][j] * determinant(submatrix)
        return det
    
    def noncommutative_fourier_coefficient(M, k):
        n = len(M)
        if n <= 3:
            return None
        identity = [[int(i == j) for j in range(n)] for i in range(n)]
        G = []
        for perm in itertools.permutations(range(n)):
            P = [[0] * n for _ in range(n)]
            for i, j in enumerate(perm):
                P[i][j] = 1
            G.append(P)
        
        def young_tableaux_decomposition(G):
            # Placeholder for actual implementation
            return [G]
        
        coefficients = []
        for g in G:
            H = matrix_multiplication(g, M)
            H = gaussian_elimination(H)
            det_H = determinant(H)
            coefficients.append(det_H)
        
        lambda_k = sum(coefficients) / len(coefficients)
        return abs(lambda_k)
    
    def communication_complexity_lower_bound(M):
        n = len(M)
        ones_count = sum(sum(row) for row in M)
        lower_bound = math.ceil(math.log2(ones_count))
        return lower_bound
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        M = generate_disjointness_instance(n)
        lambda_k = noncommutative_fourier_coefficient(M, k=0)  # Assuming k=0 for simplicity
        if lambda_k is None:
            return {
                "metric_name": "noncommutative_fourier_coefficient",
                "metric_value": None,
                "instances_tested": len(n_values),
                "conjecture_holds": False,
                "counterexample": "mapping_undefined"
            }
        
        L = communication_complexity_lower_bound(M)
        if L == 0:
            continue
        
        results.append({
            "n": n,
            "lambda_k": lambda_k,
            "L": L
        })
    
    if not results:
        return {
            "metric_name": "noncommutative_fourier_coefficient",
            "metric_value": None,
            "instances_tested": len(n_values),
            "conjecture_holds": False,
            "counterexample": "no_valid_instances"
        }
    
    lambda_k_avg = sum(result["lambda_k"] for result in results) / len(results)
    L_avg = sum(result["L"] for result in results) / len(results)
    c = lambda_k_avg / L_avg
    
    conjecture_holds = all(abs(result["lambda_k"]) >= c / result["L"] for result in results if abs(result["lambda_k"]) > 0)
    
    return {
        "metric_name": "noncommutative_fourier_coefficient",
        "metric_value": lambda_k_avg,
        "instances_tested": len(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else "c={} L={}".format(c, L_avg)
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print("TRIAL: {}".format(trial_result))
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_value = sum(result["metric_value"] for result in results) / len(results)
        support_fraction = 1.0
        print("RESULT: SUPPORTED mean={} std=0 support_fraction={}".format(mean_value, 0, support_fraction))
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        counterexample = results[seeds.index(first_failing_seed)]["counterexample"]
        print("RESULT: FALSIFIED counterexample={} first_failing_seed={}".format(counterexample, first_failing_seed))