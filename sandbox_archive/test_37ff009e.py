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
        if (n * d) % 2 != 0 or d < 1 or d > n - 1:
            return None
        graph = [[] for _ in range(n)]
        edges = set()
        for i in range(n):
            neighbors = random.sample(range(i + 1, n), d)
            for j in neighbors:
                if (i, j) not in edges and (j, i) not in edges:
                    graph[i].append(j)
                    graph[j].append(i)
                    edges.add((i, j))
        return graph

    def tseitin_formula(graph):
        n = len(graph)
        literals = list(range(1, 2 * n + 1))
        clauses = []
        for i in range(n):
            clauses.append([literals[2 * i], literals[2 * i + 1]])
            for j in graph[i]:
                if j < i:
                    continue
                clauses.append([-literals[2 * i], -literals[2 * j + 1]])
                clauses.append([-literals[2 * i + 1], -literals[2 * j]])
        return literals, clauses

    def gaussian_elimination(matrix):
        n = len(matrix)
        for i in range(n):
            if matrix[i][i] == 0:
                for j in range(i + 1, n):
                    if matrix[j][i] != 0:
                        matrix[i], matrix[j] = matrix[j], matrix[i]
                        break
                else:
                    return None
            pivot = Fraction(matrix[i][i])
            for j in range(n):
                matrix[i][j] /= pivot
            for j in range(n):
                if i == j:
                    continue
                factor = Fraction(matrix[j][i])
                for k in range(n):
                    matrix[j][k] -= factor * matrix[i][k]
        return matrix

    def root_system_length(graph):
        n = len(graph)
        adjacency_matrix = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in graph[i]:
                adjacency_matrix[i][j] = 1
                adjacency_matrix[j][i] = 1
        augmented_matrix = [row + [1] for row in adjacency_matrix]
        rank = len(gaussian_elimination(augmented_matrix))
        return n - rank

    def resolution_proof_width(literals, clauses):
        n = len(literals)
        clause_set = set(clauses)
        proof_length = 0
        while True:
            new_clause = None
            for i in range(n):
                unit_clause = [l for l in literals if l not in clause_set and -l not in clause_set]
                if unit_clause:
                    new_clause = [-unit_clause[0]]
                    break
            if new_clause is None:
                break
            proof_length += 1
            clause_set.add(new_clause)
        return proof_length

    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        graph = generate_d_regular_graph(n, random.randint(2, n - 1))
        if graph is None:
            continue
        literals, clauses = tseitin_formula(graph)
        root_length = root_system_length(graph)
        proof_width = resolution_proof_width(literals, clauses)
        results.append({
            "metric_name": "correlation",
            "metric_value": root_length * proof_width,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        })

    if not all(r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        return {
            "metric_name": "correlation",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(r["n_max"] for r in results),
            "conjecture_holds": False,
            "counterexample": f"first_failing_seed={first_failing_seed}"
        }
    else:
        return {
            "metric_name": "correlation",
            "metric_value": sum(r["metric_value"] for r in results) / len(results),
            "instances_tested": len(results),
            "n_max": max(r["n_max"] for r in results),
            "conjecture_holds": True,
            "counterexample": ""
        }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='first_failing_seed={first_failing_seed}'")