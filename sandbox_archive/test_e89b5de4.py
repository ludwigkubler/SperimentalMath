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
    
    def output_complexity(f):
        n = int(math.log2(len(f)))
        count = sum(1 for i in range(2**n) if f[i] != f[0])
        return count
    
    def matrix_multiply(A, B):
        m, k = len(A), len(B[0])
        n = len(B)
        C = [[0] * k for _ in range(m)]
        for i in range(m):
            for j in range(k):
                for l in range(n):
                    C[i][j] += A[i][l] * B[l][j]
        return C
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        rank = 0
        for i in range(m):
            if i + rank >= m:
                break
            max_row = i
            for j in range(i+1, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            if A[i][i] == 0:
                continue
            rank += 1
            for j in range(m):
                if i != j:
                    factor = -A[j][i] / A[i][i]
                    for k in range(n):
                        A[j][k] += factor * A[i][k]
        return rank
    
    def minimal_rank(f):
        n = int(math.log2(len(f)))
        F_2_n = [[0]*n for _ in range(1<<n)]
        for i in range(1<<n):
            x = [i >> j & 1 for j in range(n)]
            F_2_n[i] = f[x]
        
        A = []
        for i in range(1<<n):
            row = [F_2_n[i][j] ^ F_2_n[0][j] for j in range(n)]
            A.append(row)
        
        return gaussian_elimination(A)
    
    def find_homomorphism(f, rank):
        n = int(math.log2(len(f)))
        F_2_n = [[0]*n for _ in range(1<<n)]
        for i in range(1<<n):
            x = [i >> j & 1 for j in range(n)]
            F_2_n[i] = f[x]
        
        A = []
        for i in range(1<<n):
            row = [F_2_n[i][j] ^ F_2_n[0][j] for j in range(n)]
            A.append(row)
        
        B = [[random.choice([0, 1]) for _ in range(n)] for _ in range(rank)]
        C = matrix_multiply(A, B)
        
        if all(C[i][i] == 0 for i in range(rank)):
            return None
        
        return B
    
    n = random.randint(5, 40)
    f = generate_boolean_function(n)
    C_f = output_complexity(f)
    
    rank = minimal_rank(f)
    homomorphism = find_homomorphism(f, rank) if C_f % 2 == 0 else None
    
    conjecture_holds = rank <= 2**C_f and (homomorphism is not None or C_f % 2 != 0)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(res["metric_value"] for res in results) / len(results)
    std_rank = math.sqrt(sum((res["metric_value"] - mean_rank)**2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] for res in results):
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")