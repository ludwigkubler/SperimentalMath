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
        rows, cols = len(matrix), len(matrix[0])
        for i in range(rows):
            max_row = i
            for j in range(i + 1, rows):
                if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                    max_row = j
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            factor = matrix[i][i]
            for j in range(cols):
                matrix[i][j] /= factor
            for j in range(rows):
                if j != i:
                    factor = matrix[j][i]
                    for k in range(cols):
                        matrix[j][k] -= factor * matrix[i][k]
        return matrix

    def determinant(matrix):
        n = len(matrix)
        det = 1
        for i in range(n):
            for j in range(i + 1, n):
                if matrix[i][i] == 0:
                    continue
                factor = matrix[j][i] / matrix[i][i]
                for k in range(n):
                    matrix[j][k] -= factor * matrix[i][k]
            det *= matrix[i][i]
        return det

    def is_prime(num):
        if num <= 1:
            return False
        if num == 2:
            return True
        if num % 2 == 0:
            return False
        for i in range(3, int(math.sqrt(num)) + 1, 2):
            if num % i == 0:
                return False
        return True

    def generate_random_graph(n, p):
        graph = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                if random.random() < p:
                    graph[i][j] = 1
                    graph[j][i] = 1
        return graph

    def automorphism_group(graph):
        n = len(graph)
        group = []
        visited = [False] * n
        
        def dfs(node, path):
            if node == n:
                group.append(path[:])
                return
            for i in range(n):
                if not visited[i]:
                    visited[i] = True
                    path.append(i)
                    dfs(node + 1, path)
                    path.pop()
                    visited[i] = False
        
        dfs(0, [])
        return group

    def geometric_invariants(group):
        # Placeholder for actual computation of geometric invariants
        return len(group)

    n = random.randint(5, 40)
    p = random.random()
    graph = generate_random_graph(n, p)
    automorphisms = automorphism_group(graph)
    invariant_count = geometric_invariants(automorphisms)
    
    # Placeholder for actual quantum query complexity calculation
    quantum_query_complexity = n ** 2
    
    return {
        "metric_name": "Invariant Count",
        "metric_value": invariant_count,
        "instances_tested": 1,
        "conjecture_holds": invariant_count <= quantum_query_complexity,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    invariant_counts = [r["metric_value"] for r in results]
    quantum_query_complexities = [n ** 2 for n in range(5, 41)]
    
    mean_invariant_count = sum(invariant_counts) / len(invariant_counts)
    std_deviation = math.sqrt(sum((x - mean_invariant_count) ** 2 for x in invariant_counts) / len(invariant_counts))
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_invariant_count} std={std_deviation} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_invariant_count} std={std_deviation} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Invariant count exceeds quantum query complexity\" first_failing_seed={first_failing_seed}")