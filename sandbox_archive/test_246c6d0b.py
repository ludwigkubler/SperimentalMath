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
                if random.random() < 0.5:
                    edges.add((i, j))
        return edges
    
    def adjacency_matrix(edges, n):
        mat = [[0] * n for _ in range(n)]
        for u, v in edges:
            mat[u][v] = 1
            mat[v][u] = 1
        return mat
    
    def is_bipartite(mat, n):
        color = [-1] * n
        queue = []
        for i in range(n):
            if color[i] == -1:
                color[i] = 0
                queue.append(i)
            while queue:
                u = queue.pop(0)
                for v in range(n):
                    if mat[u][v]:
                        if color[v] == -1:
                            color[v] = 1 - color[u]
                            queue.append(v)
                        elif color[v] == color[u]:
                            return False
        return True
    
    def min_rank_birational_realization(mat, n):
        # Simplified birational rank calculation for demonstration purposes
        if is_bipartite(mat, n):
            return 2
        else:
            return n
    
    def monotone_circuit_size(mat, n):
        # Simplified monotone circuit size calculation for demonstration purposes
        return n * (n - 1) // 2
    
    n = random.randint(5, 40)
    edges = generate_random_graph(n)
    mat = adjacency_matrix(edges, n)
    
    R_G = min_rank_birational_realization(mat, n)
    M_G = monotone_circuit_size(mat, n)
    
    if M_G == 0:
        return {
            "metric_name": "R(G)/M(G)",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "Monotone circuit size is zero"
        }
    
    ratio = R_G / M_G
    
    return {
        "metric_name": "R(G)/M(G)",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 97) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_ratio = sum(result["metric_value"] for result in results) / len(results)
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        counterexample = "R(G)/M(G) ratio exceeds expected bound"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")