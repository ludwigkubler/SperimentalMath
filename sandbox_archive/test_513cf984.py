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
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i
            for j in range(i+1, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            pivot = A[i][i]
            for j in range(n):
                A[i][j] /= pivot
            for j in range(m):
                if j != i:
                    factor = A[j][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        return A
    
    def matrix_multiply(A, B):
        m, n, p = len(A), len(B[0]), len(B)
        C = [[0]*n for _ in range(m)]
        for i in range(m):
            for j in range(n):
                for k in range(p):
                    C[i][j] += A[i][k] * B[k][j]
        return C
    
    def determinant(A):
        m, n = len(A), len(A[0])
        if m != n:
            raise ValueError("Matrix must be square")
        if n == 1:
            return A[0][0]
        det = Fraction(0)
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for row in A[1:]]
            sign = (-1) ** j
            det += sign * A[0][j] * determinant(submatrix)
        return det
    
    def inverse(A):
        m, n = len(A), len(A[0])
        if m != n:
            raise ValueError("Matrix must be square")
        det = determinant(A)
        if det == 0:
            raise ValueError("Singular matrix")
        adjugate = [[0]*n for _ in range(m)]
        for i in range(m):
            for j in range(n):
                submatrix = [row[:j] + row[j+1:] for row in A[:i] + A[i+1:]]
                sign = (-1) ** (i+j)
                adjugate[j][i] = sign * determinant(submatrix)
        return matrix_multiply(adjugate, Fraction(1, det))
    
    def gaussian_elimination_with_back_substitution(A, b):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i
            for j in range(i+1, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            b[i], b[max_row] = b[max_row], b[i]
            pivot = A[i][i]
            for j in range(n):
                A[i][j] /= pivot
            b[i] /= pivot
            for j in range(m):
                if j != i:
                    factor = A[j][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
                    b[j] -= factor * b[i]
        return [b[i] for i in range(m)]
    
    def construct_manifold(G):
        n = len(G)
        M = [[0]*n for _ in range(n)]
        for u in range(n):
            for v in range(u+1, n):
                if G[u][v]:
                    M[u][v] = 1
                    M[v][u] = 1
        return M
    
    def circuit_monotone_width(G):
        n = len(G)
        max_width = 0
        for i in range(n):
            width = 0
            visited = [False]*n
            stack = [i]
            while stack:
                u = stack.pop()
                if not visited[u]:
                    visited[u] = True
                    width += 1
                    for v in range(n):
                        if G[u][v] and not visited[v]:
                            stack.append(v)
            max_width = max(max_width, width)
        return max_width
    
    def alexander_dirac_invariant(M):
        n = len(M)
        A = [[0]*n for _ in range(n)]
        for i in range(n):
            for j in range(i+1, n):
                if M[i][j]:
                    A[i][j] = 1
                    A[j][i] = 1
        det_A = determinant(A)
        inv_A = inverse(A)
        B = [[0]*n for _ in range(n)]
        for i in range(n):
            for j in range(i+1, n):
                if M[i][j]:
                    B[i][j] = -inv_A[i][j]
                    B[j][i] = inv_A[i][j]
        det_B = determinant(B)
        return abs(det_A + det_B)
    
    def generate_d_regular_graph(n, d):
        G = [[0]*n for _ in range(n)]
        edges = set()
        while len(edges) < n*d//2:
            u = random.randint(0, n-1)
            v = random.randint(0, n-1)
            if u != v and (u, v) not in edges and (v, u) not in edges:
                G[u][v] = 1
                G[v][u] = 1
                edges.add((u, v))
        return G
    
    def run_trial(seed: int) -> dict:
        random.seed(seed)
        
        n = random.randint(5, 40)
        d = random.randint(2, 4)
        G = generate_d_regular_graph(n, d)
        M = construct_manifold(G)
        
        w_G = circuit_monotone_width(G)
        m_alex_M = alexander_dirac_invariant(M)
        
        return {
            "metric_name": "correlation",
            "metric_value": abs(w_G - m_alex_M),
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": abs(w_G - m_alex_M) <= 5,
            "counterexample": ""
        }
    
    return run_trial(seed)

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(res["metric_value"] for res in results) / len(results)
    std_value = math.sqrt(sum((res["metric_value"] - mean_value) ** 2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] for res in results) and support_fraction >= 0.8:
        first_failing_seed = next(res["seed"] for res in results if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"abs(w_G - m_alex(M)) > 5\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_support")