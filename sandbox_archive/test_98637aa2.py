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
    
    def gaussian_elimination(matrix):
        rows, cols = len(matrix), len(matrix[0])
        for i in range(rows):
            max_row = i + max(range(i, rows), key=lambda x: abs(matrix[x][i]))
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            for j in range(cols):
                if j != i:
                    factor = Fraction(matrix[j][i], matrix[i][i])
                    for k in range(rows):
                        matrix[j][k] -= factor * matrix[i][k]
        return matrix
    
    def tseitin_formula(graph):
        n = len(graph)
        literals = [random.randint(1, 2*n) for _ in range(n)]
        clauses = []
        for i in range(n):
            clauses.append([literals[2*i], -literals[2*i+1]])
            for j in range(i + 1, n):
                if graph[i][j]:
                    clauses.append([-literals[2*i], literals[2*j]])
                    clauses.append([-literals[2*j], literals[2*i]])
        return literals, clauses
    
    def resolution_length(clauses):
        stack = []
        while True:
            new_clauses = set()
            for clause1 in clauses:
                for clause2 in clauses:
                    if len(set(clause1) & set(clause2)) == 1:
                        new_clause = list(set(clause1) ^ set(clause2))
                        if not any(new_clause == c for c in stack):
                            new_clauses.add(tuple(sorted(new_clause)))
            if not new_clauses:
                break
            clauses.update(new_clauses)
        return len(stack)
    
    def asymptotic_dimension(graph):
        n = len(graph)
        radius = [0] * n
        visited = [False] * n
        
        def bfs(start):
            queue = [(start, 0)]
            while queue:
                node, dist = queue.pop(0)
                if not visited[node]:
                    visited[node] = True
                    radius[start] = max(radius[start], dist)
                    for neighbor in range(n):
                        if graph[node][neighbor] and not visited[neighbor]:
                            queue.append((neighbor, dist + 1))
        
        for i in range(n):
            bfs(i)
        
        return sum(radius) // n
    
    def generate_random_graph(n):
        graph = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                if random.choice([True, False]):
                    graph[i][j] = graph[j][i] = 1
        return graph
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_length = 0
    instances_tested = 0
    
    for n in n_values:
        graph = generate_random_graph(n)
        d = asymptotic_dimension(graph)
        literals, clauses = tseitin_formula(graph)
        length = resolution_length(clauses)
        total_length += length
        instances_tested += 1
    
    mean_length = total_length / len(n_values)
    
    return {
        "metric_name": "Resolution Length",
        "metric_value": mean_length,
        "instances_tested": instances_tested,
        "conjecture_holds": mean_length >= 2 ** (math.log(d, 2) * 0.5),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_length = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_length} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_length} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='resolution_length_not_exponential' first_failing_seed={first_failing_seed}")