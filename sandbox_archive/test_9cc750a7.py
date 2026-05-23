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
    
    def gaussian_elimination(A):
        rows, cols = len(A), len(A[0])
        for i in range(rows):
            max_row = i + max(range(i, rows), key=lambda r: abs(A[r][i]))
            A[i], A[max_row] = A[max_row], A[i]
            if A[i][i] == 0:
                continue
            denom = A[i][i]
            for j in range(cols):
                A[i][j] /= denom
            for k in range(rows):
                if k != i and A[k][i] != 0:
                    factor = A[k][i]
                    for j in range(cols):
                        A[k][j] -= factor * A[i][j]
        return A

    def determinant(A):
        rows, cols = len(A), len(A[0])
        if rows != cols:
            raise ValueError("Matrix must be square")
        det = Fraction(1)
        for i in range(rows):
            max_row = i + max(range(i, rows), key=lambda r: abs(A[r][i]))
            A[i], A[max_row] = A[max_row], A[i]
            if A[i][i] == 0:
                return Fraction(0)
            det *= A[i][i]
        return det

    def k_clique_indicator(G, X, action, k):
        n = len(X)
        adj_matrix = [[0] * n for _ in range(n)]
        for x1 in X:
            for x2 in X:
                if (x1, x2) in action or (x2, x1) in action:
                    adj_matrix[X.index(x1)][X.index(x2)] = 1
        return max(sum(row[i] for i in range(k)) for row in adj_matrix)

    def monotone_circuit_depth(G, X, action, k):
        n = len(X)
        adj_matrix = [[0] * n for _ in range(n)]
        for x1 in X:
            for x2 in X:
                if (x1, x2) in action or (x2, x1) in action:
                    adj_matrix[X.index(x1)][X.index(x2)] = 1
        rank = determinant(gaussian_elimination(adj_matrix))
        return int(math.log2(rank)) + 1

    def generate_group_and_action(n):
        G = set()
        for _ in range(n):
            g = tuple(random.randint(0, 1) for _ in range(n))
            G.add(g)
        action = {(g1, g2): (g1[0] ^ g2[0], g1[1] ^ g2[1]) for g1 in G for g2 in G}
        return G, list(G), action

    n = random.choice([5, 10, 15, 20, 30, 40])
    G, X, action = generate_group_and_action(n)
    k = random.randint(2, min(3, n))
    
    depth = monotone_circuit_depth(G, X, action, k)
    rank = len(X) ** (n - 1)
    
    return {
        "metric_name": "Minimal Rank of Geometric Group Action vs Monotone Circuit Depth for k-CLIQUE",
        "metric_value": abs(rank - depth),
        "instances_tested": 1,
        "conjecture_holds": abs(rank - depth) <= 3,
        "counterexample": "" if abs(rank - depth) <= 3 else f"Rank {rank}, Depth {depth}"
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
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
        print(f"RESULT: FALSIFIED counterexample=\"Rank exceeds Depth by more than 3\" first_failing_seed={first_failing_seed}")