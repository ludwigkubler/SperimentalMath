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
    
    def generate_instance(n):
        return [random.randint(0, n - 1) for _ in range(n)]
    
    def cayley_graph(instance):
        graph = {}
        for x in instance:
            for y in instance:
                if (x + y) % len(instance) not in graph[x]:
                    graph[x][y] = []
                graph[x][y].append((y, (x + y) % len(instance)))
        return graph
    
    def max_order(graph):
        orders = {}
        visited = set()
        
        def dfs(node, parent):
            if node in visited:
                return 0
            visited.add(node)
            order = 1
            for neighbor, _ in graph[node]:
                if neighbor != parent:
                    order = max(order, 1 + dfs(neighbor, node))
            return order
        
        for node in graph:
            if node not in visited:
                orders[node] = dfs(node, None)
        
        return max(orders.values())
    
    def communication_complexity(instance):
        n = len(instance)
        complexity = 0
        for i in range(n):
            for j in range(i + 1, n):
                complexity += abs(instance[i] - instance[j])
        return complexity
    
    def gaussian_elimination(matrix):
        m, n = len(matrix), len(matrix[0])
        rank = 0
        
        for i in range(min(m, n)):
            if matrix[i][i] == 0:
                swap_found = False
                for k in range(i + 1, m):
                    if matrix[k][i] != 0:
                        matrix[i], matrix[k] = matrix[k], matrix[i]
                        swap_found = True
                        break
                if not swap_found:
                    continue
            
            pivot = matrix[i][i]
            for j in range(n):
                matrix[i][j] /= pivot
            
            for k in range(m):
                if k != i and matrix[k][i] != 0:
                    factor = matrix[k][i]
                    for j in range(n):
                        matrix[k][j] -= factor * matrix[i][j]
            
            rank += 1
        
        return rank
    
    def min_generators(graph):
        n = len(graph)
        identity = [i for i in range(n)]
        generators = []
        
        def is_group(g):
            if set(g) != set(identity):
                return False
            for x in g:
                for y in g:
                    if (x + y) % n not in g:
                        return False
            return True
        
        for i in range(1, n):
            generators.append(i)
            if is_group(generators):
                break
        
        return len(generators)
    
    def correlation_coefficient(x, y):
        mean_x = sum(x) / len(x)
        mean_y = sum(y) / len(y)
        cov_xy = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(len(x))) / len(x)
        std_x = math.sqrt(sum((x[i] - mean_x) ** 2 for i in range(len(x))) / len(x))
        std_y = math.sqrt(sum((y[i] - mean_y) ** 2 for i in range(len(y))) / len(y))
        return cov_xy / (std_x * std_y)
    
    def mean_difference(x, y):
        return sum(abs(a - b) for a, b in zip(x, y)) / len(x)
    
    n_values = [5, 10, 15, 20, 30, 40]
    g_values = []
    o_values = []
    r_values = []
    
    for n in n_values:
        instance = generate_instance(n)
        graph = cayley_graph(instance)
        g = min_generators(graph)
        o = max_order(graph)
        r = communication_complexity(instance)
        
        g_values.append(g)
        o_values.append(o)
        r_values.append(r)
    
    corr_g_r = correlation_coefficient(g_values, r_values)
    mean_diff_o_r = mean_difference(o_values, r_values)
    
    metric_name = "Correlation Coefficient (g(L), r(φ))"
    metric_value = corr_g_r
    instances_tested = len(n_values)
    n_max = max(n_values)
    conjecture_holds = corr_g_r >= 0.7 and mean_diff_o_r <= 2
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")