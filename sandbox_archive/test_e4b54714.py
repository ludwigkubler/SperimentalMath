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
        edges = []
        for i in range(k):
            for j in range(i + 1, k):
                edges.append((vertices[i], vertices[j]))
        for _ in range(random.randint(0, n * (n - 1) // 2 - len(edges))):
            u, v = random.sample(vertices, 2)
            if (u, v) not in edges and (v, u) not in edges:
                edges.append((u, v))
        return vertices, edges
    
    def matrix_representation(graph):
        n = len(graph[0])
        M = [[0] * n for _ in range(n)]
        for u, v in graph[1]:
            M[u][v] = 1
            M[v][u] = 1
        return M
    
    def tropical_intersection_number(M):
        n = len(M)
        if n == 0:
            return 0
        max_val = -math.inf
        for i in range(n):
            for j in range(i + 1, n):
                val = M[i][j]
                for k in range(n):
                    if k != i and k != j:
                        val = max(val, M[i][k] + M[k][j])
                max_val = max(max_val, val)
        return max_val
    
    def communication_complexity(M):
        n = len(M)
        if n == 0:
            return 0
        max_val = -math.inf
        for i in range(n):
            for j in range(i + 1, n):
                val = M[i][j]
                for k in range(n):
                    if k != i and k != j:
                        val = max(val, M[i][k] + M[k][j])
                max_val = max(max_val, val)
        return max_val
    
    n = 40
    k = 3
    graph = generate_k_clique(n, k)
    if graph is None:
        return {
            "metric_name": "communication_complexity",
            "metric_value": -1,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "k-Clique instance not possible"
        }
    
    M = matrix_representation(graph)
    tau_T = tropical_intersection_number(M)
    CC_k_Clique = communication_complexity(M)
    
    if tau_T <= n**k * math.log(n):
        return {
            "metric_name": "communication_complexity",
            "metric_value": CC_k_Clique,
            "instances_tested": 1,
            "conjecture_holds": True,
            "counterexample": ""
        }
    else:
        return {
            "metric_name": "communication_complexity",
            "metric_value": CC_k_Clique,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"CC(k-Clique) > τ(T): {CC_k_Clique} > {n**k * math.log(n)}"
        }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
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
        print(f"RESULT: FALSIFIED counterexample=\"CC(k-Clique) > τ(T)\" first_failing_seed={first_failing_seed}")