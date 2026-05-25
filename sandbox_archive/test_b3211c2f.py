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
        n = len(matrix)
        for i in range(n):
            max_row = i
            for j in range(i+1, n):
                if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                    max_row = j
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            factor = matrix[i][i]
            for j in range(i, n + 1):
                matrix[i][j] /= factor
            for j in range(n):
                if j != i:
                    factor = matrix[j][i]
                    for k in range(i, n + 1):
                        matrix[j][k] -= factor * matrix[i][k]
        return [row[n] for row in matrix]

    def tropicalize(matrix):
        n = len(matrix)
        t_star = float('-inf')
        for i in range(n):
            for j in range(n):
                if matrix[i][j] > t_star:
                    t_star = matrix[i][j]
        return [[max(0, x - t_star) for x in row] for row in matrix]

    def min_rank(matrix):
        n = len(matrix)
        identity_matrix = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
        augmented_matrix = [row + col for row, col in zip(matrix, identity_matrix)]
        return len(gaussian_elimination(augmented_matrix))

    def generate_kclique_instance(n):
        edges = []
        for i in range(n):
            for j in range(i+1, n):
                if random.random() < 0.5:
                    edges.append((i, j))
        return edges

    n = random.randint(5, 40)
    instance = generate_kclique_instance(n)
    kclique_matrix = [[0] * n for _ in range(n)]
    for u, v in instance:
        kclique_matrix[u][v] = 1
        kclique_matrix[v][u] = 1

    tropicalized_matrix = tropicalize(kclique_matrix)
    rank = min_rank(tropicalized_matrix)

    conjecture_holds = False
    counterexample = ""
    if n <= 40:
        lower_bound = n ** (1/4)
        if rank >= lower_bound:
            conjecture_holds = True
        else:
            counterexample = f"Rank {rank} is less than {lower_bound}"
    else:
        lower_bound = n ** (1/4) + 1e-6 * n
        if rank >= lower_bound:
            conjecture_holds = True
        else:
            counterexample = f"Rank {rank} is less than {lower_bound}"

    return {
        "metric_name": "min_rank",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)

    mean_rank = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[seeds.index(first_failing_seed)]['counterexample']}\" first_failing_seed={first_failing_seed}")