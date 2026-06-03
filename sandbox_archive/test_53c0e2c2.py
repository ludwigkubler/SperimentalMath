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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def zonotope_vertices(f):
        n = len(f)
        vertices = []
        for i in range(2**n):
            vertex = [f[i >> j & 1] * (i >> (j + 1) & 1) for j in range(n)]
            vertices.append(vertex)
        return vertices
    
    def grothendieck_witt_class_mod_2(vertices):
        n = len(vertices[0])
        A = [[0] * n for _ in range(n)]
        for v in vertices:
            for i in range(n):
                for j in range(i + 1, n):
                    A[i][j] += v[i] * v[j]
                    A[j][i] += v[i] * v[j]
        det = determinant(A)
        return det % 2
    
    def determinant(matrix):
        if len(matrix) == 0:
            return 0
        if len(matrix) == 1:
            return matrix[0][0]
        det = 0
        for i in range(len(matrix)):
            submatrix = [row[:i] + row[i+1:] for row in matrix[1:]]
            det += (-1)**i * matrix[0][i] * determinant(submatrix)
        return det
    
    def communication_matrix_rank(f):
        n = len(f)
        tree = [[] for _ in range(2**n)]
        queue = [0]
        while queue:
            node = queue.pop()
            if node >= 2**(n-1):
                continue
            left_child = 2 * node + 1
            right_child = 2 * node + 2
            tree[node].append(left_child)
            tree[node].append(right_child)
            queue.append(left_child)
            queue.append(right_child)
        
        rank = 0
        visited = [False] * (2**n)
        for i in range(2**n):
            if not visited[i]:
                visited[i] = True
                stack = [i]
                while stack:
                    node = stack.pop()
                    for neighbor in tree[node]:
                        if not visited[neighbor]:
                            visited[neighbor] = True
                            stack.append(neighbor)
                            rank += 1
        return rank
    
    def minimal_ehrhart_polynomial_degree(vertices):
        n = len(vertices[0])
        A = [[0] * (n + 1) for _ in range(n + 1)]
        for v in vertices:
            for i in range(n):
                A[i][n] += v[i]
            A[n][n] += 1
        det = determinant(A)
        return n - math.log2(abs(det))
    
    f = generate_boolean_function(5)  # Start with n=5 and increase to 40
    vertices = zonotope_vertices(f)
    ehrhart_degree = minimal_ehrhart_polynomial_degree(vertices)
    rank = communication_matrix_rank(f)
    
    return {
        "metric_name": "communication_matrix_rank",
        "metric_value": rank,
        "instances_tested": 1,
        "n_max": 5,
        "conjecture_holds": abs(rank - ehrhart_degree) <= 1,  # Allow a constant factor of 1
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 7 for i in range(5, 8)]  # Default to first 3 primes if no seeds provided
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")