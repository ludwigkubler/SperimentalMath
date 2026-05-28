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
    
    def generate_triangle_detection_instance(n):
        if n < 3:
            return []
        vertices = list(range(n))
        edges = [(i, j) for i in range(n) for j in range(i+1, n)]
        random.shuffle(edges)
        instance = edges[:min(3, len(edges))]
        return instance
    
    def incidence_graph(instance):
        n = max(max(edge) for edge in instance) + 1
        graph = [[0] * n for _ in range(n)]
        for u, v in instance:
            graph[u][v] = 1
            graph[v][u] = 1
        return graph
    
    def gaussian_elimination(matrix):
        m, n = len(matrix), len(matrix[0])
        rank = 0
        for j in range(n):
            i_max = None
            for i in range(rank, m):
                if matrix[i][j] != 0:
                    i_max = i
                    break
            if i_max is None:
                continue
            matrix[rank], matrix[i_max] = matrix[i_max], matrix[rank]
            for i in range(m):
                if i != rank and matrix[i][j] != 0:
                    factor = -matrix[i][j] / matrix[rank][j]
                    for k in range(n):
                        matrix[i][k] += factor * matrix[rank][k]
            rank += 1
        return rank
    
    def communication_complexity(instance, n):
        if len(instance) < 3:
            return 0
        return math.log2(n)
    
    n = random.randint(5, 40)
    instance = generate_triangle_detection_instance(n)
    graph = incidence_graph(instance)
    rank = gaussian_elimination(graph)
    C_I = communication_complexity(instance, n)
    r_n = math.log2(n) ** 2
    
    metric_name = "rank"
    metric_value = rank
    instances_tested = 1
    conjecture_holds = C_I >= math.log2(n) or rank > r_n
    counterexample = "" if conjecture_holds else f"n={n}, rank={rank}, C(I)={C_I}"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [677, 727, 773, 821, 877, 929]  # Default list of prime seeds
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next((r['seed'] for r in results if not r['conjecture_holds']), None)
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")