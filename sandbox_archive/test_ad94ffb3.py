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

def generate_d_regular_graph(n, d):
    if (n * d) % 2 != 0:
        return None
    graph = [[0] * n for _ in range(n)]
    degree_counts = [0] * n
    edges_added = 0
    
    while edges_added < n * d // 2:
        u, v = random.sample(range(n), 2)
        if u != v and graph[u][v] == 0 and degree_counts[u] + degree_counts[v] < d:
            graph[u][v] = 1
            graph[v][u] = 1
            degree_counts[u] += 1
            degree_counts[v] += 1
            edges_added += 1
    
    return graph

def gaussian_elimination(matrix):
    n = len(matrix)
    for i in range(n):
        # Find pivot
        max_row = i
        for j in range(i + 1, n):
            if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                max_row = j
        
        # Swap rows
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        
        # Eliminate below pivot
        for j in range(i + 1, n):
            factor = Fraction(matrix[j][i], matrix[i][i])
            for k in range(n):
                matrix[j][k] -= factor * matrix[i][k]
    
    rank = sum(1 for row in matrix if any(row))
    return rank

def resolution_proof_width(graph):
    n = len(graph)
    clauses = []
    variables = set()
    
    # Add clauses for each edge
    for i in range(n):
        for j in range(i + 1, n):
            if graph[i][j] == 1:
                clause = [-i - 1, -j - 1]
                clauses.append(clause)
                variables.update([i + 1, j + 1])
    
    # Add unit propagation
    while True:
        new_clauses = []
        for clause in clauses:
            if len(clause) == 1:
                literal = clause[0]
                variables.discard(abs(literal))
                for c in clauses:
                    if literal in c:
                        c.remove(literal)
                    elif -literal in c:
                        new_clauses.append([l for l in c if l != -literal])
        if not new_clauses:
            break
        clauses.extend(new_clauses)
    
    return len(variables)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    rank_sum = 0
    width_sum = 0
    
    for n in [5, 10, 15, 20, 30, 40]:
        if time.time() + 200 < end_time:
            graph = generate_d_regular_graph(n, n - 1)
            if graph is None:
                continue
            rank = gaussian_elimination(graph)
            width = resolution_proof_width(graph)
            results.append((rank, width))
            rank_sum += rank
            width_sum += width
    
    if not results:
        return {
            "metric_name": "correlation",
            "metric_value": 0,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    correlation = (rank_sum * width_sum - len(results) * rank_sum * width_sum / len(results)) / \
                  math.sqrt(rank_sum**2 * width_sum**2 / len(results))
    
    return {
        "metric_name": "correlation",
        "metric_value": correlation,
        "instances_tested": len(results),
        "n_max": max(n for _, _ in results),
        "conjecture_holds": abs(correlation) <= 0.5,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    import time
    
    if not sys.argv[1:]:
        seeds = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    else:
        seeds = list(map(int, sys.argv[1:]))
    
    end_time = time.time() + 240
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_value = sum(r['metric_value'] for r in results) / len(results)
    std_value = math.sqrt(sum((r['metric_value'] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r['conjecture_holds'] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result['conjecture_holds'])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_support")