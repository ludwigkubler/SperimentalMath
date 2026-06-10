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

def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        # Find pivot
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        
        # Eliminate below the pivot
        for j in range(i+1, n):
            factor = -A[j][i] / A[i][i]
            for k in range(n):
                A[j][k] += factor * A[i][k]

    rank = 0
    for i in range(n):
        if all(abs(A[i][j]) < 1e-9 for j in range(n)):
            continue
        rank += 1
    return rank

def tropical_rank(clauses):
    n = len(clauses)
    m = len(clauses[0])
    A = [[float('-inf')] * (m + 1) for _ in range(n)]
    
    for i in range(n):
        for j in range(m):
            if clauses[i][j].startswith('-'):
                A[i][j] = float('inf')
            else:
                A[i][j] = int(clauses[i][j])
        A[i][-1] = 0
    
    return gaussian_elimination(A)

def generate_d_regular_graph(n, d):
    edges = set()
    nodes = list(range(n))
    random.shuffle(nodes)
    
    for i in range(n):
        for j in range(i+1, n):
            if len(edges) >= (n * (d - 1)) // 2:
                break
            if (nodes[i], nodes[j]) not in edges and (nodes[j], nodes[i]) not in edges:
                edges.add((nodes[i], nodes[j]))
                if len(edges) == (n * (d - 1)) // 2:
                    break
    
    return list(edges)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        d = 2
        graph = generate_d_regular_graph(n, d)
        clauses = []
        
        # Construct Tseitin formula
        variables = list(range(1, n + 1))
        literals = [f'x{i}' for i in range(1, n + 1)]
        neg_literals = [f'-x{i}' for i in range(1, n + 1)]
        
        # Add clauses for each edge
        for (u, v) in graph:
            a, b = variables[u-1], variables[v-1]
            literals.append(f'x{a}+x{b}')
            neg_literals.append(f'-x{a}-x{b}')
            literals.append(f'-x{a}-x{b}')
            neg_literals.append(f'x{a}+x{b}')
        
        # Add clauses for each node
        for i in range(n):
            a = variables[i]
            literals.append(f'x{a}')
            neg_literals.append(f'-x{a}')
        
        # Construct the Tseitin formula
        for literal in literals:
            if literal.startswith('-'):
                clauses.append([literal[1:], '0'])
            else:
                clauses.append([literal, '1'])
        
        rank = tropical_rank(clauses)
        results.append(rank)
    
    metric_value = sum(results) / len(results)
    n_max = max(n_values)
    conjecture_holds = all(r <= 2 * math.sqrt(metric_value) for r in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "tropical_rank",
        "metric_value": metric_value,
        "instances_tested": len(results),
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result["metric_value"])
    
    mean = sum(results) / len(results)
    std_dev = math.sqrt(sum((x - mean) ** 2 for x in results) / len(results))
    support_fraction = sum(1 for r in results if all(r <= 2 * math.sqrt(m) for m in results)) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
    elif any(result > 2 * math.sqrt(mean) for result in results):
        first_failing_seed = seeds[results.index(max(results))]
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")