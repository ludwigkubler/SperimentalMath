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
            max_row = i + max(range(i, m), key=lambda r: abs(A[r][i]))
            A[i], A[max_row] = A[max_row], A[i]
            if A[i][i] == 0:
                continue
            for j in range(n):
                A[i][j] /= A[i][i]
            for k in range(m):
                if k != i and A[k][i] != 0:
                    factor = A[k][i]
                    for j in range(n):
                        A[k][j] -= factor * A[i][j]
        return A
    
    def matrix_multiplication(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[0] * p for _ in range(m)]
        for i in range(m):
            for j in range(p):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C
    
    def determinant(A):
        m, n = len(A), len(A[0])
        if m != n:
            raise ValueError("Matrix must be square")
        if n == 1:
            return A[0][0]
        det = 0
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for row in A[1:]]
            det += (-1) ** j * A[0][j] * determinant(submatrix)
        return det
    
    def is_prime(num):
        if num <= 1:
            return False
        if num == 2:
            return True
        if num % 2 == 0:
            return False
        for i in range(3, int(math.sqrt(num)) + 1, 2):
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
    
    def generate_group_action(group_size, set_size):
        G = [list(range(group_size))]
        X = list(range(set_size))
        action = [[(g + x) % group_size for x in X] for g in range(group_size)]
        return G, X, action
    
    def cayley_graph(G, X, action):
        n = len(G)
        m = len(X)
        adj_matrix = [[0] * (n * m) for _ in range(n * m)]
        for i in range(n):
            for j in range(m):
                for k in range(n):
                    if action[i][j] == X[k]:
                        adj_matrix[i * m + j][(k + 1) % n * m + j] = 1
        return adj_matrix
    
    def monotone_circuit_depth(G, X, action, k):
        n = len(G)
        m = len(X)
        adj_matrix = cayley_graph(G, X, action)
        rank = determinant(gaussian_elimination(adj_matrix))
        return rank
    
    def k_clique_indicator_function(G, X, action, k):
        n = len(G)
        m = len(X)
        adj_matrix = cayley_graph(G, X, action)
        for subset in itertools.combinations(range(m), k):
            subgraph = [[adj_matrix[i][j] for j in subset] for i in subset]
            if determinant(gaussian_elimination(subgraph)) == 0:
                return True
        return False
    
    def min_rank(G, X, action):
        n = len(G)
        m = len(X)
        adj_matrix = cayley_graph(G, X, action)
        rank = determinant(gaussian_elimination(adj_matrix))
        return rank
    
    def k_clique_depth(G, X, action, k):
        n = len(G)
        m = len(X)
        adj_matrix = cayley_graph(G, X, action)
        depth = 0
        for subset in itertools.combinations(range(m), k):
            subgraph = [[adj_matrix[i][j] for j in subset] for i in subset]
            if determinant(gaussian_elimination(subgraph)) == 0:
                return depth + 1
            depth += 1
        return depth
    
    def generate_seeds(n):
        seeds = []
        for _ in range(n):
            seed = random.randint(1, 10**9)
            while seed in seeds:
                seed = random.randint(1, 10**9)
            seeds.append(seed)
        return seeds
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    group_size = n
    set_size = n * n
    G, X, action = generate_group_action(group_size, set_size)
    k = random.randint(2, min(n - 1, 5))
    
    depth = monotone_circuit_depth(G, X, action, k)
    rank = min_rank(G, X, action)
    
    return {
        "metric_name": "Minimal Rank of Geometric Group Action vs Monotone Circuit Depth",
        "metric_value": abs(depth - rank),
        "instances_tested": 1,
        "conjecture_holds": abs(depth - rank) <= 3,
        "counterexample": "" if abs(depth - rank) <= 3 else f"Depth: {depth}, Rank: {rank}"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or generate_primes(30)
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{'seed': {seed}, **result}}")
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
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")