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
            factor = 1 / A[i][i]
            for j in range(n):
                A[i][j] *= factor
            for k in range(m):
                if k != i:
                    factor = A[k][i]
                    for j in range(n):
                        A[k][j] -= factor * A[i][j]
        return A
    
    def matrix_multiplication(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[0 for _ in range(p)] for _ in range(m)]
        for i in range(m):
            for j in range(p):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C
    
    def rank_of_matrix(A):
        A = gaussian_elimination(A)
        rank = 0
        for row in A:
            if any(row):
                rank += 1
        return rank
    
    def incidence_algebra(G):
        n = len(G)
        I = [[0] * (n * (n - 1) // 2) for _ in range(n * (n - 1) // 2)]
        edge_index = 0
        for i in range(n):
            for j in range(i + 1, n):
                if G[i][j]:
                    I[edge_index][edge_index] = 1
                    I[edge_index][i * (n - 1) // 2 + j - i - 1] = 1
                    I[edge_index][j * (n - 1) // 2 + i - j - 1] = 1
                    edge_index += 1
        return I
    
    def k_clique_instance(n):
        G = [[0] * n for _ in range(n)]
        edges = random.sample(range(n * (n - 1) // 2), n)
        edge_index = 0
        for i in range(n):
            for j in range(i + 1, n):
                if edge_index < len(edges) and edge_index == edges[edge_index]:
                    G[i][j] = G[j][i] = 1
                    edge_index += 1
        return G
    
    def affine_representation(G):
        I = incidence_algebra(G)
        return rank_of_matrix(I)
    
    n = random.randint(5, 40)
    G = k_clique_instance(n)
    rank = affine_representation(G)
    
    metric_name = "Minimal Rank of Affine Representation"
    metric_value = rank
    instances_tested = 1
    conjecture_holds = rank >= math.sqrt(n)
    counterexample = "" if conjecture_holds else f"n={n}, rank={rank}"
    
    return {
        "metric_name": metric_name,
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
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"n={result['instances_tested']}, rank={result['metric_value']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")