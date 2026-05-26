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
            max_row = i
            for j in range(i+1, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            factor = A[i][i]
            for j in range(n):
                A[i][j] /= factor
            for j in range(m):
                if j != i:
                    factor = A[j][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        return A

    def matrix_multiplication(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[0]*p for _ in range(m)]
        for i in range(m):
            for j in range(p):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def tautology_degree(G):
        n = len(G)
        circuit = [[0]*n for _ in range(2**n)]
        for i in range(n):
            circuit[1<<i][i] = 1
        for k in range(1, n+1):
            for s in range(2**n):
                if (s & ((1 << k) - 1)) == (1 << k) - 1:
                    continue
                for j in range(n):
                    if G[j][k] and (s >> j) & 1:
                        circuit[s ^ (1 << j)][k] = max(circuit[s ^ (1 << j)][k], circuit[s][j])
        return max(max(row) for row in circuit)

    def minimal_rank(G):
        n = len(G)
        A = [[0]*n for _ in range(n)]
        for i in range(n):
            for j in range(i+1, n):
                if G[i][j]:
                    A[i][j] = 1
                    A[j][i] = 1
        rank = 0
        for row in gaussian_elimination(A):
            if any(row):
                rank += 1
        return rank

    def generate_graph(n, density=0.5):
        G = [[0]*n for _ in range(n)]
        for i in range(n):
            for j in range(i+1, n):
                if random.random() < density:
                    G[i][j] = 1
                    G[j][i] = 1
        return G

    n = random.choice([5, 10, 15, 20, 30, 40])
    G = generate_graph(n)
    
    rank = minimal_rank(G)
    degree = tautology_degree(G)
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": rank <= degree,
        "counterexample": "" if rank <= degree else f"Graph with n={n}, rank={rank}, degree={degree}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    metric_values = [r["metric_value"] for r in results]
    conjecture_holds = all(r["conjecture_holds"] for r in results)
    mean = sum(metric_values) / len(metric_values)
    std = math.sqrt(sum((x - mean) ** 2 for x in metric_values) / len(metric_values))
    
    if conjecture_holds:
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction=1.0")
    elif any(r["counterexample"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{next(r['counterexample'] for r in results if r['counterexample'])}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE all_trials_used_n_1")