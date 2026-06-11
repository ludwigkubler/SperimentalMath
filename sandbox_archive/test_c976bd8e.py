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
        n = len(matrix)
        augmented_matrix = [row[:] + [1] for row in matrix]
        
        for i in range(n):
            pivot = augmented_matrix[i][i]
            if pivot == 0:
                # Swap with a non-zero row
                for j in range(i+1, n):
                    if augmented_matrix[j][i] != 0:
                        augmented_matrix[i], augmented_matrix[j] = augmented_matrix[j], augmented_matrix[i]
                        break
                else:
                    return None  # Singular matrix
        
            for j in range(n):
                if j == i:
                    continue
                factor = -augmented_matrix[j][i] / pivot
                for k in range(n + 1):
                    augmented_matrix[j][k] += factor * augmented_matrix[i][k]
        
        return [row[-1] for row in augmented_matrix]

    def min_index_quaternionic_kahler_metric(graph):
        n = len(graph)
        adjacency_matrix = [[0] * n for _ in range(n)]
        for u, v in graph:
            adjacency_matrix[u][v] = 1
            adjacency_matrix[v][u] = 1
        
        indices = gaussian_elimination(adjacency_matrix)
        if indices is None:
            return float('inf')
        
        min_index = max(indices)
        return min_index

    def generate_random_cnf(n):
        clauses = []
        for _ in range(n):
            literals = random.sample(range(1, n+1), 3)
            clause = [random.choice([-1, 1]) * l for l in literals]
            clauses.append(clause)
        return clauses

    def term_overlap_graph(cnf):
        n = len(cnf)
        graph = set()
        for i in range(n):
            for j in range(i+1, n):
                overlap = sum(1 for lit_i, lit_j in zip(cnf[i], cnf[j]) if lit_i == -lit_j)
                if overlap > 0:
                    graph.add((i, j))
        return graph

    def is_satisfiable(phi):
        stack = []
        assignment = [None] * len(phi)
        
        def backtrack(i):
            if i == len(phi):
                return True
            for val in [-1, 1]:
                assignment[i] = val
                if all(assignment[j] is not None or phi[j][abs(lit)-1] * val <= 0 for lit in phi[i]):
                    stack.append((i, val))
                    if backtrack(i+1):
                        return True
                    stack.pop()
            assignment[i] = None
            return False
        
        return backtrack(0)

    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        phi = generate_random_cnf(n)
        graph = term_overlap_graph(phi)
        min_index = min_index_quaternionic_kahler_metric(graph)
        
        if is_satisfiable(phi):
            complexity = (math.log2(n)) ** 0.25
        else:
            complexity = float('inf')
        
        results.append({
            "n": n,
            "min_index": min_index,
            "complexity": complexity
        })
    
    mean_min_index = sum(result["min_index"] for result in results) / len(results)
    mean_complexity = sum(result["complexity"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["min_index"] <= result["complexity"]) / len(results)
    
    return {
        "metric_name": "min_index_quaternionic_kahler_metric",
        "metric_value": mean_min_index,
        "instances_tested": len(results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": support_fraction >= 0.8,
        "counterexample": "" if support_fraction >= 0.8 else f"n={results[0]['n']}, min_index={results[0]['min_index']}, complexity={results[0]['complexity']}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_min_index = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_min_index} std=NA support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"n={results[0]['n']}, min_index={results[0]['min_index']}, complexity={results[0]['complexity']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_support")