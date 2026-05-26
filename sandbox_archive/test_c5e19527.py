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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def construct_graph(f, n):
        graph = {}
        for i in range(2**n):
            for j in range(i+1, 2**n):
                if f[i] == f[j]:
                    if i not in graph:
                        graph[i] = []
                    if j not in graph:
                        graph[j] = []
                    graph[i].append(j)
                    graph[j].append(i)
        return graph
    
    def laplacian_matrix(graph, n):
        L = [[0]*2**n for _ in range(2**n)]
        for i in range(2**n):
            degree = len(graph.get(i, []))
            L[i][i] = degree
            for j in graph.get(i, []):
                L[i][j] = -1
                L[j][i] = -1
        return L
    
    def matrix_rank(matrix):
        m, n = len(matrix), len(matrix[0])
        rank = 0
        for i in range(min(m, n)):
            if matrix[i][i] != 0:
                for j in range(i+1, m):
                    factor = matrix[j][i] / matrix[i][i]
                    for k in range(n):
                        matrix[j][k] -= factor * matrix[i][k]
                rank += 1
        return rank
    
    n = random.randint(5, 40)
    f = generate_boolean_function(n)
    G_f = construct_graph(f, n)
    L_G_f = laplacian_matrix(G_f, n)
    rank_L_G_f = matrix_rank(L_G_f)
    
    metric_name = "minimal_rank_laplacian"
    metric_value = rank_L_G_f
    instances_tested = 1
    conjecture_holds = rank_L_G_f >= math.log(n, 2)
    counterexample = "" if conjecture_holds else f"rank={rank_L_G_f}, expected=Ω(log {n})"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"rank < Ω(log n)\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")