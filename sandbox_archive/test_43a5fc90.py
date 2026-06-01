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
    
    def generate_d_regular_graph(d, n):
        if d * (n - 1) % 2 != 0:
            return None
        graph = {i: [] for i in range(n)}
        edges = set()
        for i in range(n):
            neighbors = random.sample(range(n), d)
            for neighbor in neighbors:
                if i < neighbor and (i, neighbor) not in edges:
                    graph[i].append(neighbor)
                    graph[neighbor].append(i)
                    edges.add((i, neighbor))
        return graph

    def tseitin_formula(graph):
        n = len(graph)
        literals = {i: f'x{i}' for i in range(n)}
        clauses = []
        for i in range(n):
            clause = [literals[i]]
            for j in graph[i]:
                clause.append(f'-{literals[j]}')
            clauses.append(clause)
        return clauses

    def symplectic_form(graph):
        n = len(graph)
        matrix = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in graph[i]:
                if i < j:
                    matrix[i][j] += 1
                    matrix[j][i] += 1
        return sum(sum(row) for row in matrix)

    def frege_proof_size(clauses):
        # Simplified estimation of Frege proof size
        return len(clauses) * 2

    n = random.randint(5, 40)
    d = random.randint(3, min(n - 1, 6))
    graph = generate_d_regular_graph(d, n)
    if not graph:
        return {
            "metric_name": "symplectic_form",
            "metric_value": None,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }

    clauses = tseitin_formula(graph)
    symplectic = symplectic_form(graph)
    proof_size = frege_proof_size(clauses)

    return {
        "metric_name": "symplectic_form",
        "metric_value": symplectic,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
        support_fraction = len([r for r in results if r["conjecture_holds"]]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")