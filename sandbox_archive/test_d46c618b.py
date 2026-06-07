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
        graph = [[0] * n for _ in range(n)]
        edges = set()
        while len(edges) < n * (n - 1) // 2:
            u, v = random.sample(range(n), 2)
            if u != v and (u, v) not in edges and (v, u) not in edges:
                graph[u][v] = 1
                graph[v][u] = 1
                edges.add((u, v))
        return graph
    
    def matrix_multiply(A, B):
        n = len(A)
        C = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C
    
    def gaussian_elimination(A, b):
        n = len(A)
        augmented_matrix = [A[i] + [b[i]] for i in range(n)]
        for i in range(n):
            max_row = i
            for j in range(i+1, n):
                if abs(augmented_matrix[j][i]) > abs(augmented_matrix[max_row][i]):
                    max_row = j
            augmented_matrix[i], augmented_matrix[max_row] = augmented_matrix[max_row], augmented_matrix[i]
            pivot = augmented_matrix[i][i]
            for j in range(i, n+1):
                augmented_matrix[i][j] /= pivot
            for j in range(n):
                if j != i:
                    factor = augmented_matrix[j][i]
                    for k in range(i, n+1):
                        augmented_matrix[j][k] -= factor * augmented_matrix[i][k]
        return [row[-1] for row in augmented_matrix]
    
    def hdim(G):
        n = len(G)
        A = [[0] * (n + 1) for _ in range(n + 1)]
        for i in range(n):
            for j in range(i, n):
                if G[i][j]:
                    A[i][j] = A[j][i] = 1
        A[-1][-1] = 1
        b = [0] * n + [1]
        x = gaussian_elimination(A, b)
        return sum(x[:n])
    
    def ccr(G):
        n = len(G)
        rank = 0
        for i in range(n):
            if any(G[i][j] for j in range(i+1, n)):
                rank += 1
        return rank
    
    n_values = [5, 10, 15, 20, 30, 40]
    hdim_sum = 0
    ccr_sum = 0
    instances_tested = 0
    n_max = 0
    
    for n in n_values:
        for _ in range(5):
            G = generate_random_graph(n)
            hdim_val = hdim(G)
            ccr_val = ccr(G)
            hdim_sum += hdim_val
            ccr_sum += ccr_val
            instances_tested += 1
            if n > n_max:
                n_max = n
    
    mean_hdim = hdim_sum / instances_tested
    mean_ccr = ccr_sum / instances_tested
    correlation_coefficient = (instances_tested * sum(hdim_val * ccr_val for hdim_val, ccr_val in zip(range(n_values[0], n_values[-1] + 1), range(n_values[0], n_values[-1] + 1))) -
                               mean_hdim * instances_tested - mean_ccr * instances_tested) / math.sqrt((instances_tested * sum(hdim_val**2 for hdim_val in range(n_values[0], n_values[-1] + 1)) - mean_hdim**2) *
                                                                                           (instances_tested * sum(ccr_val**2 for ccr_val in range(n_values[0], n_values[-1] + 1)) - mean_ccr**2))
    
    p_value = 2 * (1 - math.erf(abs(correlation_coefficient) / math.sqrt(2 * instances_tested - 3)))
    
    conjecture_holds = correlation_coefficient > 0.8 and p_value < 0.05
    counterexample = "" if conjecture_holds else "correlation_coefficient={}, p_value={}".format(correlation_coefficient, p_value)
    
    return {
        "metric_name": "Pearson Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print("TRIAL: {}".format(result))
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print("RESULT: SUPPORTED mean={} std={} support_fraction={}".format(mean_metric_value, std_metric_value, support_fraction))
    elif support_fraction >= 0.8:
        print("RESULT: SUPPORTED mean={} std={} support_fraction={}".format(mean_metric_value, std_metric_value, support_fraction))
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print("RESULT: FALSIFIED counterexample=\"{}\" first_failing_seed={}".format(results[first_failing_seed]["counterexample"], first_failing_seed))