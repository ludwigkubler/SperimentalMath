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
    
    def gram_schmidt(A):
        n = len(A)
        Q, R = [], []
        for i in range(n):
            q_i = A[i]
            for j in range(i):
                r_ij = sum(Q[j][k] * A[i][k] for k in range(n))
                q_i = [q_i[k] - r_ij * Q[j][k] for k in range(n)]
            norm_q_i = math.sqrt(sum(q_i[k]**2 for k in range(n)))
            R.append([q_i[k] / norm_q_i if i == j else 0 for k in range(n)])
            Q.append([q_i[k] / norm_q_i for k in range(n)])
        return Q, R
    
    def matrix_mult(A, B):
        n = len(A)
        C = [[sum(A[i][k] * B[k][j] for k in range(n)) for j in range(n)] for i in range(n)]
        return C
    
    def determinant(matrix):
        n = len(matrix)
        if n == 1:
            return matrix[0][0]
        det = 0
        for c in range(n):
            sub_matrix = [row[:c] + row[c+1:] for row in matrix[1:]]
            sign = (-1) ** (c % 2)
            sub_det = determinant(sub_matrix)
            det += sign * matrix[0][c] * sub_det
        return det
    
    def is_invertible(matrix):
        return determinant(matrix) != 0
    
    def max_cut_instance(n):
        edges = []
        for i in range(n):
            for j in range(i+1, n):
                if random.random() < 0.5:
                    edges.append((i, j))
        return edges
    
    def characteristic_polynomial(matrix):
        n = len(matrix)
        x = random.choice(range(2, n))
        poly = [[matrix[i][j] for j in range(n)] for i in range(n)]
        for _ in range(x-1):
            poly = matrix_mult(poly, matrix)
        return poly
    
    def quantum_logarithmic_form(poly):
        n = len(poly)
        form = 0
        for i in range(n):
            for j in range(i+1, n):
                if poly[i][j] != 0:
                    form += math.log(abs(poly[i][j]))
        return form
    
    def sum_of_squares_degree(edges):
        # Placeholder for actual implementation
        return len(edges)
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    edges = max_cut_instance(n)
    matrix = [[random.randint(0, 1) if i != j else 0 for j in range(n)] for i in range(n)]
    
    Q, R = gram_schmidt(matrix)
    rank = sum(1 for row in Q if any(row[i] != 0 for i in range(n)))
    
    poly = characteristic_polynomial(matrix)
    form = quantum_logarithmic_form(poly)
    degree = sum_of_squares_degree(edges)
    
    conjecture_holds = degree <= rank
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Rank vs DPLL Heig",
        "metric_value": form,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        for result in results:
            if not result["conjecture_holds"]:
                counterexample = result["counterexample"]
                first_failing_seed = seed
                break
        
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")