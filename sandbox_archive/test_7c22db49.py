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
        if n % d != 0:
            raise ValueError("Graph size must be a multiple of the degree")
        graph = [[] for _ in range(n)]
        edges_added = set()
        for i in range(d * n // 2):
            while True:
                u = random.randint(0, n - 1)
                v = random.randint(0, n - 1)
                if u == v or (u, v) in edges_added or (v, u) in edges_added:
                    continue
                graph[u].append(v)
                graph[v].append(u)
                edges_added.add((u, v))
                break
        return graph

    def topological_entropy(graph):
        n = len(graph)
        adjacency_matrix = [[0] * n for _ in range(n)]
        for u in range(n):
            for v in graph[u]:
                adjacency_matrix[u][v] = 1
        
        # Gaussian elimination to find the rank of the matrix
        def gaussian_elimination(matrix):
            rows, cols = len(matrix), len(matrix[0])
            rank = 0
            for col in range(cols):
                pivot_row = -1
                for row in range(rank, rows):
                    if matrix[row][col] != 0:
                        pivot_row = row
                        break
                if pivot_row == -1:
                    continue
                matrix[pivot_row], matrix[rank] = matrix[rank], matrix[pivot_row]
                rank += 1
                for row in range(rank, rows):
                    factor = matrix[row][col] / matrix[pivot_row][col]
                    for j in range(cols):
                        matrix[row][j] -= factor * matrix[pivot_row][j]
            return rank
        
        rank = gaussian_elimination(adjacency_matrix)
        return math.log2(n) - math.log2(rank)

    def resolution_proof_width(graph):
        n = len(graph)
        clauses = []
        for u in range(n):
            clause = [i + 1 if i != u else -u for i in graph[u]]
            clauses.append(clause)
        
        # Resolution algorithm to find the width
        def resolve(clauses, literals):
            new_clauses = []
            for literal in literals:
                for clause in clauses:
                    if literal in clause:
                        continue
                    neg_literal = -literal
                    if neg_literal in clause:
                        new_clause = [l for l in clause if l != neg_literal]
                        if new_clause not in new_clauses:
                            new_clauses.append(new_clause)
                    else:
                        new_clauses.append(clause)
            return new_clauses
        
        width = 0
        while clauses:
            literals = set()
            for clause in clauses:
                literals.update(abs(l) for l in clause)
            literals = list(literals)
            if len(literals) > width:
                width = len(literals)
            clauses = resolve(clauses, literals)
        
        return width

    n_max = 40
    instances_tested = 30
    h_values = []
    w_values = []

    for _ in range(instances_tested):
        n = random.randint(5, n_max)
        d = random.randint(2, min(n - 1, 4))
        graph = generate_d_regular_graph(n, d)
        h = topological_entropy(graph)
        w = resolution_proof_width(graph)
        h_values.append(h)
        w_values.append(w)

    correlation_coefficient = sum((h_values[i] - sum(h_values) / instances_tested) * (w_values[i] - sum(w_values) / instances_tested) for i in range(instances_tested)) / (instances_tested * math.sqrt(sum((h_values[i] - sum(h_values) / instances_tested) ** 2 for i in range(instances_tested)) * sum((w_values[i] - sum(w_values) / instances_tested) ** 2 for i in range(instances_tested))))

    conjecture_holds = correlation_coefficient >= 0.7
    counterexample = "" if conjecture_holds else "correlation_coefficient < 0.7"

    return {
        "metric_name": "Pearson Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [random.randint(2, 1000000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...{result}...}}")
        results.append(result)

    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] and r["metric_value"] < 0.5 for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"] and r["metric_value"] < 0.5)
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient < 0.7\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction} < 80%")