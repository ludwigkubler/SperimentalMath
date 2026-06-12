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
        if (d * n) % 2 != 0:
            return None
        graph = {i: [] for i in range(n)}
        edges = set()
        while len(edges) < d * n // 2:
            u, v = random.sample(range(n), 2)
            if u != v and (u, v) not in edges and (v, u) not in edges:
                graph[u].append(v)
                graph[v].append(u)
                edges.add((u, v))
        return graph

    def tseitin_formula(graph):
        n = len(graph)
        literals = {i: f"x{i}" for i in range(n)}
        clauses = []
        for u in range(n):
            clauses.append([f"~{literals[u]}"])
            for v in graph[u]:
                clauses.append([f"{literals[u]}", f"~{literals[v]}"])
        return literals, clauses

    def symplectic_form_matrix(clauses):
        n = len(clauses)
        matrix = [[0] * (n + 1) for _ in range(n + 1)]
        for i in range(n):
            matrix[i][i] = -1
            for j in range(i + 1, n):
                if any(l in clauses[j] for l in clauses[i]):
                    matrix[i][j] = 1
                    matrix[j][i] = 1
        return matrix

    def gaussian_elimination(matrix, mod):
        n = len(matrix)
        for i in range(n):
            pivot = i
            while pivot < n and matrix[pivot][i] == 0:
                pivot += 1
            if pivot == n:
                continue
            matrix[i], matrix[pivot] = matrix[pivot], matrix[i]
            for j in range(i + 1, n):
                factor = -matrix[j][i] * pow(matrix[i][i], mod - 2, mod) % mod
                for k in range(n + 1):
                    matrix[j][k] = (matrix[j][k] + factor * matrix[i][k]) % mod
        rank = sum(1 for row in matrix if any(x != 0 for x in row))
        return rank

    def resolution_proof_width(clauses):
        n = len(clauses)
        queue = [clauses]
        while queue:
            clause = queue.pop()
            if not clause:
                continue
            literal = random.choice(clause)
            new_clauses = []
            for c in clauses:
                if literal in c:
                    new_clauses.append([l for l in c if l != literal and l[0] != '~'])
                elif f"~{literal}" in c:
                    new_clauses.append([l for l in c if l != f"~{literal}"])
            queue.extend(new_clauses)
        return len(queue)

    n = random.choice([5, 10, 15, 20, 30, 40])
    d = (n - 1) * 2
    graph = generate_d_regular_graph(n, d)
    if not graph:
        return {
            "metric_name": "sfr_w_ratio",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    literals, clauses = tseitin_formula(graph)
    matrix = symplectic_form_matrix(clauses)
    sfr = gaussian_elimination(matrix, mod=2)
    w = resolution_proof_width(clauses)

    return {
        "metric_name": "sfr_w_ratio",
        "metric_value": sfr / (w + 1e-9) if w != 0 else None,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": abs(sfr / (w + 1e-9) - 1) <= 0.2 * (sfr / (w + 1e-9) + 1),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    if all(r["conjecture_holds"] is not False for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
        support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = "mapping_undefined"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")