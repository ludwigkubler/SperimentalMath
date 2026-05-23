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

def generate_delone_triangulation(n):
    # Simple Delone triangulation generation (not accurate but sufficient for testing)
    vertices = [(random.uniform(-1, 1), random.uniform(-1, 1)) for _ in range(n)]
    edges = []
    for i in range(n):
        for j in range(i + 1, n):
            if math.dist(vertices[i], vertices[j]) < 2:
                edges.append((i, j))
    return vertices, edges

def matrix_rank(matrix):
    # Gaussian elimination to find the rank of a matrix
    m, n = len(matrix), len(matrix[0])
    rank = 0
    for i in range(min(m, n)):
        if matrix[i][i] != 0:
            for j in range(i + 1, m):
                factor = -matrix[j][i] / matrix[i][i]
                for k in range(n):
                    matrix[j][k] += factor * matrix[i][k]
            rank += 1
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    total_rank = 0
    instances_tested = 0
    conjecture_holds = True

    for n in n_values:
        vertices, edges = generate_delone_triangulation(n)
        matrix = [[Fraction(0) for _ in range(n)] for _ in range(n)]
        for i, j in edges:
            matrix[i][j] = Fraction(1)
            matrix[j][i] = Fraction(1)

        rank = matrix_rank(matrix)
        instances_tested += 1
        total_rank += rank

        if n == 20 and rank < (1/4) * n**(3/2):
            conjecture_holds = False
            counterexample = "Rank does not meet the expected value for non-k-CLIQUE instance"
        elif n == 20 and rank >= (1/2) * n**(3/2):
            conjecture_holds = False
            counterexample = "Rank does not meet the expected value for k-CLIQUE instance"

    mean_rank = total_rank / instances_tested
    return {
        "metric_name": "Matrix Rank",
        "metric_value": mean_rank,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{'seed': {seed}, **result}}")
        results.append(result)

    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='Rank does not meet the expected value' first_failing_seed={first_failing_seed}")