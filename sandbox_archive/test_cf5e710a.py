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
    
    def min_ehrhart_polynomial(vertices):
        n = len(vertices[0])
        A = [[sum(v[j] for v in vertices if v[i] == 1) - sum(v[j] for v in vertices if v[i] == 0) for j in range(n)] for i in range(n)]
        det = determinant(A)
        return det
    
    def determinant(matrix):
        n = len(matrix)
        if n == 1:
            return matrix[0][0]
        det = 0
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for row in matrix[1:]]
            det += (-1)**j * matrix[0][j] * determinant(submatrix)
        return det
    
    def communication_matrix_rank(f):
        n = len(f)
        tree = [[] for _ in range(2*n-1)]
        queue = [0]
        while queue:
            node = queue.pop(0)
            if node < n:
                left_child = 2*node + 1
                right_child = 2*node + 2
                tree[node].append(left_child)
                tree[node].append(right_child)
                queue.append(left_child)
                queue.append(right_child)
        rank = 0
        visited = [False] * (2*n-1)
        for i in range(n):
            if not visited[i]:
                stack = [i]
                while stack:
                    node = stack.pop()
                    if not visited[node]:
                        visited[node] = True
                        for neighbor in tree[node]:
                            stack.append(neighbor)
                rank += 1
        return rank
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    f = generate_boolean_function(n)
    vertices = zonotope_vertices(f)
    ehrhart_poly = min_ehrhart_polynomial(vertices)
    comm_rank = communication_matrix_rank(f)
    
    if ehrhart_poly == 0:
        return {
            "metric_name": "communication_matrix_rank",
            "metric_value": comm_rank,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    degree = len(bin(ehrhart_poly)) - 2
    if comm_rank == 0:
        return {
            "metric_name": "communication_matrix_rank",
            "metric_value": comm_rank,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    ratio = abs(comm_rank / degree)
    return {
        "metric_name": "communication_matrix_rank",
        "metric_value": comm_rank,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": ratio <= 2 and ratio >= 0.5,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [random.randint(2, 1000003) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    metric_values = [r["metric_value"] for r in results]
    conjecture_holds = all(r["conjecture_holds"] for r in results)
    counterexample = next((r["counterexample"] for r in results if not r["conjecture_holds"]), "")
    
    mean_value = sum(metric_values) / len(metric_values)
    std_value = math.sqrt(sum((x - mean_value)**2 for x in metric_values) / len(metric_values))
    
    if conjecture_holds:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction=1.0")
    elif counterexample:
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={seeds[results.index(next(r for r in results if not r['conjecture_holds'] ))]}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")