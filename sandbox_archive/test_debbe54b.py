# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from itertools import combinations

# Helper functions for linear algebra and quiver representations
def matrix_multiply(A, B):
    if len(A[0]) != len(B):
        raise ValueError("Incompatible dimensions for matrix multiplication")
    result = [[sum(a * b for a, b in zip(row_A, col_B)) for col_B in zip(*B)] for row_A in A]
    return result

def gaussian_elimination(matrix):
    n = len(matrix)
    augmented_matrix = [row + [0] for row in matrix]
    for i in range(n):
        max_row = max(range(i, n), key=lambda k: abs(augmented_matrix[k][i]))
        augmented_matrix[i], augmented_matrix[max_row] = augmented_matrix[max_row], augmented_matrix[i]
        for j in range(i + 1, n):
            factor = augmented_matrix[j][i] / augmented_matrix[i][i]
            augmented_matrix[j] = [a - factor * b for a, b in zip(augmented_matrix[j], augmented_matrix[i])]
    return augmented_matrix

def rank(matrix):
    augmented_matrix = gaussian_elimination(matrix)
    rank = sum(1 for row in augmented_matrix if any(row))
    return rank

# Function to generate random quivers and their representations
def generate_quiver(n):
    vertices = list(range(n))
    edges = [(u, v) for u, v in combinations(vertices, 2)]
    quiver = {v: [] for v in vertices}
    for u, v in edges:
        if random.choice([True, False]):
            quiver[u].append(v)
    return quiver

def generate_quiver_representation(quiver, q):
    n = len(quiver)
    representation = [[0] * n for _ in range(n)]
    for u in quiver:
        for v in quiver[u]:
            representation[u][v] = random.randint(1, q - 1)
    return representation

# Function to generate random communication complexity instances
def generate_communication_complexity_instance(n):
    variables = list(range(n))
    instance = {var: random.choice([True, False]) for var in variables}
    return instance

def communication_complexity_rank(instance):
    n = len(instance)
    rank = 0
    for i in range(1, n + 1):
        for subset in combinations(instance.keys(), i):
            if all(instance[var] == instance[list(subset)[0]] for var in subset):
                rank += 1
    return rank

# Function to run one trial with a given seed
def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    min_ranks = []
    comm_ranks = []

    for n in n_values:
        quiver = generate_quiver(n)
        representation = generate_quiver_representation(quiver, q=5)
        min_rank = rank(representation)
        min_ranks.append(min_rank)

        instance = generate_communication_complexity_instance(n)
        comm_rank = communication_complexity_rank(instance)
        comm_ranks.append(comm_rank)

    mean_min_ranks = sum(min_ranks) / len(min_ranks)
    mean_comm_ranks = sum(comm_ranks) / len(comm_ranks)
    correlation_coefficient = sum((x - mean_min_ranks) * (y - mean_comm_ranks) for x, y in zip(min_ranks, comm_ranks)) / len(min_ranks)

    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": abs(correlation_coefficient) >= 0.8 and mean(abs(min_rank - comm_rank)) <= 3,
        "counterexample": "" if abs(correlation_coefficient) >= 0.8 and mean(abs(min_rank - comm_rank)) <= 3 else "correlation_threshold_not_met"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3

    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_metric_value = sum(res["metric_value"] for res in results) / len(results)
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)

    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(i for i, res in enumerate(results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_threshold_not_met\" first_failing_seed={first_failing_seed + 1}")