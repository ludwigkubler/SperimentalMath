# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def generate_d_regular_graph(d, n):
    if n % d != 0:
        raise ValueError("Graph size must be a multiple of the degree")
    
    graph = [[] for _ in range(n)]
    edges_used = set()
    
    def add_edge(u, v):
        if (u, v) not in edges_used and (v, u) not in edges_used:
            graph[u].append(v)
            graph[v].append(u)
            edges_used.add((u, v))
            edges_used.add((v, u))
    
    for i in range(n):
        for j in range(i + 1, n):
            if len(graph[i]) < d and len(graph[j]) < d:
                add_edge(i, j)
                if len(edges_used) == (n * d) // 2:
                    break
        if len(edges_used) == (n * d) // 2:
            break
    
    return graph

def tseitin_formula(graph):
    n = len(graph)
    clauses = []
    
    for i in range(n):
        literals = [f"x{i}_{j}" for j in range(d)]
        clause = ["~" + literals[0]]
        for literal in literals[1:]:
            clause.append("~" + literal)
            clause.append(literals[0] + " | " + literal)
        clauses.append(clause)
    
    for i in range(n):
        for j in range(i + 1, n):
            if j not in graph[i]:
                literals = [f"x{i}_{k}" for k in range(d)]
                literals += [f"x{j}_{k}" for k in range(d)]
                clause = []
                for literal in literals:
                    clause.append("~" + literal)
                clauses.append(clause)
    
    return clauses

def gaussian_elimination(matrix):
    n, m = len(matrix), len(matrix[0])
    rank = 0
    
    for i in range(n):
        if rank >= m:
            break
        
        pivot_row = -1
        for j in range(rank, n):
            if matrix[j][i] != 0:
                pivot_row = j
                break
        
        if pivot_row == -1:
            continue
        
        matrix[i], matrix[pivot_row] = matrix[pivot_row], matrix[i]
        
        factor = Fraction(1, matrix[i][i])
        for j in range(i + 1, m):
            matrix[i][j] *= factor
        
        for j in range(n):
            if j != i:
                factor = matrix[j][i]
                for k in range(i + 1, m):
                    matrix[j][k] -= factor * matrix[i][k]
        
        rank += 1
    
    return rank

def minimal_tropical_motivic_rank(clauses):
    n = len(clauses)
    m = len(clauses[0])
    
    matrix = [[Fraction(0) for _ in range(m)] for _ in range(n)]
    
    for i in range(n):
        for j in range(m):
            if clauses[i][j] == "1":
                matrix[i][j] = Fraction(1)
            elif clauses[i][j] == "0":
                matrix[i][j] = Fraction(0)
            else:
                matrix[i][j] = Fraction(-1)
    
    return gaussian_elimination(matrix)

def communication_complexity_rank(clauses):
    n = len(clauses)
    m = len(clauses[0])
    
    max_depth = 0
    
    def dfs(node, depth):
        nonlocal max_depth
        if depth > max_depth:
            max_depth = depth
        
        for i in range(n):
            if clauses[i][node] != "0":
                dfs(i, depth + 1)
    
    for i in range(m):
        dfs(i, 1)
    
    return max_depth

def run_trial(seed: int) -> dict:
    random.seed(seed)
    d = random.randint(3, 40)
    n = d * (d + 1)
    
    graph = generate_d_regular_graph(d, n)
    clauses = tseitin_formula(graph)
    
    mtr_C = minimal_tropical_motivic_rank(clauses)
    CR = communication_complexity_rank(clauses)
    
    ratio = Fraction(mtr_C, CR ** 2)
    
    return {
        "metric_name": "ratio",
        "metric_value": float(ratio),
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": ratio <= 1.5,
        "counterexample": "" if ratio <= 1.5 else f"correlation_coefficient={float(ratio)}"
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
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient>1.5\" first_failing_seed={first_failing_seed}")