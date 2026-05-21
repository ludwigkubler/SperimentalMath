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
    
    def generate_abp(w, n):
        nodes = list(range(n))
        edges = []
        for i in range(1, w + 1):
            for j in range(i):
                edges.append((random.choice(nodes[:i]), random.choice(nodes[i:])))
        return nodes, edges
    
    def matrix_multiply(A, B):
        m, k = len(A), len(B[0])
        n = len(B)
        C = [[0] * k for _ in range(m)]
        for i in range(m):
            for j in range(k):
                for l in range(n):
                    C[i][j] += A[i][l] * B[l][j]
        return C
    
    def gaussian_elimination(A, b):
        m, n = len(A), len(A[0])
        augmented_matrix = [A[i] + [b[i]] for i in range(m)]
        for i in range(n):
            max_row = i
            for j in range(i + 1, m):
                if abs(augmented_matrix[j][i]) > abs(augmented_matrix[max_row][i]):
                    max_row = j
            augmented_matrix[i], augmented_matrix[max_row] = augmented_matrix[max_row], augmented_matrix[i]
            pivot = augmented_matrix[i][i]
            for j in range(i, n + 1):
                augmented_matrix[i][j] /= pivot
            for j in range(m):
                if j != i:
                    factor = augmented_matrix[j][i]
                    for k in range(i, n + 1):
                        augmented_matrix[j][k] -= factor * augmented_matrix[i][k]
        return [row[-1] for row in augmented_matrix[:n]]
    
    def partial_derivatives(f, x, y):
        df_dx = (f(x + 1e-6, y) - f(x - 1e-6, y)) / (2 * 1e-6)
        df_dy = (f(x, y + 1e-6) - f(x, y - 1e-6)) / (2 * 1e-6)
        return df_dx, df_dy
    
    def castelnuovo_mumford_regularity(f, x, y):
        df_dx, df_dy = partial_derivatives(f, x, y)
        I = [[df_dx], [df_dy]]
        b = [0, 0]
        return len(gaussian_elimination(I, b))
    
    def abp_width(nodes, edges):
        visited = set()
        stack = []
        for node in nodes:
            if node not in visited:
                stack.append(node)
                while stack:
                    current = stack.pop()
                    if current not in visited:
                        visited.add(current)
                        for neighbor in [edge[1] for edge in edges if edge[0] == current]:
                            if neighbor not in visited:
                                stack.append(neighbor)
        return len(visited)
    
    def f(x, y):
        return x**2 + 3*x*y + y**2
    
    n = random.randint(5, 40)
    w = random.randint(1, 10)
    nodes, edges = generate_abp(w, n)
    reg_I = castelnuovo_mumford_regularity(f, 1, 1)
    abp_w = abp_width(nodes, edges)
    
    return {
        "metric_name": "castelnuovo_mumford_regularity",
        "metric_value": reg_I,
        "instances_tested": 1,
        "conjecture_holds": reg_I <= w * math.log(n) + 10,
        "counterexample": "" if reg_I <= w * math.log(n) + 10 else f"reg(I) = {reg_I}, expected ≤ {w * math.log(n) + 10}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 35)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{'seed': {seed}, 'metric_name': '{result['metric_name']}', 'metric_value': {result['metric_value']}, 'instances_tested': {result['instances_tested']}, 'conjecture_holds': {result['conjecture_holds']}, 'counterexample': '{result['counterexample']}'}}")
        results.append(result)
    
    mean_reg_I = sum(r["metric_value"] for r in results) / len(results)
    std_reg_I = math.sqrt(sum((r["metric_value"] - mean_reg_I) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_reg_I} std={std_reg_I} support_fraction={support_fraction}")
    elif any(r["counterexample"]):
        print(f"RESULT: FALSIFIED counterexample=\"{results[results.index(next(filter(lambda r: r['counterexample'], results), default=None))]['counterexample']}\" first_failing_seed={seeds[results.index(next(filter(lambda r: r['counterexample'], results), default=None))]}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")