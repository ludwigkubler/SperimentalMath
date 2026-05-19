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

def gaussian_elimination(matrix):
    n = len(matrix)
    for i in range(n):
        # Find pivot row and swap with current row
        max_row = i
        for k in range(i+1, n):
            if abs(matrix[k][i]) > abs(matrix[max_row][i]):
                max_row = k
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        
        # Eliminate non-pivot elements below the pivot
        factor = Fraction(1, matrix[i][i])
        for k in range(i+1, n):
            matrix[k][i] *= -factor
        
        # Eliminate non-pivot elements above and below the current row
        for j in range(n):
            if j != i:
                factor = matrix[j][i]
                for k in range(n):
                    matrix[j][k] += factor * matrix[i][k]
    
    # Count non-zero rows to get Jordan rank
    jordan_rank = sum(1 for row in matrix if any(row))
    return jordan_rank

def d_regular_expander_graph(d, n):
    graph = [[] for _ in range(n)]
    for i in range(n):
        neighbors = random.sample(range(n), d)
        while len(neighbors) > 0:
            neighbor = neighbors.pop()
            if neighbor != i and i not in graph[neighbor]:
                graph[i].append(neighbor)
                graph[neighbor].append(i)
    return graph

def clause_incidence_matrix(graph, n):
    matrix = [[0] * n for _ in range(n)]
    for u in range(n):
        for v in graph[u]:
            if u < v:
                matrix[u][v] = 1
                matrix[v][u] = 1
    return matrix

def resolution_width(matrix, n):
    # Placeholder function; actual implementation needed
    return 0  # Replace with actual width estimation logic

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    
    for n in n_values:
        d = 3  # Example value; adjust as needed
        graph = d_regular_expander_graph(d, n)
        matrix = clause_incidence_matrix(graph, n)
        
        jordan_rank = gaussian_elimination(matrix)
        width = resolution_width(matrix, n)
        
        if jordan_rank >= math.sqrt(n):
            total_metric_value += width
            instances_tested += 1
    
    metric_name = "resolution_width"
    metric_value = total_metric_value / instances_tested if instances_tested > 0 else 0
    conjecture_holds = metric_value >= math.sqrt(n_values[-1])
    counterexample = "" if conjecture_holds else f"width < sqrt({n_values[-1]})"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")