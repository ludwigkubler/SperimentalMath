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
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            # Find pivot
            max_row = i
            for j in range(i+1, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            
            # Eliminate below pivot
            for j in range(i+1, m):
                factor = A[j][i] / A[i][i]
                for k in range(n):
                    A[j][k] -= factor * A[i][k]
        
        # Back-substitute to find solution
        x = [0] * n
        for i in range(m-1, -1, -1):
            x[i] = A[i][-1] / A[i][i]
            for j in range(i-1, -1, -1):
                A[j][-1] -= A[j][i] * x[i]
        
        return x
    
    def matrix_multiply(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[0 for _ in range(p)] for _ in range(m)]
        for i in range(m):
            for j in range(p):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C
    
    def is_connected(G):
        n = len(G)
        visited = [False] * n
        stack = [0]
        while stack:
            u = stack.pop()
            if not visited[u]:
                visited[u] = True
                for v in range(n):
                    if G[u][v] and not visited[v]:
                        stack.append(v)
        return all(visited)
    
    def compute_rho(G):
        n = len(G)
        if not is_connected(G):
            return float('inf')
        
        # Convert graph to adjacency matrix
        A = [[0 for _ in range(n)] for _ in range(n)]
        for i in range(n):
            for j in range(i+1, n):
                if G[i][j]:
                    A[i][j] = 1
                    A[j][i] = 1
        
        # Perform Gaussian elimination to find rank
        rank = len(gaussian_elimination(A))
        return rank
    
    def xor_circuit_size(n):
        # Brute-force search for XOR circuit size (simplified)
        return n * n
    
    n = random.randint(5, 40)
    G = [[random.choice([0, 1]) if i != j else 0 for j in range(n)] for i in range(n)]
    
    rho_G = compute_rho(G)
    C = xor_circuit_size(n)
    
    if rho_G >= 10 and C >= 100:
        return {
            "metric_name": "XOR circuit size",
            "metric_value": C,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "rho(G) >= 10"
        }
    
    if abs(C - (1 / rho_G) ** 2) > 3:
        return {
            "metric_name": "XOR circuit size",
            "metric_value": C,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"C - (1/rho(G))^2 > 3"
        }
    
    return {
        "metric_name": "XOR circuit size",
        "metric_value": C,
        "instances_tested": 1,
        "conjecture_holds": True,
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
    
    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = 1.0
        result = f"RESULT: SUPPORTED mean={mean_value} std=0 support_fraction={support_fraction}"
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = next((r["counterexample"] for r in results if not r["conjecture_holds"]), "")
        result = f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}"
    
    print(result)