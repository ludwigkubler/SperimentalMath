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
    
    def generate_random_graph(n):
        edges = set()
        for i in range(n):
            for j in range(i + 1, n):
                if random.random() < 0.5:
                    edges.add((i, j))
        return edges
    
    def tensor_product(graph1, graph2):
        n = len(graph1)
        m = len(graph2)
        result = [[0] * (m * n) for _ in range(n * m)]
        
        for i, j in graph1:
            for k, l in graph2:
                result[i * m + k][j * n + l] += 1
        
        return result
    
    def rank(matrix):
        m = len(matrix)
        n = len(matrix[0])
        augmented_matrix = [row[:] + [1 if i == j else 0 for j in range(n)] for i, row in enumerate(matrix)]
        
        def gaussian_elimination(A, b):
            rows, cols = len(A), len(A[0])
            for i in range(rows):
                max_row = i
                for j in range(i + 1, rows):
                    if abs(A[j][i]) > abs(A[max_row][i]):
                        max_row = j
                
                A[i], A[max_row] = A[max_row], A[i]
                b[i], b[max_row] = b[max_row], b[i]
                
                factor = Fraction(1, A[i][i])
                for j in range(cols):
                    A[i][j] *= factor
                b[i] *= factor
                
                for j in range(rows):
                    if i != j:
                        factor = A[j][i]
                        for k in range(cols):
                            A[j][k] -= factor * A[i][k]
                        b[j] -= factor * b[i]
            
            return [b[i][-1] for i in range(rows)]
        
        solution = gaussian_elimination(augmented_matrix, [0]*len(matrix))
        rank = sum(1 for x in solution if x != 0)
        return rank
    
    n = random.randint(5, 40)
    graph1 = generate_random_graph(n)
    graph2 = generate_random_graph(n)
    
    min_rank = rank(tensor_product(graph1, graph2))
    
    metric_value = min_rank
    instances_tested = 1
    conjecture_holds = False
    counterexample = ""
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    
    seeds = [int(x) for x in sys.argv[1:]] if sys.argv[1:] else list(range(2, 30)) + list(map(lambda p: int(p), filter(str.isdigit, open('primes.txt').read())))
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")