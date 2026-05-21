# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction
from itertools import combinations, permutations

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_3_regular_graph(n):
        while True:
            edges = set()
            vertices = list(range(n))
            for v in vertices:
                neighbors = random.sample(vertices, 2)
                if (v, neighbors[0]) not in edges and (neighbors[0], v) not in edges:
                    edges.add((v, neighbors[0]))
                    edges.add((v, neighbors[1]))
            G = {v: [] for v in vertices}
            for u, v in edges:
                G[u].append(v)
                G[v].append(u)
            if is_connected(G) and spectral_gap(G) >= 0.15:
                return G
    
    def is_connected(G):
        visited = set()
        stack = [0]
        while stack:
            v = stack.pop()
            if v not in visited:
                visited.add(v)
                stack.extend(u for u in G[v] if u not in visited)
        return len(visited) == len(G)
    
    def spectral_gap(G):
        n = len(G)
        A = [[0] * n for _ in range(n)]
        d = [sum(1 for _ in neighbors) for neighbors in G.values()]
        for v, neighbors in enumerate(G.values()):
            for u in neighbors:
                A[v][u] = 1 / math.sqrt(d[u] * d[v])
        
        eigenvalues_A = eigenvalues(A)
        return max(eigenvalues_A) - min(eigenvalue for eigenvalue in eigenvalues_A if eigenvalue > 0)
    
    def eigenvalues(M):
        n = len(M)
        identity = [[Fraction(1, n) if i == j else Fraction(0) for j in range(n)] for i in range(n)]
        
        def matrix_multiply(A, B):
            result = [[sum(A[i][k] * B[k][j] for k in range(n)) for j in range(n)] for i in range(n)]
            return result
        
        def subtract_matrices(A, B):
            result = [[A[i][j] - B[i][j] for j in range(n)] for i in range(n)]
            return result
        
        def add_matrices(A, B):
            result = [[A[i][j] + B[i][j] for j in range(n)] for i in range(n)]
            return result
        
        def scalar_multiply(M, c):
            result = [[c * M[i][j] for j in range(n)] for i in range(n)]
            return result
        
        def matrix_power(M, k):
            if k == 0:
                return identity
            elif k % 2 == 1:
                return matrix_multiply(M, matrix_power(M, k - 1))
            else:
                half_power = matrix_power(M, k // 2)
                return matrix_multiply(half_power, half_power)
        
        def trace(M):
            return sum(M[i][i] for i in range(n))
        
        def det(M):
            if n == 1:
                return M[0][0]
            elif n == 2:
                return M[0][0] * M[1][1] - M[0][1] * M[1][0]
            else:
                result = Fraction(0)
                for j in range(n):
                    submatrix = [[M[i][k] for k in range(n) if k != j] for i in range(1, n)]
                    result += (-1) ** j * M[0][j] * det(submatrix)
                return result
        
        def gaussian_elimination(A):
            A_augmented = [row + [Fraction(1)] for row in A]
            n = len(A)
            for i in range(n):
                pivot_row = max(range(i, n), key=lambda r: abs(A[r][i]))
                A_augmented[i], A_augmented[pivot_row] = A_augmented[pivot_row], A_augmented[i]
                for j in range(i + 1, n):
                    factor = A_augmented[j][i] / A_augmented[i][i]
                    A_augmented[j] = [A_augmented[j][k] - factor * A_augmented[i][k] for k in range(n + 1)]
            return [row[:-1] for row in A_augmented]
        
        eigenvalues = []
        A_copy = [row[:] for row in M]
        while len(A_copy) > 0:
            pivot_row = max(range(len(A_copy)), key=lambda r: abs(A_copy[r][r]))
            A_copy[pivot_row], A_copy[0] = A_copy[0], A_copy[pivot_row]
            pivot = A_copy[0][0]
            for j in range(1, len(A_copy[0])):
                A_copy[0][j] /= pivot
            for i in range(1, len(A_copy)):
                factor = A_copy[i][0]
                for j in range(len(A_copy[0])):
                    A_copy[i][j] -= factor * A_copy[0][j]
            eigenvalues.append(pivot)
            A_copy = [row[1:] for row in A_copy[1:]]
        return eigenvalues
    
    def dhar_burning(G, c):
        n = len(G)
        q = random.choice(list(G.keys()))
        reduced_divisor = {v: 0 for v in G}
        queue = [(q, c[q])]
        while queue:
            u, val = queue.pop(0)
            if val > 0:
                reduced_divisor[u] += val
                for v in G[u]:
                    reduced_divisor[v] -= val / len(G[u])
                    if reduced_divisor[v] < 0:
                        queue.append((v, -reduced_divisor[v]))
        return sum(reduced_divisor.values())
    
    def tseitin_formula(G, c):
        n = len(G)
        literals = {v: f'x{v}' for v in G}
        clauses = []
        for v in G:
            if c[v] == 1:
                clauses.append([literals[v]])
            else:
                clauses.append([-literals[v]])
        for u, v in G:
            clauses.append([literals[u], -literals[v]])
            clauses.append([-literals[u], literals[v]])
        return clauses
    
    def dpll(clauses):
        n = len(clauses)
        assignment = [None] * n
        stack = []
        
        def backtrack(level):
            if level == n:
                return True
            for literal in clauses[level]:
                var, sign = (literal[1:], -1) if literal.startswith('-') else (literal, 1)
                if assignment[var] is None:
                    assignment[var] = sign
                    stack.append((var, sign))
                    if backtrack(level + 1):
                        return True
                    assignment[var] = None
                    stack.pop()
            return False
        
        return backtrack(0)
    
    n_values = [8, 10, 12, 14]
    results = []
    for n in n_values:
        for _ in range(30):
            G = generate_3_regular_graph(n)
            c = {v: random.choice([0, 1]) for v in G}
            if sum(c.values()) % 2 == 0:
                continue
            r_BN = dhar_burning(G, c)
            D_G_c = n - r_BN
            Tseitin_clauses = tseitin_formula(G, c)
            leaf_count = 0
            max_width = 0
            
            def dpll_with_count(clauses):
                nonlocal leaf_count, max_width
                n = len(clauses)
                assignment = [None] * n
                stack = []
                
                def backtrack(level):
                    if level == n:
                        nonlocal leaf_count
                        leaf_count += 1
                        return True
                    for literal in clauses[level]:
                        var, sign = (literal[1:], -1) if literal.startswith('-') else (literal, 1)
                        if assignment[var] is None:
                            assignment[var] = sign
                            stack.append((var, sign))
                            max_width = max(max_width, len(literal))
                            if backtrack(level + 1):
                                return True
                            assignment[var] = None
                            stack.pop()
                    return False
                
                return backtrack(0)
            
            dpll_with_count(Tseitin_clauses)
            results.append({
                "metric_name": "D(G,c)",
                "metric_value": D_G_c,
                "instances_tested": 1,
                "conjecture_holds": True if (1/3 <= math.log2(leaf_count) / D_G_c <= 3 and 1/3 <= max_width / D_G_c <= 3) else False,
                "counterexample": "" if (1/3 <= math.log2(leaf_count) / D_G_c <= 3 and 1/3 <= max_width / D_G_c <= 3) else f"Leaf count: {leaf_count}, Max width: {max_width}"
            })
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        return {
            "seed": seed,
            "metric_name": "D(G,c)",
            "mean_metric_value": mean_metric_value,
            "std_metric_value": std_metric_value,
            "support_fraction": support_fraction
        }
    else:
        for result in results:
            if not result["conjecture_holds"]:
                return {
                    "seed": seed,
                    "metric_name": "D(G,c)",
                    "mean_metric_value": mean_metric_value,
                    "std_metric_value": std_metric_value,
                    "support_fraction": support_fraction,
                    "counterexample": result["counterexample"]
                }
        return {
            "seed": seed,
            "metric_name": "D(G,c)",
            "mean_metric_value": mean_metric_value,
            "std_metric_value": std_metric_value,
            "support_fraction": support_fraction
        }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]]
    if not seeds:
        seeds = [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(result["mean_metric_value"] for result in results) / len(results)
    std_metric_value = math.sqrt(sum((result["mean_metric_value"] - mean_metric_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["support_fraction"] >= 0.8) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(result["support_fraction"] < 0.8 for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if result["support_fraction"] < 0.8)
        counterexample = next(result["counterexample"] for result in results if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_support")