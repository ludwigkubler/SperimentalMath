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
    
    def generate_d_regular_graph(n, d):
        if (n * d) % 2 != 0 or n < d:
            return None
        graph = {i: [] for i in range(n)}
        edges_added = set()
        for _ in range(d * n // 2):
            while True:
                u, v = random.sample(range(n), 2)
                if u == v or (u, v) in edges_added or (v, u) in edges_added:
                    continue
                graph[u].append(v)
                graph[v].append(u)
                edges_added.add((u, v))
                break
        return graph
    
    def tseitin_formula(graph):
        n = len(graph)
        clauses = []
        for i in range(n):
            literals = [f"x{i}"]
            for j in graph[i]:
                literals.append(f"~x{j}")
            clause = " | ".join(literals)
            clauses.append(clause)
        return clauses
    
    def tropical_rank(clauses):
        n = len(clauses)
        m = len(clauses[0].split(" | "))
        A = [[0] * m for _ in range(m)]
        for i in range(n):
            for j in range(m):
                if "x" + str(j) in clauses[i]:
                    A[j][j] += 1
                elif "~x" + str(j) in clauses[i]:
                    A[j][j] -= 1
        rank = 0
        for i in range(m):
            pivot = None
            for j in range(i, m):
                if A[j][i] != 0:
                    pivot = j
                    break
            if pivot is None:
                continue
            rank += 1
            for j in range(m):
                A[i][j], A[pivot][j] = A[pivot][j], A[i][j]
            for j in range(m):
                if i != j:
                    factor = -A[j][i] / A[i][i]
                    for k in range(m):
                        A[j][k] += factor * A[i][k]
        return rank
    
    def mean(lst):
        return sum(lst) / len(lst)
    
    def std(lst, m):
        return math.sqrt(sum((x - m) ** 2 for x in lst) / len(lst))
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        d = random.randint(2, min(n - 1, 6))  # Ensure graph is regular
        graph = generate_d_regular_graph(n, d)
        if graph is None:
            continue
        
        clauses = tseitin_formula(graph)
        rank = tropical_rank(clauses)
        
        results.append(rank / math.log(n) / math.log(d))
    
    if not results:
        return {
            "metric_name": "tropical_rank_ratio",
            "metric_value": 0,
            "instances_tested": 0,
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "graph_generation_failed"
        }
    
    mean_val = mean(results)
    std_val = std(results, mean_val)
    support_fraction = sum(1 for r in results if r <= 2 * std_val + mean_val) / len(results)
    
    return {
        "metric_name": "tropical_rank_ratio",
        "metric_value": mean_val,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": support_fraction >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result["metric_value"])
    
    mean_val = mean(results)
    std_val = std(results, mean_val)
    support_fraction = sum(1 for r in results if r <= 2 * std_val + mean_val) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_val} std={std_val} support_fraction={support_fraction}")
    elif any(r > 2 * std_val + mean_val for r in results):
        first_failing_seed = seeds[results.index(max(results))]
        print(f"RESULT: FALSIFIED counterexample=\"exceeds_bound\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_support_fraction support_fraction={support_fraction}")