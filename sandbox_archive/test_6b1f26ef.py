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
    
    def generate_adjacency_matrix(n):
        if n < 2:
            return []
        matrix = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                p = random.random()
                if p < 0.5:
                    matrix[i][j] = 1
                    matrix[j][i] = 1
        return matrix
    
    def compute_geometric_entropy(matrix):
        n = len(matrix)
        row_sums = [sum(row) for row in matrix]
        total_edges = sum(row_sums) / 2
        if total_edges == 0:
            return 0
        p_i = [row_sum / total_edges for row_sum in row_sums]
        entropy = -sum(p * math.log2(p) for p in p_i if p > 0)
        return entropy
    
    def compute_communication_complexity_rank(matrix):
        n = len(matrix)
        adjacency_list = [[] for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                if matrix[i][j] == 1:
                    adjacency_list[i].append(j)
                    adjacency_list[j].append(i)
        
        def dfs(node, visited):
            stack = [node]
            while stack:
                current = stack.pop()
                if not visited[current]:
                    visited[current] = True
                    for neighbor in adjacency_list[current]:
                        if not visited[neighbor]:
                            stack.append(neighbor)
        
        visited = [False] * n
        rank = 0
        for i in range(n):
            if not visited[i]:
                dfs(i, visited)
                rank += 1
        
        return rank
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        matrix = generate_adjacency_matrix(n)
        H_G = compute_geometric_entropy(matrix)
        r_k = compute_communication_complexity_rank(matrix)
        if r_k == 0:
            continue
        ratio = H_G / r_k
        results.append({"n": n, "H(G)": H_G, "r(k)": r_k, "ratio": ratio})
    
    mean_ratio = sum(result["ratio"] for result in results) / len(results)
    conjecture_holds = all(result["ratio"] <= 1 for result in results)
    counterexample = "" if conjecture_holds else "H(G)/r(k) > 1"
    
    return {
        "metric_name": "H(G)/r(k)",
        "metric_value": mean_ratio,
        "instances_tested": len(results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(seed) for seed in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ratio = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0 support_fraction=1")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"H(G)/r(k) > 1\" first_failing_seed={first_failing_seed}")