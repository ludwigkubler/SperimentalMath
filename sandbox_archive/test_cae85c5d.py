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
    
    def generate_d_regular_graph(n, d):
        if (n * d) % 2 != 0 or n < d:
            return None
        graph = [[] for _ in range(n)]
        edges = set()
        for i in range(n):
            for j in range(i + 1, n):
                if len(graph[i]) < d and len(graph[j]) < d:
                    if (i, j) not in edges and (j, i) not in edges:
                        graph[i].append(j)
                        graph[j].append(i)
                        edges.add((i, j))
        return graph
    
    def tseitin_formula(graph):
        n = len(graph)
        literals = [f'x{i}' for i in range(n)]
        clauses = []
        for i in range(n):
            clause = [literals[i]]
            for j in graph[i]:
                clause.append(f'-{literals[j]}')
            clauses.append(clause)
            for j in range(i + 1, n):
                if (i, j) not in graph and (j, i) not in graph:
                    clauses.append([f'-{literals[i]}', literals[j]])
                    clauses.append([f'-{literals[j]}', literals[i]])
        return literals, clauses
    
    def tropical_rank(clauses):
        n = len(clauses)
        m = len(clauses[0])
        matrix = [[0] * (m + 1) for _ in range(n)]
        for i in range(n):
            for j in range(m):
                if clauses[i][j].startswith('-'):
                    matrix[i][j] = -1
                else:
                    matrix[i][j] = 1
            matrix[i][-1] = 1
        
        def gaussian_elimination(A, b):
            n = len(A)
            m = len(A[0])
            for i in range(n):
                max_row = i
                for j in range(i + 1, n):
                    if abs(A[j][i]) > abs(A[max_row][i]):
                        max_row = j
                A[i], A[max_row] = A[max_row], A[i]
                b[i], b[max_row] = b[max_row], b[i]
                
                for j in range(i + 1, n):
                    factor = -A[j][i] / A[i][i]
                    for k in range(i, m):
                        A[j][k] += factor * A[i][k]
                    b[j] += factor * b[i]
            
            x = [0] * m
            for i in range(n - 1, -1, -1):
                x[i] = (b[i] - sum(A[i][j] * x[j] for j in range(i + 1, m))) / A[i][i]
            return x
        
        rank = 0
        b = [1] * n
        while True:
            try:
                gaussian_elimination(matrix, b)
                rank += 1
            except ZeroDivisionError:
                break
        return rank
    
    def compute_ratio(rank, n, d):
        if n <= 0 or d <= 0:
            return None
        return rank / (math.log(n) * math.log(d))
    
    results = []
    for _ in range(30):
        n = random.randint(5, 40)
        d = random.randint(2, min(n - 1, 10))
        graph = generate_d_regular_graph(n, d)
        if graph is None:
            continue
        literals, clauses = tseitin_formula(graph)
        rank = tropical_rank(clauses)
        ratio = compute_ratio(rank, n, d)
        if ratio is not None:
            results.append(ratio)
    
    if len(results) == 0:
        return {
            "metric_name": "Ratio",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    mean = sum(results) / len(results)
    std = math.sqrt(sum((x - mean) ** 2 for x in results) / len(results))
    support_fraction = sum(1 for r in results if r <= 2 * std + mean) / len(results)
    
    return {
        "metric_name": "Ratio",
        "metric_value": mean,
        "instances_tested": len(results),
        "n_max": max(n for _ in range(30)),
        "conjecture_holds": support_fraction >= 0.8,
        "counterexample": "" if support_fraction >= 0.8 else f"Ratio {max(results)} > 2*std+mean"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...{result}...}}")
        results.append(result["metric_value"])
    
    if all(v is not None for v in results):
        mean = sum(results) / len(results)
        std = math.sqrt(sum((x - mean) ** 2 for x in results) / len(results))
        support_fraction = sum(1 for r in results if r <= 2 * std + mean) / len(results)
        
        if support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
        else:
            first_failing_seed = next(i for i, r in enumerate(results) if r > 2 * std + mean)
            print(f"RESULT: FALSIFIED counterexample=\"Ratio {max(results)} > 2*std+mean\" first_failing_seed={seeds[first_failing_seed]}")
    else:
        print("RESULT: INCONCLUSIVE some results are None")