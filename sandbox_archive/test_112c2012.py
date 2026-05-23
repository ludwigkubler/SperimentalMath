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
    
    def generate_k_clique(n, k):
        vertices = list(range(n))
        edges = []
        for _ in range(k * n // 2):
            u = random.choice(vertices)
            v = random.choice(vertices)
            if u != v and (u, v) not in edges and (v, u) not in edges:
                edges.append((u, v))
        return vertices, edges
    
    def monomial_to_index(monomial):
        return sum(1 << i for i in monomial if i in monomial)
    
    def ideal_to_matrix(ideal, n):
        matrix = [[0] * (2 ** n) for _ in range(2 ** n)]
        for monomial in ideal:
            index = monomial_to_index(monomial)
            for i in range(2 ** n):
                if all(i & (1 << j) == 0 for j in monomial):
                    matrix[index][i] = 1
        return matrix
    
    def gaussian_elimination(matrix, n):
        rows, cols = len(matrix), len(matrix[0])
        rank = 0
        for i in range(cols):
            pivot_row = -1
            for r in range(rank, rows):
                if matrix[r][i] != 0:
                    pivot_row = r
                    break
            if pivot_row == -1:
                continue
            matrix[pivot_row], matrix[rank] = matrix[rank], matrix[pivot_row]
            for r in range(rows):
                if r != rank and matrix[r][i] != 0:
                    factor = matrix[r][i] / matrix[rank][i]
                    for c in range(cols):
                        matrix[r][c] -= factor * matrix[rank][c]
            rank += 1
        return rank
    
    def minimal_rank(n, k):
        vertices, edges = generate_k_clique(n, k)
        ideal = [tuple(sorted(edge)) for edge in edges]
        matrix = ideal_to_matrix(ideal, n)
        return gaussian_elimination(matrix, n)
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            rank = minimal_rank(n, k)
            if rank > n ** (1.5 - k):
                return {
                    "metric_name": "minimal_rank",
                    "metric_value": rank,
                    "instances_tested": 1,
                    "conjecture_holds": False,
                    "counterexample": f"n={n}, k={k}, rank={rank} > O(n^(1.5-k))"
                }
            results.append(rank)
    
    mean = sum(results) / len(results)
    std = math.sqrt(sum((x - mean) ** 2 for x in results) / len(results))
    return {
        "metric_name": "minimal_rank",
        "metric_value": mean,
        "instances_tested": len(results),
        "conjecture_holds": all(rank <= n ** (1.5 - k) for rank, n, k in zip(results, [5] * 5 + [10] * 5 + [15] * 5 + [20] * 5 + [30] * 5 + [40] * 5)),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = list(map(int, sys.argv[1:])) or [2**i - 1 for i in range(1, 6)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result["metric_value"])
    
    mean = sum(results) / len(results)
    std = math.sqrt(sum((x - mean) ** 2 for x in results) / len(results))
    support_fraction = sum(1 for r in results if all(r <= n ** (1.5 - k) for _, n, k in zip([r] * 6, [5] * 5 + [10] * 5 + [15] * 5 + [20] * 5 + [30] * 5 + [40] * 5))) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    elif any(r > n ** (1.5 - k) for _, n, k in zip(results, [5] * 6 + [10] * 6 + [15] * 6 + [20] * 6 + [30] * 6 + [40] * 6)):
        first_failing_seed = seeds[results.index(max(results))]
        print(f"RESULT: FALSIFIED counterexample=\"n={n}, k={k}, rank={r} > O(n^(1.5-k))\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_support")