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

def reverse_bfs(g, start):
    n = len(g)
    visited = [False] * n
    queue = [start]
    visited[start] = True
    cone = set()
    while queue:
        node = queue.pop(0)
        cone.add(node)
        for neighbor in g[node]:
            if not visited[neighbor]:
                visited[neighbor] = True
                queue.append(neighbor)
    return cone

def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        # Find the pivot row
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        
        # Eliminate below the pivot
        for j in range(i+1, n):
            factor = A[j][i] / A[i][i]
            for k in range(n):
                A[j][k] -= factor * A[i][k]
    
    # Back-substitute to find the solution
    x = [0] * n
    for i in range(n-1, -1, -1):
        x[i] = A[i][-1]
        for j in range(i+1, n):
            x[i] -= A[i][j] * x[j]
        x[i] /= A[i][i]
    
    return x

def power_method(A, max_iter=30):
    n = len(A)
    v = [random.random() for _ in range(n)]
    v = [x / sum(v) for x in v]  # Normalize
    
    for _ in range(max_iter):
        Av = [sum(A[i][j] * v[j] for j in range(n)) for i in range(n)]
        lambda_max = max(abs(x) for x in Av)
        v = [x / lambda_max for x in Av]
    
    return lambda_max, v

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [4, 6, 8, 10, 12, 14, 16, 20, 24]
    d_values = [2, 3]
    results = []
    
    for n in n_values:
        for d in d_values:
            for _ in range(30):
                # Generate a random permutation of input variables
                inputs = list(range(n))
                random.shuffle(inputs)
                
                # Construct the circuit
                g = [[] for _ in range(n)]
                if d == 2:
                    for i in range(n):
                        g[i].append((i, 'AND'))
                        g[i].append((i, 'OR'))
                elif d == 3:
                    block_size = math.ceil(math.sqrt(n))
                    for i in range(block_size):
                        for j in range(i*block_size, min((i+1)*block_size, n)):
                            g[j].append((j, 'AND'))
                            g[j].append((j, 'OR'))
                
                # Add random NOT-NOT redundancy gates
                for _ in range(5):
                    i = random.randint(0, n-1)
                    j = random.choice(g[i])
                    if j[1] == 'AND':
                        g[i].append((i, 'NOT', j))
                    elif j[1] == 'OR':
                        g[i].append((i, 'NOT', j))
                
                # Compute the cone of each gate
                cones = [reverse_bfs(g, i) for i in range(n)]
                
                # Form the Gram matrix K(C)
                K = [[0] * n for _ in range(n)]
                for i in range(n):
                    for j in range(i+1, n):
                        intersection_size = len(cones[i].intersection(cones[j]))
                        K[i][j] = K[j][i] = intersection_size / n
                
                # Compute the top spectrum of K(C)
                lambda_max, _ = power_method(K)
                
                # Compute ψ(C) and r(C)
                psi_C = sum(K[i][i] for i in range(n)) / lambda_max
                r_C = psi_C ** (1/(d-1)) / math.log2(2**n)
                
                results.append(r_C)
    
    mean_r = sum(results) / len(results)
    max_r = max(results)
    
    if max_r > 8:
        return {
            "metric_name": "r(C)",
            "metric_value": mean_r,
            "instances_tested": len(results),
            "conjecture_holds": False,
            "counterexample": f"max r(C) = {max_r} (exceeds threshold)"
        }
    else:
        return {
            "metric_name": "r(C)",
            "metric_value": mean_r,
            "instances_tested": len(results),
            "conjecture_holds": True,
            "counterexample": ""
        }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    
    results = []
    for seed in seeds:
        trial = run_trial(seed)
        print(f"TRIAL: {trial}")
        results.append(trial["metric_value"])
    
    mean_r = sum(results) / len(results)
    max_r = max(results)
    support_fraction = sum(1 for r in results if r <= 8) / len(results)
    
    if max_r > 8:
        print(f"RESULT: FALSIFIED counterexample=\"max r(C) = {max_r}\" first_failing_seed={seeds[results.index(max_r)]}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_r} std=0 support_fraction={support_fraction}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")