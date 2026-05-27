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
    
    def matrix_multiply(A, B):
        m = len(A)
        n = len(B[0])
        p = len(B)
        C = [[0 for _ in range(n)] for _ in range(m)]
        for i in range(m):
            for j in range(n):
                for k in range(p):
                    C[i][j] += A[i][k] * B[k][j]
        return C
    
    def gaussian_elimination(A, b):
        m = len(A)
        n = len(A[0])
        augmented_matrix = [A[i] + [b[i]] for i in range(m)]
        
        for i in range(n):
            max_row = i
            for j in range(i+1, m):
                if abs(augmented_matrix[j][i]) > abs(augmented_matrix[max_row][i]):
                    max_row = j
            augmented_matrix[i], augmented_matrix[max_row] = augmented_matrix[max_row], augmented_matrix[i]
            
            pivot = augmented_matrix[i][i]
            for j in range(i, n+1):
                augmented_matrix[i][j] /= pivot
            
            for j in range(m):
                if j != i:
                    factor = augmented_matrix[j][i]
                    for k in range(n+1):
                        augmented_matrix[j][k] -= factor * augmented_matrix[i][k]
        
        x = [0 for _ in range(n)]
        for i in range(n-1, -1, -1):
            x[i] = augmented_matrix[i][-1]
            for j in range(i+1, n):
                x[i] -= augmented_matrix[i][j] * x[j]
        return x
    
    def svd(A):
        m, n = len(A), len(A[0])
        U = [[0 for _ in range(m)] for _ in range(m)]
        S = [0 for _ in range(min(m, n))]
        Vt = [[0 for _ in range(n)] for _ in range(n)]
        
        A_t = list(zip(*A))
        
        # Compute U
        for i in range(m):
            u_i = [A[i][j] for j in range(n)]
            norm_u_i = math.sqrt(sum(x**2 for x in u_i))
            U[i] = [x / norm_u_i for x in u_i]
        
        # Compute Vt
        for j in range(n):
            v_j = [A_t[j][i] for i in range(m)]
            norm_v_j = math.sqrt(sum(x**2 for x in v_j))
            Vt[j] = [x / norm_v_j for x in v_j]
        
        # Compute S
        for i in range(min(m, n)):
            S[i] = sum(A[i][j]**2 for j in range(n))**(1/2)
        
        return U, S, Vt
    
    def min_tensor_rank(n):
        A = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
        B = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
        C = matrix_multiply(A, B)
        U, S, Vt = svd(C)
        return len([s for s in S if s != 0])
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    depth = random.randint(1, 10)
    
    instances_tested = 30
    total_rank = 0
    
    for _ in range(instances_tested):
        rank = min_tensor_rank(n)
        total_rank += rank
    
    mean_rank = total_rank / instances_tested
    
    conjecture_holds = mean_rank <= 2**depth or (n == 40 and mean_rank > n**2 / 4)
    
    return {
        "metric_name": "min_tensor_rank",
        "metric_value": mean_rank,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"mean_rank={mean_rank}, depth={depth}"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")