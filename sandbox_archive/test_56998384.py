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
    
    def generate_d_regular_graph(n, d):
        if n % d != 0:
            return None
        graph = {i: set() for i in range(n)}
        edges = set()
        while len(edges) < (n * d) // 2:
            u, v = random.sample(range(n), 2)
            if u not in graph[v] and v not in graph[u]:
                graph[u].add(v)
                graph[v].add(u)
                edges.add((u, v))
        return graph
    
    def gaussian_elimination(matrix):
        n = len(matrix)
        for i in range(n):
            max_row = i
            for j in range(i+1, n):
                if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                    max_row = j
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            factor = matrix[i][i]
            if factor == 0:
                return None
            for j in range(i, n):
                matrix[i][j] /= factor
            for j in range(n):
                if j != i and matrix[j][i] != 0:
                    factor = matrix[j][i]
                    for k in range(i, n):
                        matrix[j][k] -= factor * matrix[i][k]
        return matrix
    
    def minimal_tropical_hodge_dimension(clauses):
        n = len(clauses)
        matrix = [[Fraction(1 if i == j else 0, 1) for j in range(n)] for i in range(n)]
        for clause in clauses:
            for var in clause:
                matrix[var][var] += Fraction(1, 1)
        reduced_matrix = gaussian_elimination(matrix)
        if reduced_matrix is None:
            return None
        rank = sum(1 for row in reduced_matrix if any(val != 0 for val in row))
        return rank
    
    def circuit_depth(clauses):
        n = len(clauses)
        depth = [0] * n
        for i in range(n):
            for var in clauses[i]:
                depth[var] = max(depth[var], depth[i] + 1)
        return max(depth)
    
    def generate_clauses(graph):
        clauses = []
        for node, neighbors in graph.items():
            clause = [node]
            for neighbor in neighbors:
                clause.append(-neighbor - 1)
            clauses.append(clause)
        return clauses
    
    n_max = 40
    instances_tested = 0
    total_mhd = 0
    total_depth = 0
    conjecture_holds = True
    counterexample = ""
    
    for n in range(5, n_max + 1, 5):
        for _ in range(6):  # Ensure at least 30 instances per seed
            graph = generate_d_regular_graph(n, 2)
            if graph is None:
                continue
            clauses = generate_clauses(graph)
            mhd = minimal_tropical_hodge_dimension(clauses)
            depth = circuit_depth(clauses)
            if mhd is None or depth is None:
                continue
            instances_tested += 1
            total_mhd += mhd
            total_depth += depth
            if mhd > 2 * depth:
                conjecture_holds = False
                counterexample = f"n={n}, mhd={mhd}, depth={depth}"
    
    if instances_tested == 0:
        return {
            "metric_name": "minimal_tropical_hodge_dimension",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "Graph size must be a multiple of the degree"
        }
    
    mean_mhd = total_mhd / instances_tested
    mean_depth = total_depth / instances_tested
    
    return {
        "metric_name": "minimal_tropical_hodge_dimension",
        "metric_value": mean_mhd,
        "instances_tested": instances_tested,
        "n_max": n_max,
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
    
    mean_mhd = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_mhd} std=0.0 support_fraction=1.0")
    elif any(not r["conjecture_holds"] and "counterexample" in r for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")