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
                if random.choice([True, False]):
                    edges.add((i, j))
        return edges
    
    def graph_to_cnf(graph, n):
        cnf = []
        for i in range(n):
            clause = [-j - 1 for j in range(1, n + 1) if (i, j - 1) not in graph]
            cnf.append(clause)
        return cnf
    
    def gaussian_elimination(matrix):
        rows, cols = len(matrix), len(matrix[0])
        rank = 0
        for i in range(cols):
            max_row = None
            for r in range(rank, rows):
                if matrix[r][i] != 0:
                    max_row = r
                    break
            if max_row is not None:
                matrix[rank], matrix[max_row] = matrix[max_row], matrix[rank]
                pivot = matrix[rank][i]
                for j in range(i, cols):
                    matrix[rank][j] /= pivot
                for r in range(rows):
                    if r != rank and matrix[r][i] != 0:
                        factor = matrix[r][i]
                        for j in range(i, cols):
                            matrix[r][j] -= factor * matrix[rank][j]
                rank += 1
        return rank
    
    def min_depth_of_tree(cnf):
        n = len(cnf)
        graph = generate_random_graph(n)
        cnf = graph_to_cnf(graph, n)
        matrix = [[0 for _ in range(len(cnf))] for _ in range(len(cnf))]
        for i in range(len(cnf)):
            for j in range(i + 1, len(cnf)):
                if (i, j) in graph or (j, i) in graph:
                    matrix[i][j] = 1
                    matrix[j][i] = 1
        return gaussian_elimination(matrix)
    
    n = random.randint(5, 40)
    graph = generate_random_graph(n)
    cnf = graph_to_cnf(graph, n)
    rank = gaussian_elimination(cnf)
    depth = min_depth_of_tree(cnf)
    
    return {
        "metric_name": "Rank vs Depth",
        "metric_value": abs(rank - math.log2(n)),
        "instances_tested": 1,
        "conjecture_holds": abs(rank - math.log2(n)) <= 3 * math.log2(n),
        "counterexample": f"n={n}, rank={rank}, depth={depth}" if not conjecture_holds else ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 10**9) for _ in range(30)]
    
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
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")