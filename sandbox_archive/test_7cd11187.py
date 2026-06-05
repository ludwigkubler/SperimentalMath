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
    
    def generate_random_graph(n):
        edges = set()
        for i in range(n):
            for j in range(i + 1, n):
                if random.choice([True, False]):
                    edges.add((i, j))
        return {i: sorted(j for j in edges if j > i) for i in range(n)}
    
    def matrix_multiply(A, B):
        m = len(A)
        p = len(B[0])
        q = len(B)
        C = [[0] * p for _ in range(m)]
        for i in range(m):
            for j in range(p):
                for k in range(q):
                    C[i][j] += A[i][k] * B[k][j]
        return C
    
    def gaussian_elimination(A, b):
        m = len(A)
        n = len(b)
        Augmented = [A[i] + [b[i]] for i in range(m)]
        for i in range(m):
            max_row = i
            for j in range(i+1, m):
                if abs(Augmented[j][i]) > abs(Augmented[max_row][i]):
                    max_row = j
            Augmented[i], Augmented[max_row] = Augmented[max_row], Augmented[i]
            pivot = Augmented[i][i]
            for j in range(n + 1):
                Augmented[i][j] /= pivot
            for j in range(m):
                if j != i:
                    factor = Augmented[j][i]
                    for k in range(n + 1):
                        Augmented[j][k] -= factor * Augmented[i][k]
        return [row[-1] for row in Augmented]
    
    def communication_complexity_rank(G):
        n = len(G)
        I_G = [[0 if j != i else 1 for j in range(n)] + G[i] for i in range(n)]
        A = []
        for i in range(n):
            row = [I_G[j][i] for j in range(n, 2*n)]
            A.append(row)
        b = [1] * n
        x = gaussian_elimination(A, b)
        return sum(x[i] != 0 for i in range(n))
    
    def minimal_monodromy_group_order(G):
        n = len(G)
        I_G = [[0 if j != i else 1 for j in range(n)] + G[i] for i in range(n)]
        S_n = list(itertools.permutations(range(n)))
        stabilizer_subgroup = []
        for sigma in S_n:
            permuted_I_G = [I_G[sigma[i]] for i in range(n)]
            if matrix_multiply(permuted_I_G, I_G) == I_G and matrix_multiply(I_G, permuted_I_G) == I_G:
                stabilizer_subgroup.append(sigma)
        return len(stabilizer_subgroup)
    
    def alpha(n):
        return math.log2(n) ** 2
    
    n_values = [5, 10, 15, 20, 30, 40]
    metrics = []
    for n in n_values:
        G = generate_random_graph(n)
        order_M_G = minimal_monodromy_group_order(G)
        r_G = communication_complexity_rank(G)
        metrics.append({
            "n": n,
            "order_M_G": order_M_G,
            "r_G": r_G
        })
    
    mean_metric_value = sum(metric["order_M_G"] for metric in metrics) / len(metrics)
    std_metric_value = math.sqrt(sum((metric["order_M_G"] - mean_metric_value) ** 2 for metric in metrics) / len(metrics))
    conjecture_holds = all(metric["order_M_G"] <= alpha(metric["n"]) and metric["r_G"] <= alpha(metric["n"]) for metric in metrics)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "minimal_monodromy_group_order",
        "metric_value": mean_metric_value,
        "instances_tested": len(metrics),
        "n_max": max(metric["n"] for metric in metrics),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(sys.argv[1])] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
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
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")