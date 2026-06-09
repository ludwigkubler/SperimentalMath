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
        G = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i+1, n):
                if random.random() < 0.5:
                    G[i][j] = G[j][i] = 1
        return G
    
    def matrix_multiply(A, B):
        m, k, n = len(A), len(B[0]), len(B)
        C = [[0] * n for _ in range(m)]
        for i in range(m):
            for j in range(n):
                for l in range(k):
                    C[i][j] += A[i][l] * B[l][j]
        return C
    
    def gaussian_elimination(A, b):
        m, n = len(A), len(b)
        Augmented = [A[i] + [b[i]] for i in range(m)]
        for i in range(m):
            max_row = i
            for j in range(i+1, m):
                if abs(Augmented[j][i]) > abs(Augmented[max_row][i]):
                    max_row = j
            Augmented[i], Augmented[max_row] = Augmented[max_row], Augmented[i]
            factor = 1 / Augmented[i][i]
            for j in range(n):
                Augmented[i][j] *= factor
            for j in range(m):
                if j != i:
                    factor = Augmented[j][i]
                    for k in range(n):
                        Augmented[j][k] -= factor * Augmented[i][k]
        return [row[-1] for row in Augmented]
    
    def compute_minimal_representation_degree(G):
        n = len(G)
        A = [[0] * (n + 1) for _ in range(n + 1)]
        b = [0] * (n + 1)
        for i in range(n):
            for j in range(i+1, n):
                if G[i][j]:
                    A[i][i] += 1
                    A[j][j] += 1
                    A[i][j] -= 1
                    A[j][i] -= 1
                    b[i] += 1
                    b[j] += 1
        return sum(gaussian_elimination(A, b))
    
    def compute_communication_complexity_rank_variance(G):
        n = len(G)
        rank_sum = 0
        for i in range(n):
            row_sum = sum(G[i])
            if row_sum > 0:
                rank_sum += math.log2(row_sum + 1)
        return rank_sum / n
    
    def pearson_correlation(X, Y):
        mean_X = sum(X) / len(X)
        mean_Y = sum(Y) / len(Y)
        cov = sum((X[i] - mean_X) * (Y[i] - mean_Y) for i in range(len(X))) / len(X)
        std_X = math.sqrt(sum((X[i] - mean_X) ** 2 for i in range(len(X))) / len(X))
        std_Y = math.sqrt(sum((Y[i] - mean_Y) ** 2 for i in range(len(Y))) / len(Y))
        return cov / (std_X * std_Y)
    
    n_values = [5, 10, 15, 20, 30, 40]
    d_values = []
    r_values = []
    
    for n in n_values:
        G = generate_random_graph(n)
        d = compute_minimal_representation_degree(G)
        r = compute_communication_complexity_rank_variance(G)
        d_values.append(d)
        r_values.append(r)
    
    correlation_coefficient = pearson_correlation(d_values, r_values)
    conjecture_holds = correlation_coefficient >= 0
    counterexample = "" if conjecture_holds else "Pearson correlation coefficient is negative"
    
    return {
        "metric_name": "Pearson Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
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
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Pearson correlation coefficient is negative\" first_failing_seed={first_failing_seed}")