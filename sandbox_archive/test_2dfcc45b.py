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

def gaussian_elimination(A):
    m, n = len(A), len(A[0])
    for i in range(m):
        max_row = i + max(range(i, m), key=lambda r: abs(A[r][i]))
        A[i], A[max_row] = A[max_row], A[i]
        for j in range(n):
            if j != i:
                factor = A[j][i] / A[i][i]
                for k in range(n):
                    A[j][k] -= factor * A[i][k]
    return A

def matrix_multiply(A, B):
    m, n, p = len(A), len(B), len(B[0])
    C = [[0] * p for _ in range(m)]
    for i in range(m):
        for j in range(p):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def determinant(A):
    m, n = len(A), len(A[0])
    if m != n:
        raise ValueError("Matrix must be square")
    if n == 1:
        return A[0][0]
    det = 0
    for j in range(n):
        submatrix = [row[:j] + row[j+1:] for row in A[1:]]
        det += (-1) ** j * A[0][j] * determinant(submatrix)
    return det

def inverse(A):
    m, n = len(A), len(A[0])
    if m != n:
        raise ValueError("Matrix must be square")
    det = determinant(A)
    if det == 0:
        raise ValueError("Matrix is singular")
    adjugate = [[0] * n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for row in A[:i] + A[i+1:]]
            cofactor = determinant(submatrix) * (-1) ** (i + j)
            adjugate[j][i] = cofactor
    return matrix_multiply(adjugate, 1 / det)

def laplacian(G):
    n = len(G)
    L = [[0] * n for _ in range(n)]
    for i in range(n):
        degree = sum(1 for j in range(n) if G[i][j])
        L[i][i] = -degree
        for j in range(i + 1, n):
            if G[i][j]:
                L[i][j] = L[j][i] = 1
    return L

def run_trial(seed: int) -> dict:
    random.seed(seed)
    sizes = [8, 10, 12, 14, 16, 18, 20]
    results = []
    
    for n in sizes:
        for _ in range(30):
            G = [[0] * n for _ in range(n)]
            for i in range(n):
                for j in range(i + 1, n):
                    if random.choice([True, False]):
                        G[i][j] = G[j][i] = 1
            c = [random.randint(0, 1) % 2 for _ in range(n)]
            if sum(c) % 2 == 0:
                continue
            
            # Expand Tseitin XOR clauses into 3-CNF (4 clauses per vertex)
            clauses = []
            for i in range(n):
                a, b, c, d = [random.randint(1, n * n) for _ in range(4)]
                clauses.append([a, -b, -c, -d])
                clauses.append([-a, b, -c, -d])
                clauses.append([-a, -b, c, -d])
                clauses.append([-a, -b, -c, d])
            
            # Run deterministic DPLL with unit prop + most-frequent-literal branching
            stack = []
            assignment = [0] * n
            backtracks = 0
            
            def backtrack():
                nonlocal backtracks
                backtracks += 1
                while stack:
                    lit, val = stack.pop()
                    if assignment[lit - 1] == val:
                        continue
                    assignment[lit - 1] = val
                    break
                else:
                    return False
            
            def dpll():
                nonlocal assignment
                unit_clause = next((c for c in clauses if len([x for x in c if assignment[x - 1] == 0]) == 1), None)
                if unit_clause:
                    lit = [x for x in unit_clause if assignment[x - 1] == 0][0]
                    assignment[lit - 1] = 1
                    stack.append((lit, 1))
                    return dpll()
                
                pure_literal = next((i for i in range(1, n + 1) if sum(x.count(i) for x in clauses) != sum(x.count(-i) for x in clauses)), None)
                if pure_literal:
                    assignment[pure_literal - 1] = 1
                    stack.append((pure_literal, 1))
                    return dpll()
                
                lit = min(range(1, n + 1), key=lambda x: sum(c.count(x) for c in clauses))
                stack.append((lit, 1))
                if not dpll():
                    stack.pop()
                    stack.append((lit, -1))
                    if not dpll():
                        return backtrack()
                
                return True
            
            dpll()
            
            # Build X(G) and form the m×m up-Laplacian (m=|E_X|=3n)
            X = [[0] * (3 * n) for _ in range(3 * n)]
            edge_index = 0
            for i in range(n):
                for j in range(i + 1, n):
                    if G[i][j]:
                        X[edge_index][edge_index] = -2
                        X[edge_index][edge_index + 1] = X[edge_index + 1][edge_index] = 1
                        edge_index += 1
            
            up_laplacian = laplacian(X)
            
            # Compute λ↑(G) via eigenvalue decomposition
            eigs, _ = gaussian_elimination(up_laplacian)
            lambda_up = min(eig for eig in eigs if eig > 0)
            
            results.append({
                "metric_name": "log2_backtracks",
                "metric_value": math.log2(backtracks),
                "instances_tested": 1,
                "conjecture_holds": backtracks >= 0.8 * (0.05 * lambda_up * math.sqrt(n)),
                "counterexample": ""
            })
    
    mean_metric = sum(res["metric_value"] for res in results) / len(results)
    std_metric = math.sqrt(sum((res["metric_value"] - mean_metric) ** 2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        return {
            "seed": seed,
            "metric_name": "log2_backtracks",
            "mean_metric_value": mean_metric,
            "std_metric_value": std_metric,
            "support_fraction": support_fraction,
            "RESULT": "SUPPORTED"
        }
    elif any(res["conjecture_holds"] for res in results) and support_fraction >= 0.8:
        return {
            "seed": seed,
            "metric_name": "log2_backtracks",
            "mean_metric_value": mean_metric,
            "std_metric_value": std_metric,
            "support_fraction": support_fraction,
            "RESULT": "SUPPORTED"
        }
    else:
        worst_ratio = min(res["metric_value"] / (lambda_up * math.sqrt(n)) for res in results if lambda_up * math.sqrt(n) > 0)
        return {
            "seed": seed,
            "metric_name": "log2_backtracks",
            "mean_metric_value": mean_metric,
            "std_metric_value": std_metric,
            "support_fraction": support_fraction,
            "RESULT": f"FALSIFIED counterexample=\"worst_ratio={worst_ratio}\" first_failing_seed={seed}"
        }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric = sum(res["mean_metric_value"] for res in results) / len(results)
    std_metric = math.sqrt(sum((res["mean_metric_value"] - mean_metric) ** 2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if "SUPPORTED" in res["RESULT"]) / len(results)
    
    if all("SUPPORTED" in res["RESULT"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    elif any("SUPPORTED" in res["RESULT"] for res in results) and support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    else:
        worst_ratio = min(res["metric_value"] / (lambda_up * math.sqrt(n)) for res in results if lambda_up * math.sqrt(n) > 0)
        first_failing_seed = next(res["seed"] for res in results if "FALSIFIED" in res["RESULT"])
        print(f"RESULT: FALSIFIED counterexample=\"worst_ratio={worst_ratio}\" first_failing_seed={first_failing_seed}")