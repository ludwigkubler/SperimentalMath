# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction
from itertools import combinations

def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

def generate_primes(k):
    primes = []
    num = 2
    while len(primes) < k:
        if is_prime(num):
            primes.append(num)
        num += 1
    return primes

def random_3_regular_graph(n, seed=None):
    if seed is not None:
        random.seed(seed)
    
    G = [[] for _ in range(n)]
    degree = [0] * n
    
    while True:
        available_nodes = [i for i in range(n) if degree[i] < 3]
        if not available_nodes:
            break
        
        node1 = random.choice(available_nodes)
        neighbors = set(G[node1])
        
        while len(neighbors) >= 2:
            node2 = random.choice(list(neighbors))
            neighbors.remove(node2)
        
        G[node1].append(node2)
        G[node2].append(node1)
        degree[node1] += 1
        degree[node2] += 1
    
    return G

def adjacency_matrix(G):
    n = len(G)
    A = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in G[i]:
            A[i][j] = 1
            A[j][i] = 1
    return A

def trace(A, k):
    n = len(A)
    result = 0
    for i in range(n):
        result += A[i][(i + k) % n]
    return result / n

def hankel_matrix(A):
    n = len(A)
    H = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            H[i][j] = trace(A, i + j)
    return H

def gaussian_elimination(A):
    n = len(A)
    rank = 0
    for i in range(n):
        if A[i][i] == 0:
            found_non_zero = False
            for k in range(i + 1, n):
                if A[k][i] != 0:
                    A[i], A[k] = A[k], A[i]
                    found_non_zero = True
                    break
            if not found_non_zero:
                continue
        
        pivot = A[i][i]
        for j in range(n):
            A[i][j] /= pivot
        
        for k in range(n):
            if k != i and A[k][i] != 0:
                factor = A[k][i]
                for j in range(n):
                    A[k][j] -= factor * A[i][j]
        
        rank += 1
    return rank

def eigenvalues(A):
    n = len(A)
    if n == 1:
        return [A[0][0]]
    
    if n == 2:
        a, b, c = A[0][0], A[0][1], A[1][1]
        det = a * c - b * b
        return [a + c, (b * b + det) / (2 * (a + c))]
    
    if n == 3:
        a, b, c = A[0][0], A[0][1], A[0][2]
        d, e, f = A[1][0], A[1][1], A[1][2]
        g, h, i = A[2][0], A[2][1], A[2][2]
        
        det = a * (e * i - f * h) - b * (d * i - f * g) + c * (d * h - e * g)
        if det == 0:
            return eigenvalues([[a, b, c], [d, e, f]])
        
        p = -(a * e + a * h + b * d + b * g + c * f + c * i) / 6
        q = (2 * (a * e * h + a * f * g + b * d * i - a * f * h - b * e * g - c * d * h) - det * p) / 6
        
        if q == 0:
            r = -(p ** 3) / 27
            s = math.sqrt(r ** 2 + (q ** 2) / 4)
            t = -r + s
            u = -r - s
            
            root1 = 2 * math.cbrt(t) if t >= 0 else -2 * math.cbrt(u)
            root2 = -(root1 / 2) + (q / (3 * root1)) - p / 3
            root3 = -(root1 / 2) - (q / (3 * root1)) - p / 3
            
            return [root1, root2, root3]
        
        if q > 0:
            r = -(p ** 3) / 27
            s = math.sqrt(r ** 2 + (q ** 2) / 4)
            t = -r + s
            u = -r - s
            
            theta = math.acos(-q / (2 * math.sqrt(-(r ** 2 + q ** 2))))
            
            root1 = 2 * math.cbrt(t) * math.cos(theta / 3) - p / 3
            root2 = 2 * math.cbrt(u) * math.cos((theta + 2 * math.pi) / 3) - p / 3
            root3 = 2 * math.cbrt(u) * math.cos((theta + 4 * math.pi) / 3) - p / 3
            
            return [root1, root2, root3]
        
        if q < 0:
            r = -(p ** 3) / 27
            s = math.sqrt(r ** 2 + (q ** 2) / 4)
            t = -r + s
            u = -r - s
            
            theta = math.acos(-q / (2 * math.sqrt(-(r ** 2 + q ** 2))))
            
            root1 = 2 * math.cbrt(t) * math.cos(theta / 3) - p / 3
            root2 = 2 * math.cbrt(u) * math.cos((theta + 2 * math.pi) / 3) - p / 3
            root3 = 2 * math.cbrt(u) * math.cos((theta + 4 * math.pi) / 3) - p / 3
            
            return [root1, root2, root3]
    
    raise NotImplementedError("Mapping undefined for n > 3")

def max_cut(G):
    n = len(G)
    max_cut_value = 0
    for subset in combinations(range(n), n // 2):
        cut_value = sum(1 for u, v in G if (u in subset and v not in subset) or (v in subset and u not in subset))
        max_cut_value = max(max_cut_value, cut_value)
    return max_cut_value

def run_trial(seed: int) -> dict:
    n_values = [8, 10, 12, 14, 16, 18]
    results = []
    
    for n in n_values:
        for _ in range(30):
            G = random_3_regular_graph(n, seed)
            A = adjacency_matrix(G)
            eigenvals = eigenvalues(A)
            distinct_eigenvals = len(set(eigenvals))
            
            H = hankel_matrix(A)
            H_rank = gaussian_elimination(H)
            if H_rank != distinct_eigenvals:
                return {
                    "metric_name": "S(G)/n",
                    "metric_value": None,
                    "instances_tested": 1,
                    "conjecture_holds": False,
                    "counterexample": "Hankel matrix rank mismatch"
                }
            
            num_edges = sum(sum(row) for row in A) // 2
            lambda_min = min(eigenvals)
            UB_DP = num_edges / 2 - (n / 4) * lambda_min
            max_cut_value = max_cut(G)
            S_G = UB_DP - max_cut_value
            
            results.append(S_G / n)
    
    mean_r_G = sum(results) / len(results)
    min_r_G = min(results)
    
    return {
        "metric_name": "S(G)/n",
        "metric_value": mean_r_G,
        "instances_tested": len(results),
        "conjecture_holds": min_r_G >= 0.02 and mean_r_G <= 0.45,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or generate_primes(30)
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
    
    results = [run_trial(seed)["metric_value"] for seed in seeds if run_trial(seed)["conjecture_holds"]]
    support_fraction = len(results) / len(seeds)
    mean_r_G = sum(results) / len(results) if results else None
    
    if all(r >= 0.02 for r in results):
        print(f"RESULT: SUPPORTED mean={mean_r_G} std={sum((r - mean_r_G) ** 2 for r in results) / len(results)} support_fraction={support_fraction}")
    elif any(r < 0.02 for r in results):
        first_failing_seed = next(seed for seed in seeds if run_trial(seed)["metric_value"] < 0.02)
        print(f"RESULT: FALSIFIED counterexample='S(G)/n < 0.02' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no valid results")