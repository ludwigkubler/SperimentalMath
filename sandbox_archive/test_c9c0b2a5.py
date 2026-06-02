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

def gaussian_elimination(matrix):
    n = len(matrix)
    augmented_matrix = [row[:] + [0] for row in matrix]
    for i in range(n):
        if matrix[i][i] == 0:
            for j in range(i+1, n):
                if matrix[j][i] != 0:
                    matrix[i], matrix[j] = matrix[j], matrix[i]
                    augmented_matrix[i], augmented_matrix[j] = augmented_matrix[j], augmented_matrix[i]
                    break
        if matrix[i][i] == 0:
            continue
        factor = Fraction(1, matrix[i][i])
        for j in range(i, n + 1):
            augmented_matrix[i][j] *= factor
        for j in range(n):
            if j != i and matrix[j][i] != 0:
                factor = -matrix[j][i]
                for k in range(i, n + 1):
                    augmented_matrix[j][k] += factor * augmented_matrix[i][k]
    return [row[n:] for row in augmented_matrix]

def rank(matrix):
    augmented_matrix = gaussian_elimination(matrix)
    rank = 0
    for row in augmented_matrix:
        if any(row):
            rank += 1
    return rank

def generate_quiver(n):
    quiver = {}
    for i in range(n):
        for j in range(n):
            if i != j and random.random() < 0.5:
                quiver[(i, j)] = random.randint(1, 10)
    return quiver

def generate_communication_complexity_instance(n):
    instance = [random.randint(1, 10) for _ in range(n)]
    return instance

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    min_rank_sum = 0
    communication_complexity_rank_sum = 0
    instances_tested = 0
    n_max = 0

    for n in n_values:
        quiver = generate_quiver(n)
        representation = [[quiver.get((i, j), 0) for j in range(n)] for i in range(n)]
        min_rank = rank(representation)
        min_rank_sum += min_rank
        instances_tested += n

        communication_complexity_instance = generate_communication_complexity_instance(n)
        communication_complexity_rank = sum(communication_complexity_instance)
        communication_complexity_rank_sum += communication_complexity_rank
        instances_tested += n

        n_max = max(n_max, n)

    mean_min_rank = min_rank_sum / instances_tested
    mean_communication_complexity_rank = communication_complexity_rank_sum / instances_tested
    correlation_coefficient = (instances_tested * sum(min_rank * communication_complexity_rank for min_rank, communication_complexity_rank in zip(min_ranks, communication_complexity_ranks)) - min_rank_sum * communication_complexity_rank_sum) / math.sqrt(instances_tested * sum(min_rank ** 2 for min_rank in min_ranks) - min_rank_sum ** 2) * math.sqrt(instances_tested * sum(communication_complexity_rank ** 2 for communication_complexity_rank in communication_complexity_ranks) - communication_complexity_rank_sum ** 2)

    conjecture_holds = correlation_coefficient >= 0.8 and max(abs(min_rank - communication_complexity_rank) for min_rank, communication_complexity_rank in zip(min_ranks, communication_complexity_ranks)) <= 3
    counterexample = "" if conjecture_holds else "correlation_coefficient < 0.8 or mean(|min_rank - communication_complexity_rank|) > 3"

    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(seed) for seed in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...{result}...}}")
        results.append(result)

    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")