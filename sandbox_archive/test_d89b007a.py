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
    
    def generate_random_graph(n):
        return [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    
    def matrix_mult(A, B):
        n = len(A)
        C = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C
    
    def gaussian_elimination(A):
        n = len(A)
        for i in range(n):
            max_row = i
            for j in range(i+1, n):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            pivot = A[i][i]
            if pivot == 0:
                continue
            for j in range(i, n):
                A[i][j] /= pivot
            for j in range(n):
                if j != i:
                    factor = A[j][i]
                    for k in range(i, n):
                        A[j][k] -= factor * A[i][k]
        rank = sum(1 for row in A if any(row))
        return rank
    
    def generate_subspaces(A, d):
        n = len(A)
        subspaces = []
        for i in range(n):
            for j in range(i+1, n):
                subspace = [A[i], A[j]]
                subspaces.append(subspace)
        return subspaces
    
    def rank(subspace, A):
        B = [[0] * len(subspace) for _ in range(len(subspace))]
        for i in range(len(subspace)):
            for j in range(len(subspace)):
                B[i][j] = sum(A[k][i] * A[k][j] for k in range(len(A)))
        return gaussian_elimination(B)
    
    n = 10
    d = 2
    k = 3
    
    graph = generate_random_graph(n)
    subspaces = generate_subspaces(graph, d)
    min_rank = float('inf')
    
    for subspace in subspaces:
        rank_value = rank(subspace, graph)
        if rank_value < min_rank:
            min_rank = rank_value
    
    metric_value = min_rank
    instances_tested = len(subspaces)
    conjecture_holds = min_rank >= (n**2 / k) * 0.5
    counterexample = "" if conjecture_holds else "min_rank too small"
    
    return {
        "metric_name": "Minimum Rank",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))**0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='min_rank too small' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient data")