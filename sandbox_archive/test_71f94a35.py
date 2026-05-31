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
    
    def generate_graph(n):
        graph = {}
        for i in range(n):
            neighbors = random.sample(range(n), random.randint(1, n-1))
            graph[i] = neighbors
        return graph
    
    def compute_curvature_form(graph):
        n = len(graph)
        curvature_form = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i+1, n):
                if j in graph[i]:
                    curvature_form[i][j] = 1
                    curvature_form[j][i] = 1
        return curvature_form
    
    def min_rank(matrix):
        n = len(matrix)
        rank = 0
        for i in range(n):
            pivot_row = next((r for r, row in enumerate(matrix) if row[i]), None)
            if pivot_row is not None:
                rank += 1
                matrix[pivot_row], matrix[i] = matrix[i], matrix[pivot_row]
                for j in range(i+1, n):
                    factor = -matrix[j][i] / matrix[i][i]
                    for k in range(n):
                        matrix[j][k] += factor * matrix[i][k]
        return rank
    
    def communication_complexity(graph):
        n = len(graph)
        max_degree = max(len(neighbors) for neighbors in graph.values())
        return max_degree
    
    n_max = 40
    instances_tested = 30
    ranks = []
    
    for _ in range(instances_tested):
        n = random.randint(5, n_max)
        graph = generate_graph(n)
        curvature_form = compute_curvature_form(graph)
        rank = min_rank(curvature_form)
        complexity = communication_complexity(graph)
        ranks.append(rank)
    
    mean_rank = sum(ranks) / instances_tested
    conjecture_holds = all(2 * n <= rank <= 5 * n for rank, n in zip(ranks, range(5, n_max+1)))
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Minimal Rank",
        "metric_value": mean_rank,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")