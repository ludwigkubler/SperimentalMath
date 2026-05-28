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

def generate_clique(n, k):
    if n < 4 or k <= 0:
        return None
    vertices = list(range(2**n))
    clique = []
    for _ in range(k):
        vertex = random.choice(vertices)
        clique.append(vertex)
    return clique

def compute_incidence_variety(clique, n):
    if len(clique) == 0 or n < 4:
        return None
    incidence_matrix = [[0] * (2**n) for _ in range(len(clique))]
    for i, vertex in enumerate(clique):
        for j in range(2**n):
            if all((j & (1 << bit)) == (vertex & (1 << bit)) for bit in range(n)):
                incidence_matrix[i][j] = 1
    return incidence_matrix

def gaussian_elimination(matrix):
    rows, cols = len(matrix), len(matrix[0])
    rank = 0
    for col in range(cols):
        pivot_row = -1
        for row in range(rank, rows):
            if matrix[row][col] != 0:
                pivot_row = row
                break
        if pivot_row == -1:
            continue
        matrix[pivot_row], matrix[rank] = matrix[rank], matrix[pivot_row]
        for r in range(rows):
            if r != rank and matrix[r][col] != 0:
                factor = Fraction(matrix[r][col], matrix[rank][col])
                for c in range(cols):
                    matrix[r][c] -= factor * matrix[rank][c]
        rank += 1
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    total_rank = 0
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""

    for n in n_values:
        for _ in range(5):  # Sample 5 instances per size
            k = random.randint(1, min(n, 4))
            clique = generate_clique(n, k)
            if clique is None:
                continue
            incidence_matrix = compute_incidence_variety(clique, n)
            if incidence_matrix is None:
                continue
            rank = gaussian_elimination(incidence_matrix)
            total_rank += rank
            instances_tested += 1

    mean_rank = Fraction(total_rank, instances_tested) if instances_tested > 0 else 0
    lower_bound = n_values[-1]**2 * math.log(n_values[-1])
    if mean_rank < lower_bound:
        conjecture_holds = False
        counterexample = f"Mean rank {mean_rank} is less than the lower bound {lower_bound}"

    return {
        "metric_name": "Minimal Rank of Hodge Structure",
        "metric_value": float(mean_rank),
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else list(range(2, 30))  # Default to first 29 primes

    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")

    if all(result["conjecture_holds"] for result in results):
        mean_rank = sum(result["metric_value"] for result in results) / len(results)
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        counterexample = next(result["counterexample"] for result in results if result["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")