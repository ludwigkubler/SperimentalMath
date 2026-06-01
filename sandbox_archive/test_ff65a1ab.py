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
    
    def generate_d_regular_graph(n, d):
        if (n * d) % 2 != 0:
            return None
        graph = {i: [] for i in range(n)}
        edges = set()
        while len(edges) < n * d // 2:
            u, v = random.sample(range(n), 2)
            if u not in graph[v] and v not in graph[u]:
                graph[u].append(v)
                graph[v].append(u)
                edges.add((u, v))
                edges.add((v, u))
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
            for j in range(i + 1, n):
                for k in range(j + 1, n):
                    if (i, j) not in graph and (j, k) not in graph and (k, i) not in graph:
                        clause = [f'-{literals[i]}', f'-{literals[j]}', f'-{literals[k]}']
                        clauses.append(clause)
        return clauses
    
    def frege_proof_size(clauses):
        size = 0
        for clause in clauses:
            size += len(clause) + 1
        return size
    
    def symplectic_form(graph):
        n = len(graph)
        if n == 0:
            return 0
        matrix = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in graph[i]:
                matrix[i][j] = 1
                matrix[j][i] = 1
        det = determinant(matrix)
        if det == 0:
            return 0
        return abs(det) ** (1 / n)
    
    def determinant(matrix):
        n = len(matrix)
        if n == 1:
            return matrix[0][0]
        det = 0
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for row in matrix[1:]]
            det += (-1) ** j * matrix[0][j] * determinant(submatrix)
        return det
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        graph = generate_d_regular_graph(n, 3)
        if graph is None:
            continue
        clauses = tseitin_formula(graph)
        proof_size = frege_proof_size(clauses)
        symplectic = symplectic_form(graph)
        results.append((symplectic, proof_size))
    
    if len(results) < 30:
        return {
            "metric_name": "Pearson correlation",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "not_enough_instances"
        }
    
    symplectic = [r[0] for r in results]
    proof_size = [r[1] for r in results]
    mean_symplectic = sum(symplectic) / len(symplectic)
    mean_proof_size = sum(proof_size) / len(proof_size)
    covariance = sum((symplectic[i] - mean_symplectic) * (proof_size[i] - mean_proof_size) for i in range(len(symplectic)))
    variance_symplectic = sum((symplectic[i] - mean_symplectic) ** 2 for i in range(len(symplectic))) / len(symplectic)
    variance_proof_size = sum((proof_size[i] - mean_proof_size) ** 2 for i in range(len(proof_size))) / len(proof_size)
    correlation = covariance / math.sqrt(variance_symplectic * variance_proof_size)
    
    return {
        "metric_name": "Pearson correlation",
        "metric_value": correlation,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": correlation > 0.7,
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
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='not_enough_support' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")