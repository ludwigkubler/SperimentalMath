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
        return math.log2(x) if x > 0 else float('inf')
    
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
    
    def matrix_multiply(A, B):
        m, k, n = len(A), len(B), len(B[0])
        C = [[0] * n for _ in range(m)]
        for i in range(m):
            for j in range(n):
                for l in range(k):
                    C[i][j] += A[i][l] * B[l][j]
        return C
    
    def determinant(A):
        if len(A) == 1:
            return A[0][0]
        det = 0
        for c in range(len(A)):
            det += ((-1)**c) * A[0][c] * determinant([row[:c] + row[c+1:] for row in A[1:]])
        return det
    
    def is_invertible(matrix):
        return determinant(matrix) != 0
    
    def tensor_product(V, W):
        m, n = len(V), len(W)
        result = [[0] * (n * m) for _ in range(m)]
        for i in range(m):
            for j in range(n):
                for k in range(m):
                    result[i][j*m + k] = V[i][k] * W[j][k]
        return result
    
    def tropical_vector_add(v1, v2):
        return [max(a, b) for a, b in zip(v1, v2)]
    
    def tropical_vector_mul(v, a):
        return [a + x for x in v]
    
    def tropical_vector_length(v):
        return max(v)
    
    n = random.randint(5, 40)
    s = random.randint(1, 40)
    C = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    b = [random.choice([0, 1]) for _ in range(n)]
    
    x = gaussian_elimination(C, b)
    output_vector = tropical_vector_mul(x, n)
    
    d = int(log2(s))
    V = [[random.uniform(-1, 1) for _ in range(d)] for _ in range(d)]
    T = [[0] * d for _ in range(d)]
    W = [[0] * d for _ in range(d)]
    T[0][0] = 1
    
    if is_invertible(V):
        V_inv = gaussian_elimination([[V[i][j], float('inf') if i != j else -1] for i in range(d)], [float('-inf')] * d)
        W = matrix_multiply(V_inv, tensor_product(T, V))
    
    dimension = tropical_vector_length(output_vector)
    conjecture_holds = dimension >= log2(s) and all(w == 0 or w == 1 for row in W for w in row)
    counterexample = "Output vector length {} does not match dimension {}".format(dimension, d) if not conjecture_holds else ""
    
    return {
        "metric_name": "dimension",
        "metric_value": dimension,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        results.append(result)
        print("TRIAL:", result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print("RESULT: SUPPORTED mean={} std={} support_fraction={}".format(mean_value, std_value, support_fraction))
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print("RESULT: FALSIFIED counterexample='{}' first_failing_seed={}".format(results[first_failing_seed]["counterexample"], first_failing_seed))
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")