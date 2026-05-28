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
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_k_clique(n, k):
        vertices = list(range(n))
        edges = []
        for _ in range(k):
            clique = random.sample(vertices, 2)
            if clique not in edges and (clique[1], clique[0]) not in edges:
                edges.append(clique)
        return vertices, edges
    
    def incidence_variety(vertices, edges):
        n = len(vertices)
        m = len(edges)
        incidence_matrix = [[0] * m for _ in range(n)]
        for i, (u, v) in enumerate(edges):
            incidence_matrix[u][i] = 1
            incidence_matrix[v][i] = 1
        return incidence_matrix
    
    def gaussian_elimination(matrix):
        n, m = len(matrix), len(matrix[0])
        rank = 0
        for i in range(n):
            if all(matrix[i][j] == 0 for j in range(m)):
                continue
            pivot_col = matrix[i].index(1)
            rank += 1
            for j in range(i + 1, n):
                if matrix[j][pivot_col] == 1:
                    for k in range(m):
                        matrix[j][k] ^= matrix[i][k]
        return rank
    
    def min_rank_of_hodge_structure(n, k):
        vertices, edges = generate_k_clique(n, k)
        incidence_matrix = incidence_variety(vertices, edges)
        return gaussian_elimination(incidence_matrix)
    
    n_values = [5, 10, 15, 20, 30, 40]
    ranks = []
    for n in n_values:
        for _ in range(5):
            rank = min_rank_of_hodge_structure(n, k)
            if rank is None:
                return {
                    "metric_name": "min_rank",
                    "metric_value": None,
                    "instances_tested": 0,
                    "conjecture_holds": False,
                    "counterexample": "mapping_undefined"
                }
            ranks.append(rank)
    
    mean_rank = sum(ranks) / len(ranks)
    std_rank = math.sqrt(sum((x - mean_rank) ** 2 for x in ranks) / len(ranks))
    support_fraction = Fraction(len([r for r in ranks if r >= n**2 * math.log(k)]), len(ranks))
    
    conjecture_holds = support_fraction > Fraction(95, 100)
    counterexample = "" if conjecture_holds else "mean_rank < n^2 log k"
    
    return {
        "metric_name": "min_rank",
        "metric_value": mean_rank,
        "instances_tested": len(ranks),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_rank = math.sqrt(sum((r["metric_value"] - mean_rank) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["metric_value"] is not None for r in results):
        if support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
        elif support_fraction > 0.5:
            print(f"RESULT: FALSIFIED counterexample=\"mean_rank < n^2 log k\" first_failing_seed={seeds[next(i for i, r in enumerate(results) if not r['conjecture_holds'])]}")
        else:
            print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")
    else:
        print("RESULT: INCONCLUSIVE some trials returned None")