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
        if n < k:
            return None
        vertices = list(range(n))
        clique = [vertices[:k]]
        for i in range(k, n):
            new_vertex = random.choice(vertices[:i])
            clique.append(clique[0] + [new_vertex])
        return clique
    
    def incidence_graph(clique):
        graph = {v: [] for v in set(sum(clique, []))}
        for edge in clique:
            for i in range(len(edge)):
                for j in range(i + 1, len(edge)):
                    if edge[i] not in graph[edge[j]]:
                        graph[edge[i]].append(edge[j])
                    if edge[j] not in graph[edge[i]]:
                        graph[edge[j]].append(edge[i])
        return graph
    
    def quandle_representation(graph):
        n = len(graph)
        q = [[0 for _ in range(n)] for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                if j in graph[i]:
                    q[i][j] = 1
                else:
                    q[i][j] = -1
        return q
    
    def min_rank(matrix):
        m, n = len(matrix), len(matrix[0])
        rank = 0
        for i in range(m):
            if matrix[i][i] != 0:
                for j in range(n):
                    matrix[j][i] /= matrix[i][i]
                for j in range(i + 1, m):
                    factor = -matrix[j][i]
                    for k in range(n):
                        matrix[j][k] += factor * matrix[i][k]
                rank += 1
            else:
                found_pivot = False
                for j in range(i + 1, m):
                    if matrix[j][i] != 0:
                        matrix[i], matrix[j] = matrix[j], matrix[i]
                        found_pivot = True
                        break
                if not found_pivot:
                    continue
                for j in range(n):
                    matrix[j][i] /= matrix[i][i]
                for j in range(i + 1, m):
                    factor = -matrix[j][i]
                    for k in range(n):
                        matrix[j][k] += factor * matrix[i][k]
                rank += 1
        return rank
    
    n = random.randint(5, 40)
    k = random.randint(2, min(n, 3))
    clique = generate_k_clique(n, k)
    if clique is None:
        return {
            "metric_name": "min_rank",
            "metric_value": 0,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "k-clique generation failed"
        }
    
    graph = incidence_graph(clique)
    q = quandle_representation(graph)
    rank = min_rank(q)
    
    return {
        "metric_name": "min_rank",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": rank >= k,
        "counterexample": "" if rank >= k else f"rank={rank}, expected at least {k}"
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    std_rank = math.sqrt(sum((r["metric_value"] - mean_rank) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"rank<{result['metric_value']}, expected at least {k}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")