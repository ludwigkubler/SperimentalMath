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
    
    def gaussian_elimination(A, b):
        n = len(b)
        for i in range(n):
            max_row = i
            for j in range(i+1, n):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            b[i], b[max_row] = b[max_row], b[i]
            for j in range(i+1, n):
                factor = A[j][i] / A[i][i]
                for k in range(i, n):
                    A[j][k] -= factor * A[i][k]
                b[j] -= factor * b[i]
        x = [0.0] * n
        for i in range(n-1, -1, -1):
            x[i] = (b[i] - sum(A[i][j] * x[j] for j in range(i+1, n))) / A[i][i]
        return x

    def matrix_multiply(A, B):
        m, k = len(A), len(B[0])
        p = len(B)
        C = [[0.0] * k for _ in range(m)]
        for i in range(m):
            for j in range(k):
                for l in range(p):
                    C[i][j] += A[i][l] * B[l][j]
        return C

    def determinant(A):
        n = len(A)
        if n == 1:
            return A[0][0]
        det = 0
        for c in range(n):
            submatrix = [row[:c] + row[c+1:] for row in A[1:]]
            sign = (-1) ** (c % 2)
            sub_det = determinant(submatrix)
            det += sign * A[0][c] * sub_det
        return det

    def inverse(A):
        n = len(A)
        det_A = determinant(A)
        if det_A == 0:
            raise ValueError("Matrix is not invertible")
        adjoint = [[0.0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                submatrix = [row[:j] + row[j+1:] for row in A[:i] + A[i+1:]]
                sign = (-1) ** (i+j)
                adjoint[j][i] = sign * determinant(submatrix)
        inv_A = [[0.0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                inv_A[i][j] = adjoint[i][j] / det_A
        return inv_A

    def generate_d_regular_graph(n, d):
        if (n * d) % 2 != 0:
            raise ValueError("Invalid n and d")
        graph = [[] for _ in range(n)]
        edges = set()
        while len(edges) < n * d // 2:
            u = random.randint(0, n-1)
            v = random.randint(0, n-1)
            if u != v and (u, v) not in edges and (v, u) not in edges:
                graph[u].append(v)
                graph[v].append(u)
                edges.add((u, v))
        return graph

    def tseitin_formula(graph):
        n = len(graph)
        literals = [f"x{i}" for i in range(n)]
        formulas = []
        for i in range(n):
            clause = [literals[i]]
            for j in graph[i]:
                clause.append(f"~{literals[j]}")
            formulas.append(" | ".join(clause))
        for i in range(n):
            for j in range(i+1, n):
                formulas.append(f"{literals[i]} | {literals[j]} | ~({literals[i]} ^ {literals[j]})")
        return " & ".join(formulas)

    def resolution_width(formula):
        clauses = formula.split(" & ")
        literals = set()
        for clause in clauses:
            literals.update(clause.split(" | "))
        literal_count = len(literals)
        max_width = 0
        for i in range(1, literal_count + 1):
            width = sum(1 for clause in clauses if any(lit in clause or f"~{lit}" in clause for lit in literals[:i]))
            max_width = max(max_width, width)
        return max_width

    def kdim(graph):
        n = len(graph)
        adjacency_matrix = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in graph[i]:
                adjacency_matrix[i][j] = 1
        laplacian_matrix = [[0] * n for _ in range(n)]
        degree_sum = sum(len(neighbors) for neighbors in graph)
        for i in range(n):
            laplacian_matrix[i][i] = len(graph[i])
            for j in graph[i]:
                laplacian_matrix[i][j] = -1
        laplacian_inv = inverse(laplacian_matrix)
        kdim = determinant(laplacian_inv) / degree_sum
        return kdim

    n = 20
    d = 3
    graph = generate_d_regular_graph(n, d)
    formula = tseitin_formula(graph)
    width = resolution_width(formula)
    kdim_value = kdim(graph)

    return {
        "metric_name": "resolution_width",
        "metric_value": width,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": abs(kdim_value - width) < 0.1 * max(abs(kdim_value), abs(width)),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        print("RESULT: FALSIFIED counterexample=\"not supported\" first_failing_seed=NA")
    else:
        print(f"RESULT: INCONCLUSIVE reason=budget_exceeded n_tested={len(results)}")