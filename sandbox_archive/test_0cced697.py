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
    
    def generate_k_regular_graph(n, k):
        if (k * n) % 2 != 0 or k > n - 1:
            return None
        graph = {i: [] for i in range(n)}
        edges = set()
        while len(edges) < k * n // 2:
            u, v = random.sample(range(n), 2)
            if (u, v) not in edges and (v, u) not in edges:
                edges.add((u, v))
                graph[u].append(v)
                graph[v].append(u)
        return graph
    
    def tseitin_formula(graph):
        n = len(graph)
        clauses = []
        for i in range(n):
            clauses.append([i + 1])
            for j in graph[i]:
                clauses.append([-i - 1, j + 1])
        return clauses
    
    def gaussian_elimination(matrix):
        m, n = len(matrix), len(matrix[0])
        for i in range(m):
            max_row = i
            for j in range(i + 1, m):
                if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                    max_row = j
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            if matrix[i][i] == 0:
                return None
            for j in range(i + 1, n):
                matrix[i][j] /= matrix[i][i]
            matrix[i][i] = 1
            for j in range(m):
                if j != i and matrix[j][i] != 0:
                    factor = matrix[j][i]
                    for k in range(n):
                        matrix[j][k] -= factor * matrix[i][k]
        return matrix
    
    def schur_multiplier(graph):
        n = len(graph)
        A = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in graph[i]:
                A[i][j] += 1
        B = gaussian_elimination(A)
        if B is None:
            return None
        rank = sum(1 for row in B if any(x != 0 for x in row))
        return n - rank
    
    def frege_proof_width(clauses):
        variables = set()
        for clause in clauses:
            for literal in clause:
                variables.add(abs(literal))
        num_vars = len(variables)
        max_width = 1
        for _ in range(1000):  # Random DPLL solver simulation
            assignment = {i: random.choice([True, False]) for i in range(1, num_vars + 1)}
            satisfied = True
            for clause in clauses:
                if all(not assignment[abs(lit)] if lit < 0 else assignment[lit] for lit in clause):
                    continue
                satisfied = False
                break
            if not satisfied:
                max_width += 1
        return max_width
    
    def correlation(x, y):
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        cov = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n)) / n
        std_x = math.sqrt(sum((x[i] - mean_x) ** 2 for i in range(n)) / n)
        std_y = math.sqrt(sum((y[i] - mean_y) ** 2 for i in range(n)) / n)
        return cov / (std_x * std_y)
    
    def is_valid_graph(graph):
        n = len(graph)
        for neighbors in graph.values():
            if len(neighbors) != len(set(neighbors)):
                return False
        return True
    
    results = []
    instances_tested = 0
    n_max = 0
    conjecture_holds = True
    counterexample = ""
    
    for n in [5, 10, 15, 20, 30, 40]:
        if n > n_max:
            n_max = n
        
        for _ in range(5):  # Sample 5 instances per size
            k = random.randint(1, min(n - 1, 3))
            graph = generate_k_regular_graph(n, k)
            if graph is None or not is_valid_graph(graph):
                continue
            
            clauses = tseitin_formula(graph)
            gamma = schur_multiplier(graph)
            width = frege_proof_width(clauses)
            
            if gamma is None:
                conjecture_holds = False
                counterexample = "mapping_undefined"
                break
            
            results.append((gamma, width))
            instances_tested += 1
    
    if not conjecture_holds:
        return {
            "metric_name": "correlation",
            "metric_value": -1,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": counterexample
        }
    
    gamma_values, width_values = zip(*results)
    corr = correlation(gamma_values, width_values)
    mean_gamma = sum(gamma_values) / len(gamma_values)
    max_width = max(width_values)
    
    if corr < 0.8 or mean_gamma > 3 * max_width:
        conjecture_holds = False
        counterexample = "correlation_too_low"
    
    return {
        "metric_name": "correlation",
        "metric_value": corr,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result["metric_value"])
    
    mean_corr = sum(results) / len(results)
    support_fraction = sum(1 for r in results if r >= 0.8 and r <= 3 * max(results)) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_corr} std={math.sqrt(sum((r - mean_corr) ** 2 for r in results) / len(results))} support_fraction={support_fraction}")
    elif any(r < 0.8 or r > 3 * max(results) for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if result < 0.8 or result > 3 * max(results))
        print(f"RESULT: FALSIFIED counterexample='correlation_too_low' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_support")