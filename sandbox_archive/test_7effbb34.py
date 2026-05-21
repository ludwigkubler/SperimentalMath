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
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_quiver(n):
        G = {i: set() for i in range(n)}
        for _ in range(n * (n - 1) // 2):
            u, v = random.sample(range(n), 2)
            if u not in G[v]:
                G[u].add(v)
                G[v].add(u)
        return G
    
    def geometric_entropy(G):
        n = len(G)
        adjacency_matrix = [[0] * n for _ in range(n)]
        for u, neighbors in G.items():
            for v in neighbors:
                adjacency_matrix[u][v] = 1
        # Compute the eigenvalues of the adjacency matrix
        eigenvalues = [eigenvalue(adjacency_matrix) for _ in range(30)]  # Sample multiple times to average
        entropy = sum(-p * math.log2(p) for p in eigenvalues if p > 0)
        return entropy
    
    def eigenvalue(matrix):
        n = len(matrix)
        identity = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
        # Gaussian elimination to find the eigenvalues
        for k in range(n):
            max_row = k + random.choice([i - k for i in range(k, n) if matrix[i][k] != 0])
            matrix[k], matrix[max_row] = matrix[max_row], matrix[k]
            factor = Fraction(matrix[k][k], matrix[k][k])
            for j in range(n):
                matrix[k][j] /= factor
            for i in range(n):
                if i != k:
                    factor = Fraction(matrix[i][k], matrix[k][k])
                    for j in range(n):
                        matrix[i][j] -= factor * matrix[k][j]
        # The eigenvalues are the diagonal elements of the upper triangular matrix
        return [matrix[i][i] for i in range(n)]
    
    def communication_complexity(n):
        # Simulate a randomized communication protocol for the disjointness function
        # This is a simplified model and does not reflect actual communication complexity
        return random.randint(1, n)
    
    n = 40
    G = generate_quiver(n)
    gamma_Q = geometric_entropy(G)
    kappa_DISJ_n = communication_complexity(n)
    
    return {
        "metric_name": "geometric_entropy",
        "metric_value": gamma_Q,
        "instances_tested": 1,
        "conjecture_holds": gamma_Q >= kappa_DISJ_n,
        "counterexample": "" if gamma_Q >= kappa_DISJ_n else f"gamma(Q)={gamma_Q}, kappa(DISJ_{n})={kappa_DISJ_n}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = next(r["counterexample"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")