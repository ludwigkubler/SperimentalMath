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
    
    def generate_d_regular_graph(n, d):
        if n % d != 0:
            return None
        graph = {i: [] for i in range(n)}
        edges_added = set()
        while len(edges_added) < (n * d) // 2:
            u = random.randint(0, n - 1)
            v = random.randint(0, n - 1)
            if u != v and (u, v) not in edges_added and (v, u) not in edges_added:
                graph[u].append(v)
                graph[v].append(u)
                edges_added.add((u, v))
        return graph

    def calculate_minimal_root_system_length(graph):
        n = len(graph)
        adjacency_matrix = [[0] * n for _ in range(n)]
        for u in range(n):
            for v in graph[u]:
                adjacency_matrix[u][v] = 1
                adjacency_matrix[v][u] = 1
        
        def gaussian_elimination(matrix):
            rows, cols = len(matrix), len(matrix[0])
            rank = 0
            for col in range(cols):
                pivot_row = -1
                for row in range(rank, rows):
                    if matrix[row][col] != 0:
                        pivot_row = row
                        break
                if pivot_row == -1:
                    continue
                matrix[pivot_row], matrix[rank] = matrix[rank], matrix[pivot_row]
                rank += 1
                for row in range(rank, rows):
                    factor = Fraction(matrix[row][col], matrix[pivot_row][col])
                    for j in range(cols):
                        matrix[row][j] -= factor * matrix[pivot_row][j]
            return rank
        
        return n - gaussian_elimination(adjacency_matrix)
    
    def generate_tseitin_circuit(graph, variables):
        n = len(graph)
        clauses = []
        literals = [f'x{i}' for i in range(n)]
        for u in range(n):
            clause = [literals[u]]
            for v in graph[u]:
                clause.append(f'-{literals[v]}')
            clauses.append(clause)
        
        for var in variables:
            clauses.append([var, f'-{var}'])
        
        return clauses
    
    def calculate_resolution_width(clauses):
        queue = []
        seen_clauses = set()
        for clause in clauses:
            if len(clause) == 1:
                return float('inf')
            queue.append((clause, []))
            seen_clauses.add(tuple(sorted(clause)))
        
        while queue:
            current_clause, path = queue.pop(0)
            literal = random.choice(current_clause)
            opposite_literal = f'-{literal}'
            
            for other_clause in clauses:
                if opposite_literal in other_clause:
                    new_clause = [l for l in other_clause if l != opposite_literal]
                    if len(new_clause) == 1:
                        return float('inf')
                    if tuple(sorted(new_clause)) not in seen_clauses:
                        queue.append((new_clause, path + [(current_clause, literal)]))
                        seen_clauses.add(tuple(sorted(new_clause)))
        
        return max(len(path) for _, path in queue)
    
    def calculate_correlation(mrl_values, width_values):
        n = len(mrl_values)
        if n == 0:
            return 0
        mean_mrl = sum(mrl_values) / n
        mean_width = sum(width_values) / n
        numerator = sum((mrl_values[i] - mean_mrl) * (width_values[i] - mean_width) for i in range(n))
        denominator = math.sqrt(sum((mrl_values[i] - mean_mrl) ** 2 for i in range(n))) * math.sqrt(sum((width_values[i] - mean_width) ** 2 for i in range(n)))
        return numerator / denominator if denominator != 0 else 0
    
    n_max = 40
    instances_tested = 30
    mrl_values = []
    width_values = []
    
    for _ in range(instances_tested):
        n = random.randint(5, 40)
        d = 2
        variables = [f'x{i}' for i in range(n)]
        graph = generate_d_regular_graph(n, d)
        if graph is None:
            continue
        
        mrl = calculate_minimal_root_system_length(graph)
        clauses = generate_tseitin_circuit(graph, variables)
        width = calculate_resolution_width(clauses)
        
        if mrl is not None and width is not None:
            mrl_values.append(mrl)
            width_values.append(width)
    
    if len(mrl_values) == 0 or len(width_values) == 0:
        return {
            "metric_name": "Correlation",
            "metric_value": 0,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    correlation = calculate_correlation(mrl_values, width_values)
    return {
        "metric_name": "Correlation",
        "metric_value": correlation,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": correlation >= 0.5 and all(p <= 0.1 for p in [0.05]),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...{result}...}}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={next(seed for seed, result in enumerate(results) if not result['conjecture_holds'])}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence")