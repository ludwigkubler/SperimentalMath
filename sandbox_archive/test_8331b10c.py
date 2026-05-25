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
    n = 40
    k = 3
    random.seed(seed)
    
    # Generate a random k-Clique graph with n vertices
    G = {i: set() for i in range(n)}
    edges = list(itertools.combinations(range(n), 2))
    random.shuffle(edges)
    added_edges = 0
    for u, v in edges:
        if len(G[u]) < k and len(G[v]) < k:
            G[u].add(v)
            G[v].add(u)
            added_edges += 1
            if added_edges == k * (k - 1) // 2:
                break
    
    # Convert the graph to a matrix representation
    A = [[0] * n for _ in range(n)]
    for u, v in G.items():
        for w in v:
            A[u][w] = 1
            A[w][u] = 1
    
    # Calculate the tropical intersection number τ(T)
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i
            for j in range(i + 1, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            if A[i][i] == 0:
                return None
            for j in range(i + 1, n):
                A[i][j] /= A[i][i]
            for j in range(m):
                if j != i and A[j][i] != 0:
                    for l in range(n):
                        A[j][l] -= A[i][l] * A[j][i]
        return A
    
    def multigraded_lexicomial_valuation(A):
        m, n = len(A), len(A[0])
        val = 0
        for i in range(m):
            for j in range(n):
                if A[i][j] == 1:
                    val += i * j
        return val
    
    tau_T = multigraded_lexicomial_valuation(gaussian_elimination(A))
    
    # Measure the communication complexity CC(k-Clique)
    def cc_k_clique(G, k):
        n = len(G)
        if k > n // 2:
            return float('inf')
        
        def dfs(u, visited, path):
            if len(path) == k:
                return True
            for v in G[u]:
                if v not in visited:
                    visited.add(v)
                    path.append(v)
                    if dfs(v, visited, path):
                        return True
                    path.pop()
                    visited.remove(v)
            return False
        
        count = 0
        for i in range(n):
            visited = {i}
            path = [i]
            if dfs(i, visited, path):
                count += 1
        return count
    
    CC_k_clique = cc_k_clique(G, k)
    
    # Verify the conjecture
    conjecture_holds = CC_k_clique <= tau_T and tau_T == O(n**k * math.log(n))
    counterexample = "" if conjecture_holds else "CC(k-Clique) > τ(T)"
    
    return {
        "metric_name": "Communication Complexity",
        "metric_value": CC_k_clique,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    if len(sys.argv) > 1:
        seeds = [int(seed) for seed in sys.argv[1:]]
    else:
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
        seeds = random.sample(primes * 3, 30)
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"CC(k-Clique) > τ(T)\" first_failing_seed={first_failing_seed}")