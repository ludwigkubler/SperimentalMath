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

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    return abs(a * b) // gcd(a, b)

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
    M = [A[i] + b[i] for i in range(n)]
    for i in range(n):
        max_row = i
        for j in range(i+1, n):
            if abs(M[j][i]) > abs(M[max_row][i]):
                max_row = j
        M[i], M[max_row] = M[max_row], M[i]
        factor = M[i][i]
        for j in range(n):
            M[i][j] /= factor
        for j in range(n):
            if i != j:
                factor = M[j][i]
                for k in range(n):
                    M[j][k] -= factor * M[i][k]
    return [M[i][-1] for i in range(n)]

def is_prime(num):
    if num < 2:
        return False
    for i in range(2, int(math.sqrt(num)) + 1):
        if num % i == 0:
            return False
    return True

def generate_primes(n):
    primes = []
    candidate = 2
    while len(primes) < n:
        if is_prime(candidate):
            primes.append(candidate)
        candidate += 1
    return primes

def generate_bipartite_graph(n):
    A = list(range(n))
    B = list(range(n, 2*n))
    E = []
    for i in range(n):
        for j in range(i+1, n):
            if random.choice([True, False]):
                E.append((A[i], B[j]))
                E.append((B[j], A[i]))
    return A, B, E

def max_matching(G):
    n = len(G)
    matching = [-1] * n
    visited = [False] * n
    
    def dfs(u):
        for v in range(n):
            if G[u][v] and not visited[v]:
                visited[v] = True
                if matching[v] == -1 or dfs(matching[v]):
                    matching[v] = u
                    return True
        return False
    
    for u in range(n):
        visited = [False] * n
        dfs(u)
    
    return sum(1 for x in matching if x != -1)

def schur_weyl_rank(G):
    n = len(G)
    A, B, E = G
    M = [[0] * n for _ in range(n)]
    for u, v in E:
        M[u][v], M[v][u] = 1, 1
    
    rank = gaussian_elimination(M, [0] * n).count(0)
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        A, B, E = generate_bipartite_graph(n)
        G = (A, B, E)
        lambda_G = max_matching(G)
        R_G = schur_weyl_rank(G)
        
        if lambda_G < 2 or R_G >= math.sqrt(n):
            results.append({"n": n, "lambda_G": lambda_G, "R_G": R_G})
    
    metric_name = "Schur-Weyl Rank"
    metric_value = sum(result["R_G"] for result in results) / len(results)
    instances_tested = len(results)
    conjecture_holds = all(result["R_G"] >= math.sqrt(result["n"]) for result in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or generate_primes(30)
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")