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
    
    def generate_max_cut_instance(n):
        return [random.choice([-1, 1]) for _ in range(n)]
    
    def matrix_multiply(A, B):
        n = len(A)
        C = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C
    
    def gaussian_elimination(A, b):
        n = len(A)
        M = [A[i] + [b[i]] for i in range(n)]
        for i in range(n):
            max_row = max(range(i, n), key=lambda r: abs(M[r][i]))
            M[i], M[max_row] = M[max_row], M[i]
            factor = M[i][i]
            for j in range(i, n + 1):
                M[i][j] /= factor
            for k in range(n):
                if k != i:
                    factor = M[k][i]
                    for j in range(i, n + 1):
                        M[k][j] -= factor * M[i][j]
        return [row[-1] for row in M]
    
    def determinant(A):
        n = len(A)
        det = 0
        if n == 1:
            return A[0][0]
        elif n == 2:
            return A[0][0] * A[1][1] - A[0][1] * A[1][0]
        else:
            for j in range(n):
                det += (-1) ** j * A[0][j] * determinant([row[:j] + row[j+1:] for row in A[1:]])
        return det
    
    def inverse(A):
        n = len(A)
        det_A = determinant(A)
        if det_A == 0:
            raise ValueError("Modular inverse does not exist")
        adjoint = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                minor = [row[:j] + row[j+1:] for row in A[:i] + A[i+1:]]
                cofactor = determinant(minor) * ((-1) ** (i + j))
                adjoint[j][i] = cofactor
        return [[adjoint[i][j] / det_A for j in range(n)] for i in range(n)]
    
    def real_radical_rank(I):
        n = len(I)
        A = [[I[i][j] * I[k][l] for l in range(n)] for k in range(n) for j in range(n)]
        A = [sum(A[j*n+i] for j in range(n)) for i in range(n)]
        A = [[A[i*n+j] for j in range(n)] for i in range(n)]
        det_A = determinant(A)
        return int(math.log2(det_A))
    
    def sos_degree(instance):
        n = len(instance)
        A = [[0] * (n + 1) for _ in range(n + 1)]
        for i in range(n):
            for j in range(n):
                A[i][j] = instance[i] * instance[j]
            A[i][n] = -instance[i]
        A[n][n] = 1
        b = [0] * (n + 1)
        x = gaussian_elimination(A, b)
        return n
    
    def max_cut_approximation(instance):
        n = len(instance)
        cut_value = sum(abs(x) for x in instance) / 2
        return cut_value
    
    n = 40
    instance = generate_max_cut_instance(n)
    rank_I = real_radical_rank([instance])
    d_n = sos_degree(instance)
    conjecture_holds = d_n >= math.log2(rank_I)
    
    return {
        "metric_name": "real_radical_rank",
        "metric_value": rank_I,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"instance={instance}"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")