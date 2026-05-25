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

def gaussian_elimination(A, b):
    n = len(A)
    for i in range(n):
        # Find pivot row
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        b[i], b[max_row] = b[max_row], b[i]

        # Eliminate lower entries
        for j in range(i+1, n):
            factor = A[j][i] / A[i][i]
            for k in range(i, n):
                A[j][k] -= factor * A[i][k]
            b[j] -= factor * b[i]

    # Back substitution
    x = [0] * n
    for i in range(n-1, -1, -1):
        x[i] = (b[i] - sum(A[i][j] * x[j] for j in range(i+1, n))) / A[i][i]
    return x

def rank(matrix):
    augmented_matrix = [row[:] + [0] for row in matrix]
    for i in range(len(augmented_matrix)):
        augmented_matrix[i][-1] = 1
    solution = gaussian_elimination(augmented_matrix, [0]*len(matrix))
    return sum(1 for x in solution if x != 0)

def noncommutative_tensor_product(graph1, graph2):
    n = len(graph1)
    tensor_product = [[0] * (n*n) for _ in range(n*n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                for l in range(n):
                    if graph1[i][k] and graph2[j][l]:
                        tensor_product[i*n + k][j*n + l] += 1
    return tensor_product

def minimal_rank(graph1, graph2):
    n = len(graph1)
    tensor_product = noncommutative_tensor_product(graph1, graph2)
    return rank(tensor_product)

def generate_random_graph(n):
    graph = [[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(i+1, n):
            if random.randint(0, 1) == 1:
                graph[i][j] = 1
                graph[j][i] = 1
    return graph

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    total_rank = 0
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""

    for n in n_values:
        for _ in range(5):
            graph1 = generate_random_graph(n)
            graph2 = generate_random_graph(n)
            min_rank = minimal_rank(graph1, graph2)
            total_rank += min_rank
            instances_tested += 1

            if min_rank > n * math.log(n)**2:
                conjecture_holds = False
                counterexample = f"Graph size {n}, rank {min_rank} exceeds bound {n * math.log(n)**2}"

    return {
        "metric_name": "minimal_rank",
        "metric_value": total_rank / instances_tested,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i - 1 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)

    mean_rank = sum(result["metric_value"] for result in results) / len(results)
    std_rank = math.sqrt(sum((result["metric_value"] - mean_rank)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")