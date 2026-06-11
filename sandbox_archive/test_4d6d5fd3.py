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
    
    def local_induction_dimension(poset):
        n = len(poset)
        if n <= 1:
            return 0
        adj_matrix = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                if poset[j][i]:
                    adj_matrix[i][j] = 1
                    adj_matrix[j][i] = 1
        
        def dfs(node, visited):
            stack = [node]
            while stack:
                node = stack.pop()
                if not visited[node]:
                    visited[node] = True
                    for neighbor in range(n):
                        if adj_matrix[node][neighbor] and not visited[neighbor]:
                            stack.append(neighbor)
        
        visited = [False] * n
        components = 0
        for i in range(n):
            if not visited[i]:
                dfs(i, visited)
                components += 1
        
        return components - 1
    
    def communication_complexity_rank_variance(poset):
        n = len(poset)
        rank_matrix = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                if poset[j][i]:
                    rank_matrix[i][j] = 1
                    rank_matrix[j][i] = 1
        
        def gaussian_elimination(matrix):
            rows, cols = len(matrix), len(matrix[0])
            for i in range(rows):
                max_row = i
                for j in range(i + 1, rows):
                    if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                        max_row = j
                matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
                if matrix[i][i] == 0:
                    return None
                for j in range(i + 1, cols):
                    matrix[i][j] /= matrix[i][i]
                for k in range(rows):
                    if k != i and matrix[k][i]:
                        for j in range(i + 1, cols):
                            matrix[k][j] -= matrix[i][j] * matrix[k][i]
            return matrix
        
        reduced_matrix = gaussian_elimination(rank_matrix)
        if reduced_matrix is None:
            return 0
        
        rank = sum(1 for row in reduced_matrix if any(row))
        variance = (n - rank) / n
        return variance
    
    def generate_poset(n):
        poset = [[False] * n for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                poset[i][j] = random.choice([True, False])
        return poset
    
    n_max = 40
    instances_tested = 30
    metric_values = []
    
    for _ in range(instances_tested):
        poset = generate_poset(n_max)
        l_id = local_induction_dimension(poset)
        v_p = communication_complexity_rank_variance(poset)
        
        if l_id is None or v_p is None:
            continue
        
        metric_values.append(l_id * v_p)
    
    if not metric_values:
        return {
            "metric_name": "l_i.d. * v(P)",
            "metric_value": 0,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    mean = sum(metric_values) / len(metric_values)
    std_dev = math.sqrt(sum((x - mean) ** 2 for x in metric_values) / len(metric_values))
    
    return {
        "metric_name": "l_i.d. * v(P)",
        "metric_value": mean,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": mean >= 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")