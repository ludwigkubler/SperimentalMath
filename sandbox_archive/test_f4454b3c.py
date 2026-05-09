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

def gaussian_elimination(A):
    m, n = len(A), len(A[0])
    for i in range(m):
        max_row = i
        for j in range(i+1, m):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        for j in range(i+1, m):
            factor = A[j][i] / A[i][i]
            for k in range(n):
                A[j][k] -= factor * A[i][k]
    return A

def matrix_multiply(A, B):
    m, n, p = len(A), len(B), len(B[0])
    C = [[0] * p for _ in range(m)]
    for i in range(m):
        for j in range(p):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_dnf(num_terms, num_vars):
        dnf = []
        for _ in range(num_terms):
            term = [random.choice([0, 1]) for _ in range(num_vars)]
            dnf.append(term)
        return dnf
    
    def compute_dispersion(dnf):
        n = len(dnf[0])
        vectors = [[int(x) for x in bin(i)[2:].zfill(n)] for i in range(2**n)]
        max_distance = 0
        for i in range(len(vectors)):
            for j in range(i+1, len(vectors)):
                distance = sum((vectors[i][k] - vectors[j][k])**2 for k in range(n))
                if distance > max_distance:
                    max_distance = distance
        return max_distance
    
    def is_k_clique(dnf, k):
        n = len(dnf[0])
        adjacency_matrix = [[0] * (2**n) for _ in range(2**n)]
        for i in range(len(vectors)):
            for j in range(i+1, len(vectors)):
                if sum((vectors[i][k] - vectors[j][k])**2 for k in range(n)) == n:
                    adjacency_matrix[i][j] = 1
                    adjacency_matrix[j][i] = 1
        
        def dfs(node, visited):
            stack = [node]
            while stack:
                node = stack.pop()
                if node not in visited:
                    visited.add(node)
                    for neighbor in range(2**n):
                        if adjacency_matrix[node][neighbor] == 1 and neighbor not in visited:
                            stack.append(neighbor)
        
        visited = set()
        dfs(0, visited)
        return len(visited) >= k
    
    n_max = 40
    m_max = 40
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""
    
    for n in range(5, n_max + 1):
        for m in range(5, min(m_max, 2**n) + 1):
            dnf = generate_dnf(m, n)
            dispersion = compute_dispersion(dnf)
            if dispersion > 5 * math.log(m):
                conjecture_holds = False
                counterexample = f"High dispersion for DNF with m={m}, n={n}"
                break
            instances_tested += 1
    
    k_max = 3
    for k in range(3, k_max + 1):
        dnf = generate_dnf(k-2, k)
        if not is_k_clique(dnf, k):
            conjecture_holds = False
            counterexample = f"Failed to find {k}-clique DNF with m={k-2}, n={k}"
            break
        instances_tested += 1
    
    return {
        "metric_name": "dispersion",
        "metric_value": compute_dispersion(generate_dnf(40, 40)),
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i - 1 for i in range(5, 35)]
    
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
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")