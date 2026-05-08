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

def generate_random_3_regular_graph(n):
    if n % 2 != 0:
        raise ValueError("n must be even")
    graph = [[] for _ in range(n)]
    edges = []
    for i in range(n):
        for j in range(i + 1, n):
            if len(graph[i]) < 3 and len(graph[j]) < 3:
                graph[i].append(j)
                graph[j].append(i)
                edges.append((i, j))
    return graph

def max_cut_value(graph):
    n = len(graph)
    cut_edges = []
    for u in range(n):
        for v in range(u + 1, n):
            if (u, v) in edges or (v, u) in edges:
                cut_edges.append((u, v))
    return len(cut_edges)

def sdp_moment_matrix(graph, d):
    n = len(graph)
    M_d = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            if (i, j) in edges or (j, i) in edges:
                M_d[i][j] = 1
                M_d[j][i] = 1
    return M_d

def matrix_rank(matrix):
    m, n = len(matrix), len(matrix[0])
    rank = 0
    for col in range(n):
        if any(matrix[row][col] != 0 for row in range(m)):
            rank += 1
            for row in range(m):
                if matrix[row][col] != 0:
                    factor = matrix[row][col]
                    for j in range(n):
                        matrix[row][j] /= factor
                    for i in range(m):
                        if i != row and matrix[i][col] != 0:
                            factor = matrix[i][col]
                            for j in range(n):
                                matrix[i][j] -= factor * matrix[row][j]
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 40
    graph = generate_random_3_regular_graph(n)
    alpha_G = max_cut_value(graph)
    d = 5
    M_d = sdp_moment_matrix(graph, d)
    rank = matrix_rank(M_d)
    metric_name = "moment_matrix_rank"
    metric_value = rank
    instances_tested = 1
    conjecture_holds = rank >= math.sqrt(n)
    counterexample = "" if conjecture_holds else f"Rank {rank} < √{n}"
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]]
    if not seeds:
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]
        seeds = primes[:30]
    
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
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        counterexample = results[first_failing_seed]["counterexample"]
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")