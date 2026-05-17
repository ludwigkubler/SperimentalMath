# auto-injected by SEC sandbox
import json
import os
import time
import re
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import sys
import random
import math
import itertools
from collections import defaultdict

def generate_random_matrix(n, rho, seed):
    random.seed(seed)
    matrix = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if random.random() < rho:
                matrix[i][j] = 1
    return matrix

def is_permutation_matrix(matrix):
    n = len(matrix)
    for i in range(n):
        row_sum = sum(matrix[i])
        if row_sum != 1:
            return False
    for j in range(n):
        col_sum = sum(matrix[i][j] for i in range(n))
        if col_sum != 1:
            return False
    return True

def get_permutation_matrix(matrix):
    n = len(matrix)
    perm = [-1] * n
    for i in range(n):
        for j in range(n):
            if matrix[i][j] == 1:
                perm[i] = j
                break
    return perm

def get_cycle_type(perm):
    n = len(perm)
    visited = [False] * n
    cycle_lengths = []
    for i in range(n):
        if not visited[i]:
            cycle_length = 0
            j = i
            while not visited[j]:
                visited[j] = True
                j = perm[j]
                cycle_length += 1
            cycle_lengths.append(cycle_length)
    cycle_lengths.sort(reverse=True)
    return tuple(cycle_lengths)

def murnaghan_nakayama(n, lambda_partition):
    if n == 0:
        return 1 if lambda_partition == () else 0
    if not lambda_partition:
        return 0
    total = 0
    for i in range(len(lambda_partition)):
        new_partition = list(lambda_partition)
        new_partition[i] -= 1
        new_partition = tuple(sorted((x for x in new_partition if x > 0), reverse=True))
        total += (-1) ** (n - 1 - i) * murnaghan_nakayama(n - 1, new_partition)
    return total

def compute_immanant(matrix, lambda_partition):
    n = len(matrix)
    if n != sum(lambda_partition):
        return 0
    if n == 1:
        return matrix[0][0] if lambda_partition == (1,) else 0
    total = 0
    for perm in itertools.permutations(range(n)):
        cycle_type = get_cycle_type(perm)
        if cycle_type == lambda_partition:
            product = 1
            for i in range(n):
                product *= matrix[i][perm[i]]
            total += product
    return total

def get_positivity_width(matrix):
    n = len(matrix)
    lambda_partitions = []
    for k in range(1, n + 1):
        for partition in itertools.combinations_with_replacement(range(n, 0, -1), k):
            partition = tuple(sorted(partition, reverse=True))
            if sum(partition) == n:
                lambda_partitions.append(partition)
    w = 0
    for lambda_partition in lambda_partitions:
        if compute_immanant(matrix, lambda_partition) > 0:
            w += 1
    return w

def get_kw_depth(matrix, sigma_set, cover_set):
    n = len(matrix)
    max_depth = 0
    for sigma in sigma_set:
        for cover in cover_set:
            depth = 0
            remaining_edges = set(sigma)
            while remaining_edges:
                depth += 1
                for edge in remaining_edges:
                    if edge not in cover:
                        remaining_edges.remove(edge)
                        break
            max_depth = max(max_depth, depth)
    return max_depth

def run_trial(seed):
    n_values = [3, 4, 5, 6]
    rho_values = [0.4, 0.6, 0.8]
    total_instances = 0
    total_support = 0
    metric_values = []
    counterexample = ""

    for n in n_values:
        for rho in rho_values:
            matrix = generate_random_matrix(n, rho, seed)
            if not is_permutation_matrix(matrix):
                continue
            total_instances += 1
            sigma = get_permutation_matrix(matrix)
            sigma_set = [sigma]
            w = get_positivity_width(matrix)
            cover_set = []
            for _ in range(1500):
                cover = random.sample(range(n), n - 1)
                cover_set.append(cover)
            d_kw = get_kw_depth(matrix, sigma_set, cover_set)
            metric_value = d_kw - math.ceil(math.log2(w))
            metric_values.append(metric_value)
            if d_kw < math.ceil(math.log2(w)):
                counterexample = f"n={n}, rho={rho}, d_KW={d_kw}, w={w}"
                break
            if metric_value >= 0:
                total_support += 1

    if total_instances == 0:
        return {
            "metric_name": "d_KW - log2(w)",
            "metric_value": 0.0,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "No valid matrices generated"
        }

    mean_metric = sum(metric_values) / len(metric_values)
    std_metric = math.sqrt(sum((x - mean_metric) ** 2 for x in metric_values) / len(metric_values))
    support_fraction = total_support / total_instances

    return {
        "metric_name": "d_KW - log2(w)",
        "metric_value": mean_metric,
        "instances_tested": total_instances,
        "conjecture_holds": support_fraction >= 0.95,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    total_instances = sum(result["instances_tested"] for result in results)
    total_support = sum(result["conjecture_holds"] for result in results)
    metric_values = [result["metric_value"] for result in results if result["instances_tested"] > 0]

    if total_instances == 0:
        print("RESULT: INCONCLUSIVE reason=no_valid_matrices")
        sys.exit(0)

    mean_metric = sum(metric_values) / len(metric_values)
    std_metric = math.sqrt(sum((x - mean_metric) ** 2 for x in metric_values) / len(metric_values))
    support_fraction = total_support / len(results)

    if support_fraction >= 0.95 and mean_metric >= 0:
        print(f"RESULT: SUPPORTED mean={mean_metric:.2f} std={std_metric:.2f} support_fraction={support_fraction:.2f}")
    else:
        counterexample = next((result["counterexample"] for result in results if result["counterexample"]), "")
        first_failing_seed = next((result["seed"] for result in results if not result["conjecture_holds"]), -1)
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")