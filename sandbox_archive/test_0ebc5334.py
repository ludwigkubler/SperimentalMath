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
        
        for j in range(n):
            max_row = j
            for i in range(j+1, m):
                if abs(augmented_matrix[i][j]) > abs(augmented_matrix[max_row][j]):
                    max_row = i
            
            augmented_matrix[j], augmented_matrix[max_row] = augmented_matrix[max_row], augmented_matrix[j]
            
            pivot = augmented_matrix[j][j]
            for k in range(n+1):
                augmented_matrix[j][k] /= pivot
            
            for i in range(m):
                if i != j:
                    factor = augmented_matrix[i][j]
                    for k in range(n+1):
                        augmented_matrix[i][k] -= factor * augmented_matrix[j][k]
        
        return [row[-1] for row in augmented_matrix]

    def slice_rank(T):
        m, n, _ = len(T), len(T[0]), len(T[0][0])
        rank = 0
        while True:
            max_support = 0
            axis = -1
            v = [0] * n
            
            for i in range(3):
                support = 0
                if i == 0:
                    for j in range(n):
                        for k in range(m):
                            if sum(T[k][j]) % 2 != 0:
                                support += 1
                                v[j] += 1
                elif i == 1:
                    for k in range(m):
                        for j in range(n):
                            if sum(T[k][j]) % 2 != 0:
                                support += 1
                                v[k] += 1
                else:
                    for j in range(n):
                        for k in range(m):
                            if T[k][j][k] % 2 != 0:
                                support += 1
                                v[j] += 1
                
                if support > max_support:
                    max_support = support
                    axis = i
            
            if max_support == 0:
                break
            
            rank += 1
            for j in range(n):
                T[j][j] -= v[j]
        
        return rank
    
    def generate_read_twice_bp(n, w):
        V = [i for i in range(2*n)]
        edges = []
        for _ in range(w):
            for i in range(n):
                u = random.choice(V)
                v = random.choice(V)
                while v == u:
                    v = random.choice(V)
                edges.append((u, v))
                V.remove(u)
                V.remove(v)
        
        T_P = [[[0 for _ in range(n)] for _ in range(2*n)] for _ in range(2*n)]
        for u, v in edges:
            for j in range(n):
                if random.choice([True, False]):
                    T_P[u][v][j] += 1
                if random.choice([True, False]):
                    T_P[v][u][j] += 1
        
        return T_P
    
    def generate_ip2_bp(n):
        V = [i for i in range(2*n)]
        edges = []
        for i in range(n):
            u = random.choice(V)
            v = random.choice(V)
            while v == u:
                v = random.choice(V)
            edges.append((u, v))
            V.remove(u)
            V.remove(v)
        
        T_P = [[[0 for _ in range(n)] for _ in range(2*n)] for _ in range(2*n)]
        for u, v in edges:
            for j in range(n):
                if random.choice([True, False]):
                    T_P[u][v][j] += 1
                if random.choice([True, False]):
                    T_P[v][u][j] += 1
        
        return T_P
    
    def partition_rank(T):
        m, n, _ = len(T), len(T[0]), len(T[0][0])
        rank = 0
        while True:
            max_support = 0
            axis = -1
            v = [0] * n
            
            for i in range(3):
                support = 0
                if i == 0:
                    for j in range(n):
                        for k in range(m):
                            if sum(T[k][j]) % 2 != 0:
                                support += 1
                                v[j] += 1
                elif i == 1:
                    for k in range(m):
                        for j in range(n):
                            if sum(T[k][j]) % 2 != 0:
                                support += 1
                                v[k] += 1
                else:
                    for j in range(n):
                        for k in range(m):
                            if T[k][j][k] % 2 != 0:
                                support += 1
                                v[j] += 1
                
                if support > max_support:
                    max_support = support
                    axis = i
            
            if max_support == 0:
                break
            
            rank += 1
            for j in range(n):
                T[j][j] -= v[j]
        
        return rank
    
    n_values = [6, 8, 10, 12, 14, 16, 18, 20]
    w_values = [2, 3, 4]
    results = []
    
    for n in n_values:
        for _ in range(30):
            T_P = generate_read_twice_bp(n, random.choice(w_values))
            rank = slice_rank(T_P)
            if rank > 6 * math.ceil(math.log2(2*n)):
                return {
                    "metric_name": "slice_rank",
                    "metric_value": rank,
                    "instances_tested": 1,
                    "conjecture_holds": False,
                    "counterexample": f"Read-twice BP with n={n} and rank {rank}"
                }
            results.append(rank)
    
    for n in [4, 6, 8, 10, 12]:
        T_P = generate_ip2_bp(n)
        rank = partition_rank(T_P)
        if rank < n // 8:
            return {
                "metric_name": "partition_rank",
                "metric_value": rank,
                "instances_tested": 1,
                "conjecture_holds": False,
                "counterexample": f"IP_2 BP with n={n} and rank {rank}"
            }
        results.append(rank)
    
    return {
        "metric_name": "slice_rank",
        "metric_value": sum(results) / len(results),
        "instances_tested": len(results),
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result["metric_value"])
    
    mean = sum(results) / len(results)
    std = (sum((x - mean)**2 for x in results) / len(results))**0.5
    support_fraction = sum(1 for r in results if r <= 6 * math.ceil(math.log2(2*n_values[0]))) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    elif any(r < n // 8 for n in [4, 6, 8, 10, 12]):
        first_failing_seed = seeds[results.index(next(r for r in results if r < n // 8))]
        print(f"RESULT: FALSIFIED counterexample=\"IP_2 BP\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")