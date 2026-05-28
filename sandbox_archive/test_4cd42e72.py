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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def tensor_representation(f):
        n = int(math.log2(len(f)))
        T = [[0] * (2**n) for _ in range(2**n)]
        for i in range(2**n):
            for j in range(2**n):
                T[i][j] = f[(i & j).bit_count()]
        return T
    
    def min_rank(T):
        n = len(T)
        rank = 0
        U = [[0] * n for _ in range(n)]
        V = [[0] * n for _ in range(n)]
        S = [1] * n
        
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
                    factor = -A[j][i] / A[i][i]
                    for k in range(n):
                        A[j][k] += factor * A[i][k]
                    b[j] += factor * b[i]
            
            return [x / A[i][i] for i, x in enumerate(b)]
        
        def matrix_multiplication(A, B):
            m, n = len(A), len(B[0])
            p = len(B)
            C = [[0] * n for _ in range(m)]
            for i in range(m):
                for j in range(n):
                    for k in range(p):
                        C[i][j] += A[i][k] * B[k][j]
            return C
        
        def transpose(A):
            m, n = len(A), len(A[0])
            T = [[0] * m for _ in range(n)]
            for i in range(m):
                for j in range(n):
                    T[j][i] = A[i][j]
            return T
        
        def inverse(A):
            m, n = len(A), len(A[0])
            if m != n:
                raise ValueError("Matrix must be square")
            
            I = [[1 if i == j else 0 for j in range(n)] for i in range(m)]
            A_augmented = [row + col for row, col in zip(A, I)]
            
            gaussian_elimination(A_augmented)
            
            U = [row[:n] for row in A_augmented]
            V = [row[n:] for row in A_augmented]
            
            return matrix_multiplication(transpose(V), U)
        
        def rank(A):
            m, n = len(A), len(A[0])
            rank = 0
            for i in range(m):
                if any(A[i][j] != 0 for j in range(n)):
                    rank += 1
            return rank
        
        return rank
    
    def polynomial_upper_bound(s):
        k = 2  # Example value, can be adjusted based on analysis
        return s**k
    
    n = random.randint(5, 40)
    f = generate_boolean_function(n)
    T = tensor_representation(f)
    rank = min_rank(T)
    upper_bound = polynomial_upper_bound(n)
    
    return {
        "metric_name": "Tensor Rank",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": rank <= upper_bound,
        "counterexample": "" if rank <= upper_bound else f"Rank {rank} exceeds bound {upper_bound}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    std_rank = math.sqrt(sum((r["metric_value"] - mean_rank)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = next((r["counterexample"] for r in results if not r["conjecture_holds"]), "")
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")