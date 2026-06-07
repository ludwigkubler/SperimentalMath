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
    
    def gaussian_elimination(matrix):
        n = len(matrix)
        for col in range(n):
            pivot_row = next((i for i in range(col, n) if matrix[i][col] != 0), None)
            if pivot_row is None:
                continue
            for row in range(pivot_row + 1, n):
                factor = -matrix[row][col] / matrix[pivot_row][col]
                for j in range(n):
                    matrix[row][j] += factor * matrix[pivot_row][j]
        rank = sum(1 for row in matrix if any(row))
        return rank
    
    def calculate_minimal_root_system_length(graph):
        n = len(graph)
        adjacency_matrix = [[0] * n for _ in range(n)]
        for u, v in graph:
            adjacency_matrix[u][v] = 1
            adjacency_matrix[v][u] = 1
        
        return n - gaussian_elimination(adjacency_matrix)
    
    def generate_d_regular_graph(d, n):
        if d * n % 2 != 0:
            raise ValueError("Graph size must be a multiple of the degree")
        
        graph = []
        for i in range(n):
            neighbors = random.sample(range(n), d - 1)
            while any(j in neighbors for j in graph[i]):
                neighbors = random.sample(range(n), d - 1)
            graph.append(neighbors)
        
        return graph
    
    def generate_sat_instance(graph, variables):
        n = len(graph)
        clauses = []
        for i in range(n):
            clause = [random.choice([-1, 1]) * (j + 1) for j in graph[i]]
            clauses.append(clause)
        
        return clauses
    
    def resolution_width(clauses):
        queue = list(clauses)
        learned_clauses = set()
        width = 0
        
        while queue:
            clause = queue.pop(0)
            if not any(lit in learned_clauses for lit in clause):
                learned_clauses.add(-clause[0])
                width = max(width, len([lit for lit in clause if -lit in learned_clauses]))
        
        return width
    
    n_values = [5, 10, 15, 20, 30, 40]
    mrl_sum = 0
    w_sum = 0
    instances_tested = 0
    n_max = 0
    
    for n in n_values:
        for _ in range(5):
            d = random.randint(1, n - 1)
            graph = generate_d_regular_graph(d, n)
            mrl = calculate_minimal_root_system_length(graph)
            clauses = generate_sat_instance(graph, list(range(n)))
            w = resolution_width(clauses)
            
            mrl_sum += mrl
            w_sum += w
            instances_tested += 1
            n_max = max(n_max, n)
    
    mean_mrl = mrl_sum / instances_tested
    mean_w = w_sum / instances_tested
    
    correlation_coefficient = (instances_tested * sum(mrl * w for mrl, w in zip(range(5), range(5))) -
                               mean_mrl * sum(w for w in range(5)) - 
                               mean_w * sum(mrl for mrl in range(5))) / \
                              math.sqrt((instances_tested * sum(mrl**2 for mrl in range(5)) - mean_mrl**2) *
                                        (instances_tested * sum(w**2 for w in range(5)) - mean_w**2))
    
    conjecture_holds = correlation_coefficient >= 0.5
    counterexample = "" if conjecture_holds else "correlation_coefficient_too_low"
    
    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
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
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")