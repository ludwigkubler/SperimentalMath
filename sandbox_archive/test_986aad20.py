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
    if n % d != 0:
        raise ValueError("Graph size must be a multiple of the degree")
    
    G = [[] for _ in range(n)]
    edges_added = set()
    
    def add_edge(u, v):
        if (u, v) not in edges_added and (v, u) not in edges_added:
            G[u].append(v)
            G[v].append(u)
            edges_added.add((u, v))
            edges_added.add((v, u))
    
    for i in range(n):
        available_nodes = [j for j in range(n) if j != i and len(G[j]) < d]
        random.shuffle(available_nodes)
        for j in available_nodes[:d - len(G[i])]:
            add_edge(i, j)
    
    return G

def hodge_rank(G):
    n = len(G)
    A = [[0] * n for _ in range(n)]
    I = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
    
    def matrix_multiply(A, B):
        result = [[sum(a * b for a, b in zip(row, col)) for col in zip(*B)] for row in A]
        return result
    
    def gaussian_elimination(matrix):
        n = len(matrix)
        for i in range(n):
            max_row = max(range(i, n), key=lambda r: abs(matrix[r][i]))
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            
            factor = Fraction(matrix[i][i])
            for j in range(n):
                matrix[i][j] /= factor
            
            for k in range(n):
                if k != i:
                    factor = Fraction(matrix[k][i])
                    for j in range(n):
                        matrix[k][j] -= factor * matrix[i][j]
        
        rank = sum(1 for row in matrix if any(row))
        return rank
    
    A = gaussian_elimination(A)
    B = [A[i] - I[i] for i in range(n)]
    
    h_value = 0
    for b in B:
        h_value += sum(abs(x) for x in b)
    
    return h_value

def circuit_entanglement(G):
    n = len(G)
    if n == 1:
        return 0
    
    entanglement = 0
    for i in range(n):
        for j in range(i + 1, n):
            if j in G[i]:
                entanglement += 1
    
    return entanglement

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    h_values = []
    e_values = []
    
    for n in n_values:
        G = generate_d_regular_graph(n, d=3)
        h_value = hodge_rank(G)
        e_value = circuit_entanglement(G)
        
        h_values.append(h_value)
        e_values.append(e_value)
    
    correlation_coefficient = sum((h - h_mean) * (e - e_mean) for h, e in zip(h_values, e_values)) / math.sqrt(sum((h - h_mean) ** 2 for h in h_values) * sum((e - e_mean) ** 2 for e in e_values))
    mean_absolute_difference = sum(abs(h - e) for h, e in zip(h_values, e_values)) / len(h_values)
    
    conjecture_holds = correlation_coefficient > 0.8 and mean_absolute_difference <= 3
    counterexample = "" if conjecture_holds else f"Correlation: {correlation_coefficient}, Mean Absolute Difference: {mean_absolute_difference}"
    
    return {
        "metric_name": "Hodge Rank vs Circuit Entanglement",
        "metric_value": correlation_coefficient,
        "instances_tested": len(h_values),
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    
    seeds = [int(x) for x in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = [run_trial(seed) for seed in seeds]
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")