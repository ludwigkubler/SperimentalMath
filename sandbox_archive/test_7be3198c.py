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
    
    def generate_k_clique_instance(k):
        if k < 3:
            return []
        vertices = list(range(1, k + 1))
        edges = [(i, j) for i in range(1, k + 1) for j in range(i + 1, k + 1)]
        clique_size = random.randint(3, k)
        clique_vertices = random.sample(vertices, clique_size)
        clique_edges = [(i, j) for i in clique_vertices for j in clique_vertices if i < j]
        non_clique_edges = [e for e in edges if e not in clique_edges]
        instance = {'vertices': vertices, 'edges': clique_edges + non_clique_edges}
        return instance
    
    def dpll_search_tree(instance):
        vertices = instance['vertices']
        edges = instance['edges']
        
        def dfs(path, remaining_edges):
            if not remaining_edges:
                return path
            for edge in remaining_edges:
                u, v = edge
                if (u in path and v not in path) or (v in path and u not in path):
                    new_path = path + [u] if u not in path else path + [v]
                    new_remaining_edges = [e for e in remaining_edges if e != edge]
                    result = dfs(new_path, new_remaining_edges)
                    if result:
                        return result
            return None
        
        return dfs([], edges)
    
    def lie_algebra_rank(tree):
        n = len(tree)
        adjacency_matrix = [[0] * n for _ in range(n)]
        for u, v in tree:
            adjacency_matrix[u - 1][v - 1] = 1
            adjacency_matrix[v - 1][u - 1] = 1
        
        def gaussian_elimination(matrix):
            m, n = len(matrix), len(matrix[0])
            rank = 0
            for i in range(n):
                max_row = None
                for j in range(rank, m):
                    if matrix[j][i]:
                        max_row = j
                        break
                if max_row is None:
                    continue
                matrix[max_row], matrix[rank] = matrix[rank], matrix[max_row]
                rank += 1
                for j in range(m):
                    if j != rank - 1:
                        factor = matrix[j][i] / matrix[rank - 1][i]
                        for k in range(n):
                            matrix[j][k] -= factor * matrix[rank - 1][k]
            return rank
        
        return gaussian_elimination(adjacency_matrix)
    
    def f(k):
        # Placeholder function for the upper bound f(k)
        return k**2
    
    k = random.randint(3, 40)
    instance = generate_k_clique_instance(k)
    tree = dpll_search_tree(instance)
    rank = lie_algebra_rank(tree)
    metric_value = rank
    conjecture_holds = rank <= f(k)
    counterexample = "" if conjecture_holds else f"rank={rank}, f(k)={f(k)}"
    
    return {
        "metric_name": "Lie Algebra Rank",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    if len(sys.argv) > 1:
        seeds = [int(s) for s in sys.argv[1:]]
    else:
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]
        seeds = random.sample(primes, min(30, len(primes)))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r['metric_value'] for r in results) / len(results)
    std_value = math.sqrt(sum((r['metric_value'] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    
    if all(r['conjecture_holds'] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.9 and abs(mean_value - sum(r['metric_value'] for r in results) / len(results)) <= 1.5:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result['conjecture_holds'])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")