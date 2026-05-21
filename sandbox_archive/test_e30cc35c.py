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
    
    def gaussian_elimination(matrix):
        rows, cols = len(matrix), len(matrix[0])
        for i in range(rows):
            max_row = i + max(range(i, rows), key=lambda r: abs(matrix[r][i]))
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            if matrix[i][i] == 0:
                return None
            for j in range(cols):
                matrix[i][j] /= matrix[i][i]
            for k in range(rows):
                if k != i and matrix[k][i] != 0:
                    factor = matrix[k][i]
                    for j in range(cols):
                        matrix[k][j] -= factor * matrix[i][j]
        return matrix

    def build_complex(assignment):
        vertices = set()
        edges = []
        triangles = []
        
        for clause in assignment:
            literals = [abs(lit) for lit in clause if lit != 0]
            vertices.update(literals)
            
            for i in range(len(literals)):
                for j in range(i + 1, len(literals)):
                    edge = tuple(sorted((literals[i], literals[j])))
                    edges.append(edge)
                    
                    for k in range(j + 1, len(literals)):
                        triangle = tuple(sorted((literals[i], literals[j], literals[k])))
                        triangles.append(triangle)
        
        return vertices, edges, triangles

    def compute_beta_1(vertices, edges, triangles):
        V, E = len(vertices), len(edges)
        beta_0 = 1
        boundary_matrix = [[0] * (E + len(triangles)) for _ in range(E)]
        
        edge_index = {edge: i for i, edge in enumerate(edges)}
        triangle_index = {triangle: i + E for i, triangle in enumerate(triangles)}
        
        for edge in edges:
            boundary_matrix[edge_index[edge]][triangle_index[(edge[0], edge[1], None)]] = 1
            boundary_matrix[edge_index[edge]][triangle_index[(None, edge[0], edge[1])]] = 1
        
        rank_boundary_2 = gaussian_elimination(boundary_matrix)
        if rank_boundary_2 is None:
            return -1
        
        beta_1 = E - V + beta_0 - sum(1 for row in rank_boundary_2 if any(x != 0 for x in row))
        return beta_1

    def dpll(clauses, assignment):
        if not clauses:
            return assignment
        literal = next(lit for lit in range(1, max(abs(c) for c in sum(clauses, [])) + 1) if lit not in [abs(c) for c in assignment])
        new_assignment = assignment[:]
        new_assignment.append(literal)
        if all([any(lit in clause or -lit in clause for clause in clauses) for lit in new_assignment]):
            result = dpll(clauses, new_assignment)
            if result:
                return result
        new_assignment.pop()
        new_assignment.append(-literal)
        if all([any(lit in clause or -lit in clause for clause in clauses) for lit in new_assignment]):
            result = dpll(clauses, new_assignment)
            if result:
                return result
        return None

    n = random.choice([3, 4, 5])
    clauses = [random.sample(range(-n, n + 1), k=random.randint(2, n)) for _ in range(n * (n - 1) // 2)]
    assignment = []
    
    refutation = dpll(clauses, assignment)
    if not refutation:
        return {
            "metric_name": "beta_1",
            "metric_value": -1,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "DPLL did not find a refutation"
        }
    
    vertices, edges, triangles = build_complex(refutation)
    beta_1 = compute_beta_1(vertices, edges, triangles)
    
    if beta_1 < 0:
        return {
            "metric_name": "beta_1",
            "metric_value": -1,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "Gaussian elimination failed"
        }
    
    metric_value = beta_1 / len(refutation)
    
    return {
        "metric_name": "beta_1",
        "metric_value": beta_1,
        "instances_tested": 1,
        "conjecture_holds": beta_1 >= math.floor(n * math.log2(n + 1)),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(3, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result["metric_value"])
    
    mean_metric_value = sum(results) / len(results)
    variance_metric_value = sum((x - mean_metric_value)**2 for x in results) / len(results)
    support_fraction = sum(1 for r in results if r >= math.floor(n * math.log2(n + 1))) / len(results)
    
    if all(r >= math.floor(n * math.log2(n + 1)) for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value:.4f} std={variance_metric_value:.4f} support_fraction={support_fraction:.4f}")
    elif any(r < math.floor(n * math.log2(n + 1)) for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if result < math.floor(n * math.log2(n + 1)))
        print(f"RESULT: FALSIFIED counterexample='beta_1 < n*log2(n+1)' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unsupported_operation")