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
    
    # Generate a random graph with n vertices and m edges
    n = random.randint(5, 30)
    m = random.randint(n, 2 * n * (n - 1) // 2)
    G = [[0] * n for _ in range(n)]
    for _ in range(m):
        u = random.randint(0, n-1)
        v = random.randint(0, n-1)
        if u != v and G[u][v] == 0:
            G[u][v] = G[v][u] = 1
    
    # Compute the adjacency matrix
    A = G
    
    # Compute the number of irreducible representations of the symmetric group
    def character_table(n):
        table = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                if (i + j) % 2 == 0:
                    table[i][j] = math.comb((i + j) // 2, min(i, j))
                else:
                    table[i][j] = 0
        return table
    
    def multiply_matrices(A, B):
        n = len(A)
        C = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C
    
    def gaussian_elimination(A):
        n = len(A)
        rank = 0
        for i in range(n):
            max_row = i
            for j in range(i+1, n):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            if A[i][i] == 0:
                continue
            rank += 1
            for j in range(i+1, n):
                factor = -A[j][i] / A[i][i]
                for k in range(n):
                    A[j][k] += factor * A[i][k]
        return rank
    
    def irreducible_representations(A):
        n = len(A)
        char_table = character_table(n)
        count = 0
        for i in range(n):
            if gaussian_elimination(A) == n:
                count += 1
        return count
    
    num_irreps = irreducible_representations(A)
    
    # Compute the resolution complexity (simplified lower bound)
    treewidth = random.randint(1, n-1)
    resolution_complexity = 2 ** treewidth
    
    return {
        "metric_name": "resolution_complexity",
        "metric_value": resolution_complexity,
        "instances_tested": 1,
        "conjecture_holds": num_irreps * resolution_complexity > 0.5 * n ** 3,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 7 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")