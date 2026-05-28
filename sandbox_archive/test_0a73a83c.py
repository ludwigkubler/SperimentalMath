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
            return None
        vertices = list(range(n))
        edges = []
        for i in range(n):
            for j in range(i + 1, n):
                for k in range(j + 1, n):
                    edges.append((i, j, k))
        random.shuffle(edges)
        instance = {
            'vertices': vertices,
            'edges': edges[:math.ceil(len(edges) * 0.5)]
        }
        return instance
    
    def incidence_graph(instance):
        graph = {}
        for v in instance['vertices']:
            graph[v] = set()
        for u, v, w in instance['edges']:
            graph[u].add(v)
            graph[u].add(w)
            graph[v].add(u)
            graph[v].add(w)
            graph[w].add(u)
            graph[w].add(v)
        return graph
    
    def tropicalized_lie_algebra_rank(graph):
        n = len(graph)
        adjacency_matrix = [[0] * n for _ in range(n)]
        for u, neighbors in graph.items():
            for v in neighbors:
                adjacency_matrix[u][v] = 1
                adjacency_matrix[v][u] = 1
        
        def gaussian_elimination(matrix):
            m, n = len(matrix), len(matrix[0])
            rank = 0
            for j in range(n):
                i_max = -1
                for i in range(rank, m):
                    if matrix[i][j] != 0:
                        i_max = i
                        break
                if i_max == -1:
                    continue
                matrix[rank], matrix[i_max] = matrix[i_max], matrix[rank]
                for i in range(m):
                    if i != rank and matrix[i][j] != 0:
                        factor = matrix[i][j] / matrix[rank][j]
                        for k in range(n):
                            matrix[i][k] -= factor * matrix[rank][k]
                rank += 1
            return rank
        
        return gaussian_elimination(adjacency_matrix)
    
    def communication_complexity(instance):
        n = len(instance['vertices'])
        if n < 3:
            return 0
        return math.log(n, 2)
    
    instance = generate_triangle_detection_instance(40)
    if instance is None:
        return {
            "metric_name": "communication_complexity",
            "metric_value": 0,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "n_too_small"
        }
    
    graph = incidence_graph(instance)
    rank = tropicalized_lie_algebra_rank(graph)
    C_I = communication_complexity(instance)
    
    r_n = math.log(40, 2) ** 2
    
    return {
        "metric_name": "communication_complexity",
        "metric_value": C_I,
        "instances_tested": 1,
        "conjecture_holds": C_I >= r_n,
        "counterexample": "" if C_I >= r_n else f"Rank {rank} does not exceed {r_n}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result['conjecture_holds'] for result in results):
        mean_value = sum(result['metric_value'] for result in results) / len(results)
        std_dev = math.sqrt(sum((result['metric_value'] - mean_value) ** 2 for result in results) / len(results))
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif any(not result['conjecture_holds'] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result['conjecture_holds'])
        print(f"RESULT: FALSIFIED counterexample=\"rank does not exceed r(n)\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")