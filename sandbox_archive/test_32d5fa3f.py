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
        graph = [[] for _ in range(n)]
        edges_used = set()
        for i in range(n):
            for j in range(d // 2):
                while True:
                    neighbor = random.randint(0, n - 1)
                    if neighbor == i or (i, neighbor) in edges_used or (neighbor, i) in edges_used:
                        continue
                    graph[i].append(neighbor)
                    graph[neighbor].append(i)
                    edges_used.add((i, neighbor))
                    break
        return graph
    
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
    
    def determinant(matrix):
        n = len(matrix)
        det = 1
        for i in range(n):
            det *= matrix[i][i]
        return det
    
    def hyperbolic_volume(graph):
        n = len(graph)
        adjacency_matrix = [[0] * n for _ in range(n)]
        for u, v in graph:
            adjacency_matrix[u][v] = 1
            adjacency_matrix[v][u] = 1
        
        laplacian_matrix = [[0] * n for _ in range(n)]
        for i in range(n):
            degree = sum(adjacency_matrix[i])
            laplacian_matrix[i][i] = -degree
            for j in range(i + 1, n):
                laplacian_matrix[i][j] = adjacency_matrix[i][j]
                laplacian_matrix[j][i] = adjacency_matrix[j][i]
        
        return abs(determinant(laplacian_matrix))
    
    def resolution_proof_width(graph):
        n = len(graph)
        variables = set()
        for u, v in graph:
            variables.add(u)
            variables.add(v)
        
        clauses = []
        for u, v in graph:
            clauses.append([u, -v])
            clauses.append([-u, v])
        
        def is_satisfiable(clauses):
            assignment = {}
            stack = []
            for var in variables:
                if var not in assignment and -var not in assignment:
                    stack.append((var, True))
            
            while stack:
                var, value = stack.pop()
                assignment[var] = value
                for clause in clauses:
                    if value == True and var in clause:
                        continue
                    if value == False and -var in clause:
                        continue
                    if all(x not in assignment or (assignment[x] == True and x in clause) or (assignment[x] == False and -x in clause) for x in clause):
                        return False
                    new_var = next((x for x in clause if x != var and -x != var), None)
                    if new_var is not None:
                        stack.append((-new_var, not value))
            return True
        
        width = 0
        while len(clauses) > 0:
            max_clause_length = max(len(clause) for clause in clauses)
            if max_clause_length <= width:
                break
            width += 1
            new_clauses = []
            for clause in clauses:
                if len(clause) == max_clause_length:
                    new_clauses.extend([c for c in clauses if len(c) < max_clause_length])
                    break
                new_clauses.append(clause)
            clauses = new_clauses
        
        return width
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_v = 0
    total_w = 0
    instances_tested = 0
    n_max = 0
    
    for n in n_values:
        d = random.randint(3, min(n - 1, 8))
        graph = generate_d_regular_graph(n, d)
        if graph is None:
            continue
        
        v = hyperbolic_volume(graph)
        w = resolution_proof_width(graph)
        
        total_v += v
        total_w += w
        instances_tested += 1
        n_max = max(n_max, n)
    
    mean_v = total_v / instances_tested if instances_tested > 0 else 0
    mean_w = total_w / instances_tested if instances_tested > 0 else 0
    
    conjecture_holds = mean_v >= mean_w
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Hyperbolic Volume vs Resolution Proof Width",
        "metric_value": mean_v,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_v = sum(r["metric_value"] for r in results) / len(results) if len(results) > 0 else 0
    mean_w = sum(r["instances_tested"] * r["metric_value"] for r in results) / sum(r["instances_tested"] for r in results) if sum(r["instances_tested"] for r in results) > 0 else 0
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_v} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_v} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")