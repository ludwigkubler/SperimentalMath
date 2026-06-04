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
from fractions import Fraction
import math

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def gaussian_elimination(matrix):
        n = len(matrix)
        rank = 0
        
        for i in range(n):
            if rank >= n:
                break
            
            max_row = rank
            for j in range(rank + 1, n):
                if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                    max_row = j
            
            matrix[rank], matrix[max_row] = matrix[max_row], matrix[rank]
            
            factor = Fraction(1, matrix[rank][i])
            for j in range(n):
                matrix[rank][j] *= factor
            
            for j in range(n):
                if j != rank:
                    factor = -matrix[j][i]
                    for k in range(n):
                        matrix[j][k] += factor * matrix[rank][k]
            
            rank += 1
        
        return rank
    
    def minimal_tropical_motivic_rank(clauses):
        n = len(clauses)
        m = len(clauses[0])
        
        # Convert clauses to a matrix
        matrix = [[Fraction(0, 1)] * (m + 1) for _ in range(n)]
        for i in range(n):
            for j in range(m):
                if clauses[i][j] == '1':
                    matrix[i][j] = Fraction(1, 1)
                elif clauses[i][j] == '0':
                    matrix[i][j] = Fraction(-math.inf, 1)
        
        return gaussian_elimination(matrix)
    
    def communication_complexity_rank(clauses):
        n = len(clauses)
        m = len(clauses[0])
        
        # Convert clauses to a tree structure
        tree = [[] for _ in range(n)]
        for i in range(n):
            for j in range(m):
                if clauses[i][j] == '1':
                    tree[j].append(i)
        
        # Depth-first search to find the maximum depth of the tree
        def dfs(node, depth):
            max_depth = depth
            for neighbor in tree[node]:
                max_depth = max(max_depth, dfs(neighbor, depth + 1))
            return max_depth
        
        return max(dfs(i, 0) for i in range(n))
    
    def generate_d_regular_graph(d, n):
        if d * n % 2 != 0:
            raise ValueError("Graph size must be a multiple of the degree")
        
        graph = [[] for _ in range(n)]
        edges = set()
        while len(edges) < (d * n) // 2:
            u = random.randint(0, n - 1)
            v = random.randint(0, n - 1)
            if u != v and (u, v) not in edges and (v, u) not in edges:
                graph[u].append(v)
                graph[v].append(u)
                edges.add((u, v))
        
        return graph
    
    def tseitin_formula(graph):
        n = len(graph)
        m = 2 * n - 1
        clauses = []
        
        # Add clauses for each vertex
        for i in range(n):
            clauses.append(['x' + str(i)])
            for j in range(len(graph[i])):
                clauses.append(['x' + str(i), 'x' + str(graph[i][j])])
                clauses.append(['-x' + str(i), '-x' + str(graph[i][j])])
        
        # Add clauses for each edge
        for i in range(n):
            for j in range(len(graph[i])):
                clauses.append(['-x' + str(i), 'x' + str(j)])
        
        return clauses
    
    def correlation_coefficient(x, y):
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        
        numerator = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n))
        denominator = math.sqrt(sum((x[i] - mean_x) ** 2 for i in range(n))) * math.sqrt(sum((y[i] - mean_y) ** 2 for i in range(n)))
        
        return numerator / denominator
    
    d_values = [3, 4, 5, 6, 7, 8]
    mtr_C_values = []
    CR_values = []
    
    for d in d_values:
        n = d * 10
        graph = generate_d_regular_graph(d, n)
        clauses = tseitin_formula(graph)
        
        mtr_C = minimal_tropical_motivic_rank(clauses)
        CR = communication_complexity_rank(clauses)
        
        mtr_C_values.append(mtr_C)
        CR_values.append(CR)
    
    correlation = correlation_coefficient(mtr_C_values, [CR ** 2 for CR in CR_values])
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation,
        "instances_tested": len(d_values),
        "n_max": max([d * 10 for d in d_values]),
        "conjecture_holds": abs(correlation) >= 0.95,  # Threshold set to 0.95
        "counterexample": "" if abs(correlation) >= 0.95 else f"correlation_coefficient={correlation}"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient={result['counterexample']}\" first_failing_seed={first_failing_seed}")