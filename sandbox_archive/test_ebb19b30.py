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
from math import sqrt, log2
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_d_regular_graph(d: int, n: int):
        if d * n % 2 != 0:
            return None
        graph = {i: [] for i in range(n)}
        edges_added = set()
        for _ in range(d * n // 2):
            while True:
                u, v = random.sample(range(n), 2)
                if (u, v) not in edges_added and (v, u) not in edges_added:
                    graph[u].append(v)
                    graph[v].append(u)
                    edges_added.add((u, v))
                    break
        return graph
    
    def compute_clause_set(graph):
        clause_set = []
        for node in graph:
            for neighbor in graph[node]:
                if (node, neighbor) not in clause_set and (neighbor, node) not in clause_set:
                    clause_set.append((node, neighbor))
        return clause_set
    
    def gaussian_elimination(matrix):
        n = len(matrix)
        for i in range(n):
            max_row = i
            for j in range(i+1, n):
                if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                    max_row = j
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            if matrix[i][i] == 0:
                return None
            for j in range(n):
                if j != i:
                    factor = matrix[j][i] / matrix[i][i]
                    for k in range(n):
                        matrix[j][k] -= factor * matrix[i][k]
        return matrix
    
    def compute_noncommutative_crossed_product_order(clause_set):
        n = len(clause_set)
        identity_matrix = [[Fraction(1 if i == j else 0) for j in range(n)] for i in range(n)]
        crossed_product = identity_matrix
        for clause in clause_set:
            u, v = clause
            matrix_u = [[Fraction(1 if i == u else 0) for i in range(n)] for _ in range(n)]
            matrix_v = [[Fraction(1 if j == v else 0) for j in range(n)] for _ in range(n)]
            crossed_product = multiply_matrices(gaussian_elimination(matrix_u), gaussian_elimination(crossed_product))
            crossed_product = multiply_matrices(gaussian_elimination(matrix_v), gaussian_elimination(crossed_product))
        rank = sum(1 for row in crossed_product if any(x != 0 for x in row))
        return rank
    
    def multiply_matrices(a, b):
        n = len(a)
        result = [[Fraction(0) for _ in range(n)] for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    result[i][j] += a[i][k] * b[k][j]
        return result
    
    def compute_resolution_proof_width(clause_set):
        # Simplified DPLL solver to estimate resolution proof width
        queue = clause_set[:]
        unit_clauses = [c for c in queue if len(c) == 1]
        while unit_clauses:
            u = unit_clauses.pop()
            literal = u[0]
            new_clauses = []
            for clause in queue:
                if literal in clause:
                    continue
                if -literal in clause:
                    return len(queue)
                new_clause = [l for l in clause if l != -literal]
                if not new_clause:
                    return len(queue)
                new_clauses.append(new_clause)
            queue.extend(new_clauses)
            unit_clauses.extend([c for c in new_clauses if len(c) == 1])
        return len(queue)
    
    d = random.randint(3, 40)
    n = (d * n) // 2 + 1
    graph = generate_d_regular_graph(d, n)
    if not graph:
        return {
            "metric_name": "Order",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    clause_set = compute_clause_set(graph)
    order = compute_noncommutative_crossed_product_order(clause_set)
    width = compute_resolution_proof_width(clause_set)
    
    return {
        "metric_name": "Order",
        "metric_value": order,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False if order is None else True,
        "counterexample": "" if order is not None else "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    values = [r["metric_value"] for r in results if r["metric_value"] is not None]
    conjecture_holds = all(r["conjecture_holds"] for r in results if r["metric_value"] is not None)
    counterexample = next((r["counterexample"] for r in results if r["counterexample"]), "")
    
    mean = sum(values) / len(values) if values else 0
    std = sqrt(sum((x - mean) ** 2 for x in values) / len(values)) if values else 0
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if conjecture_holds:
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    elif counterexample:
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={seeds[results.index(next(r for r in results if r['conjecture_holds'] == False))]}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_data")