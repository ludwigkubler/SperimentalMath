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
        if d * n % 2 != 0:
            return None
        graph = {i: [] for i in range(n)}
        edges = set()
        while len(edges) < (d * n) // 2:
            u = random.randint(0, n - 1)
            v = random.randint(0, n - 1)
            if u != v and (u, v) not in edges and (v, u) not in edges:
                graph[u].append(v)
                graph[v].append(u)
                edges.add((u, v))
        return graph
    
    def compute_clause_set(graph):
        clause_set = []
        for node in graph:
            neighbors = set(graph[node])
            for neighbor in neighbors:
                for other_neighbor in neighbors - {neighbor}:
                    if (neighbor, other_neighbor) not in graph and (other_neighbor, neighbor) not in graph:
                        clause_set.append((node, neighbor, other_neighbor))
        return clause_set
    
    def gaussian_elimination(matrix):
        n = len(matrix)
        for i in range(n):
            max_row = i
            for j in range(i + 1, n):
                if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                    max_row = j
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            factor = matrix[i][i]
            for j in range(i, n):
                matrix[i][j] /= factor
            for j in range(n):
                if j != i:
                    factor = matrix[j][i]
                    for k in range(i, n):
                        matrix[j][k] -= factor * matrix[i][k]
        return matrix
    
    def compute_noncommutative_crossed_product_order(clause_set):
        n = len(clause_set)
        identity_matrix = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
        crossed_product = identity_matrix
        for clause in clause_set:
            u, v, w = clause
            matrix_uv = [[0] * n for _ in range(n)]
            matrix_uv[u][v] = 1
            matrix_uv[v][u] = 1
            matrix_vw = [[0] * n for _ in range(n)]
            matrix_vw[v][w] = 1
            matrix_vw[w][v] = 1
            crossed_product = multiply_matrices(crossed_product, add_matrices(matrix_uv, matrix_vw))
        reduced_matrix = gaussian_elimination(crossed_product)
        rank = sum(1 for row in reduced_matrix if any(row[i] != 0 for i in range(n)))
        return rank
    
    def compute_resolution_proof_width(clause_set):
        # Simplified DPLL solver to estimate resolution proof width
        def dpll(clauses, assignment):
            if not clauses:
                return True
            unit_clause = next((c for c in clauses if len(c) == 1), None)
            if unit_clause:
                literal = unit_clause[0]
                new_assignment = assignment.copy()
                new_assignment[literal] = True
                if dpll([c for c in clauses if literal not in c and -literal not in c], new_assignment):
                    return True
                new_assignment[literal] = False
                if dpll([c for c in clauses if -literal not in c], new_assignment):
                    return True
                return False
            pure_literal = next((l for l in range(1, max(clause_set) + 1) if (l not in assignment and -l not in assignment)), None)
            if pure_literal is not None:
                new_assignment[pure_literal] = True
                if dpll([c for c in clauses if pure_literal not in c], new_assignment):
                    return True
                new_assignment[pure_literal] = False
                if dpll([c for c in clauses if -pure_literal not in c], new_assignment):
                    return True
                return False
            literal, _ = random.choice(clauses)
            new_assignment[literal] = True
            if dpll([c for c in clauses if literal not in c], new_assignment):
                return True
            new_assignment[literal] = False
            if dpll([c for c in clauses if -literal not in c], new_assignment):
                return True
            return False
        
        def add_clause(clauses, clause):
            if clause not in clauses:
                clauses.append(clause)
        
        def multiply_matrices(A, B):
            n = len(A)
            C = [[0] * n for _ in range(n)]
            for i in range(n):
                for j in range(n):
                    for k in range(n):
                        C[i][j] += A[i][k] * B[k][j]
            return C
        
        def add_matrices(A, B):
            n = len(A)
            C = [[0] * n for _ in range(n)]
            for i in range(n):
                for j in range(n):
                    C[i][j] = A[i][j] + B[i][j]
            return C
        
        clauses = []
        assignment = {}
        for clause in clause_set:
            add_clause(clauses, clause)
        if dpll(clauses, assignment):
            return 0
        else:
            return len(clause_set) * 2
    
    def pearson_correlation(x, y):
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        cov_xy = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n)) / n
        std_x = math.sqrt(sum((x[i] - mean_x) ** 2 for i in range(n)) / n)
        std_y = math.sqrt(sum((y[i] - mean_y) ** 2 for i in range(n)) / n)
        return cov_xy / (std_x * std_y)
    
    results = []
    for _ in range(30):
        d = random.randint(1, 40)
        n = random.randint(d + 1, 40)
        graph = generate_d_regular_graph(d, n)
        if graph is None:
            continue
        clause_set = compute_clause_set(graph)
        order = compute_noncommutative_crossed_product_order(clause_set)
        width = compute_resolution_proof_width(clause_set)
        results.append((order, width))
    
    if len(results) < 30:
        return {
            "metric_name": "Pearson Correlation",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(n for _, _ in results),
            "conjecture_holds": False,
            "counterexample": "Too few valid graphs generated"
        }
    
    x = [r[0] for r in results]
    y = [r[1] for r in results]
    correlation = pearson_correlation(x, y)
    
    return {
        "metric_name": "Pearson Correlation",
        "metric_value": correlation,
        "instances_tested": len(results),
        "n_max": max(n for _, _ in results),
        "conjecture_holds": abs(correlation) > 0.5,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] + list(range(31, 100))
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
        support_fraction = len([r for r in results if r["conjecture_holds"]]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Pearson correlation does not support the conjecture\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE No seeds supported the conjecture")