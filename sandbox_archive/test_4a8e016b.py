# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from fractions import Fraction
    from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
import itertools

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def is_connected(graph):
        visited = [False] * len(graph)
        stack = [0]
        while stack:
            node = stack.pop()
            if not visited[node]:
                visited[node] = True
                for neighbor in graph[node]:
                    if not visited[neighbor]:
                        stack.append(neighbor)
        return all(visited)
    
    def matrix_tree_theorem(matrix):
        n = len(matrix)
        det = 0
        for perm in itertools.permutations(range(n)):
            sign = (-1) ** sum(i < j for i, j in enumerate(perm) if perm[i] > perm[j])
            submatrix = [[matrix[i][j] for j in range(n) if j != perm[0]] for i in range(1, n)]
            det += sign * matrix[0][perm[0]]
        return abs(det)
    
    def gaussian_elimination(matrix):
        rows, cols = len(matrix), len(matrix[0])
        for col in range(cols):
            pivot_row = next((i for i in range(col, rows) if matrix[i][col] != 0), None)
            if pivot_row is None:
                continue
            matrix[pivot_row], matrix[col] = matrix[col], matrix[pivot_row]
            for row in range(rows):
                if row == col:
                    continue
                factor = matrix[row][col] / matrix[col][col]
                for j in range(cols):
                    matrix[row][j] -= factor * matrix[col][j]
        return matrix
    
    def rank(matrix):
        matrix = gaussian_elimination(matrix)
        return sum(1 for row in matrix if any(val != 0 for val in row))
    
    def torsion_points_of_order_2(jacobian_matrix):
        n = len(jacobian_matrix)
        jacobian_matrix = [[jacobian_matrix[i][j] % 2 for j in range(n)] for i in range(n)]
        rank_jac = rank(jacobian_matrix)
        return n - rank_jac
    
    def resolution_width(graph):
        n = len(graph)
        clauses = []
        for i in range(n):
            for j in range(i + 1, n):
                if graph[i][j]:
                    clauses.append([(i + 1), -(j + 1)])
                    clauses.append([-(i + 1), (j + 1)])
        def dpll(clauses, assignment, literals):
            if not clauses:
                return True
            literal = next(l for l in literals if l not in assignment)
            pos_literal = abs(literal)
            new_clauses = [c for c in clauses if pos_literal not in c and -pos_literal not in c]
            if dpll(new_clauses, assignment + [(literal, True)], literals):
                return True
            new_clauses = [c for c in clauses if -pos_literal not in c and pos_literal not in c]
            if dpll(new_clauses, assignment + [(literal, False)], literals):
                return True
            return False
        literals = set(abs(l) for clause in clauses for l in clause)
        return max(len([l for l in literals if dpll(clauses, [], [l])]), key=lambda x: x)
    
    def generate_random_graph(n):
        graph = [[0] * n for _ in range(n)]
        edges = set()
        while len(edges) < n - 1:
            u, v = random.sample(range(n), 2)
            if (u, v) not in edges and (v, u) not in edges:
                graph[u][v] = graph[v][u] = 1
                edges.add((u, v))
        return graph
    
    n = random.choice([5, 8, 11, 14])
    graph = generate_random_graph(n)
    if not is_connected(graph):
        return {
            "metric_name": "resolution_width",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "not_connected"
        }
    
    jacobian_matrix = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            if graph[i][j]:
                jacobian_matrix[i][j] = jacobian_matrix[j][i] = 1
    
    tau_G = torsion_points_of_order_2(jacobian_matrix)
    width = resolution_width(graph)
    
    return {
        "metric_name": "resolution_width",
        "metric_value": width,
        "instances_tested": 1,
        "conjecture_holds": width >= tau_G,
        "counterexample": "" if width >= tau_G else f"width={width}, tau(G)={tau_G}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [11, 23, 37, 53, 71]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    metric_values = [r["metric_value"] for r in results if r["metric_value"] is not None]
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={sum(metric_values)/len(metric_values):.2f} std={math.sqrt(sum((x - sum(metric_values)/len(metric_values))**2 for x in metric_values) / len(metric_values)):.2f} support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={sum(metric_values)/len(metric_values):.2f} std={math.sqrt(sum((x - sum(metric_values)/len(metric_values))**2 for x in metric_values) / len(metric_values)):.2f} support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={seeds[first_failing_seed]}")