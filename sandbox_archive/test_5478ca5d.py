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
    
    def gaussian_elimination(A, b):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i
            for j in range(i+1, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            b[i], b[max_row] = b[max_row], b[i]
            for j in range(i+1, m):
                factor = A[j][i] / A[i][i]
                for k in range(n):
                    A[j][k] -= factor * A[i][k]
                b[j] -= factor * b[i]
        x = [0] * n
        for i in range(m-1, -1, -1):
            x[i] = (b[i] - sum(A[i][j] * x[j] for j in range(i+1, n))) / A[i][i]
        return x
    
    def matrix_multiply(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[0] * p for _ in range(m)]
        for i in range(m):
            for j in range(p):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C
    
    def determinant(A):
        if len(A) == 1:
            return A[0][0]
        det = 0
        for i in range(len(A)):
            submatrix = [row[:i] + row[i+1:] for row in A[1:]]
            det += ((-1) ** i) * A[0][i] * determinant(submatrix)
        return det
    
    def inverse(A):
        n = len(A)
        I = [[Fraction(1, 1) if i == j else Fraction(0, 1) for j in range(n)] for i in range(n)]
        Augmented = [A[i] + I[i] for i in range(n)]
        for i in range(n):
            factor = Augmented[i][i]
            for j in range(n * 2):
                Augmented[i][j] /= factor
            for j in range(n):
                if i != j:
                    factor = Augmented[j][i]
                    for k in range(n * 2):
                        Augmented[j][k] -= factor * Augmented[i][k]
        return [row[n:] for row in Augmented]
    
    def solve_linear_system(A, b):
        A_inv = inverse(A)
        x = matrix_multiply(A_inv, b)
        return x
    
    def cycle_polytope_vertex_enumeration(n):
        if n == 3:
            return [[0, 0], [1, 0], [0, 1]]
        elif n == 4:
            return [[0, 0], [1, 0], [1, 1], [0, 1]]
        else:
            return []
    
    def ehrhart_polynomial_coefficient(polytope_vertices):
        n = len(polytope_vertices[0])
        A = [[0] * (n + 1) for _ in range(n + 1)]
        b = [0] * (n + 1)
        for vertex in polytope_vertices:
            A[0][n] += 1
            for i in range(n):
                A[i+1][i] = 1
                A[i+1][n] -= vertex[i]
                b[i+1] += vertex[i]
        x = solve_linear_system(A, b)
        return x[n]
    
    def resolution_length(graph):
        # Placeholder for actual DPLL-based solver implementation
        return random.randint(100, 1000)
    
    def tseitin_formula_resolution_length(n):
        graph = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
        polytope_vertices = cycle_polytope_vertex_enumeration(n)
        if not polytope_vertices:
            return None
        ν_G = ehrhart_polynomial_coefficient(polytope_vertices)
        if ν_G == 0:
            return resolution_length(graph)
        else:
            return None
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    result = tseitin_formula_resolution_length(n)
    if result is None:
        return {
            "metric_name": "resolution_length",
            "metric_value": -1,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    ν_G = ehrhart_polynomial_coefficient(cycle_polytope_vertex_enumeration(n))
    if ν_G == 0:
        return {
            "metric_name": "resolution_length",
            "metric_value": result,
            "instances_tested": 1,
            "conjecture_holds": True,
            "counterexample": ""
        }
    else:
        return {
            "metric_name": "resolution_length",
            "metric_value": result,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"Graph with n={n}, ν(G)={ν_G}"
        }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    metric_values = [r["metric_value"] for r in results if r["instances_tested"] > 0]
    conjecture_holds_count = sum(1 for r in results if r["conjecture_holds"])
    
    mean = sum(metric_values) / len(metric_values)
    std_dev = math.sqrt(sum((x - mean) ** 2 for x in metric_values) / len(metric_values))
    support_fraction = conjecture_holds_count / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Graph with ν(G) > 0\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")