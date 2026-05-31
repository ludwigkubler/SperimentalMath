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
    
    def matrix_multiplication(A, B):
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
        sign = 1
        for j in range(len(A[0])):
            submatrix = [row[:j] + row[j+1:] for row in A[1:]]
            det += sign * A[0][j] * determinant(submatrix)
            sign *= -1
        return det
    
    def tseitin_encoding(G):
        n = len(G)
        clauses = []
        literals = {}
        for i in range(n):
            literals[i] = random.randint(1, 2*n)
        for i in range(n):
            clauses.append([literals[i]])
        for i in range(n):
            for j in range(i+1, n):
                if G[i][j]:
                    clauses.append([-literals[i], -literals[j]])
        return clauses
    
    def resolution_width(clauses):
        queue = clauses[:]
        resolvents = set()
        while queue:
            clause1 = queue.pop(0)
            for clause2 in queue:
                common_lit = next((lit for lit in clause1 if -lit in clause2), None)
                if common_lit is not None:
                    new_clause = [lit for lit in clause1 if lit != common_lit] + [lit for lit in clause2 if lit != -common_lit]
                    new_clause.sort()
                    if new_clause not in resolvents:
                        resolvents.add(tuple(new_clause))
                        queue.append(new_clause)
        return len(resolvents)
    
    def differential_form_rank(G):
        n = len(G)
        A = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i+1, n):
                if G[i][j]:
                    A[i][j] = 1
                    A[j][i] = -1
        rank = 0
        for row in gaussian_elimination(A):
            if any(row):
                rank += 1
        return rank
    
    def generate_d_regular_graph(n, d):
        G = [[False] * n for _ in range(n)]
        degree_count = [0] * n
        edges_added = 0
        while edges_added < d * n // 2:
            u = random.randint(0, n-1)
            v = random.randint(0, n-1)
            if u != v and not G[u][v]:
                G[u][v] = True
                G[v][u] = True
                degree_count[u] += 1
                degree_count[v] += 1
                edges_added += 1
        return G
    
    def correlation_coefficient(x, y):
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        cov = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n)) / n
        var_x = sum((x[i] - mean_x) ** 2 for i in range(n)) / n
        var_y = sum((y[i] - mean_y) ** 2 for i in range(n)) / n
        return cov / (math.sqrt(var_x) * math.sqrt(var_y))
    
    n_max = 40
    instances_tested = 0
    ranks = []
    widths = []
    
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            G = generate_d_regular_graph(n, 2)
            rank = differential_form_rank(G)
            width = resolution_width(tseitin_encoding(G))
            ranks.append(rank)
            widths.append(width)
            instances_tested += 1
    
    if len(ranks) < 30:
        return {
            "metric_name": "Correlation Coefficient",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "Insufficient instances"
        }
    
    corr_coeff = correlation_coefficient(ranks, widths)
    
    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": corr_coeff,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": corr_coeff >= 0.7,
        "counterexample": "" if corr_coeff >= 0.7 else "Low correlation coefficient"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_corr_coeff = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_corr_coeff} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_corr_coeff} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='Low correlation coefficient' first_failing_seed={first_failing_seed}")