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

def cycle_type(perm):
    cycles = []
    visited = [False] * len(perm)
    for i in range(len(perm)):
        if not visited[i]:
            cycle = []
            j = i
            while not visited[j]:
                visited[j] = True
                cycle.append(j)
                j = perm[j]
            cycles.append(tuple(sorted(cycle)))
    return tuple(sorted(cycles))

def murnaghan_nakayama(n):
    if n == 0:
        return {(): 1}
    if n == 1:
        return {(1,): 1}

    prev = murnaghan_nakayama(n - 1)
    current = defaultdict(int)

    for partition, value in prev.items():
        for i in range(len(partition)):
            new_partition = list(partition)
            new_partition[i] += 1
            new_partition = tuple(sorted(new_partition, reverse=True))
            current[new_partition] += value

        if len(partition) < n:
            new_partition = list(partition) + [1]
            new_partition = tuple(sorted(new_partition, reverse=True))
            current[new_partition] += value

    return dict(current)

def immanant_lambda(M, lambda_partition):
    n = len(M)
    chi = murnaghan_nakayama(n)
    if lambda_partition not in chi:
        return 0

    total = 0
    for perm in itertools.permutations(range(n)):
        ct = cycle_type(perm)
        if ct == lambda_partition:
            product = 1
            for i in range(n):
                product *= M[i][perm[i]]
            total += product * chi[lambda_partition]

    return total

def compute_variance(M):
    n = len(M)
    chi = murnaghan_nakayama(n)
    lambda_partitions = list(chi.keys())

    immanants = []
    for lambda_partition in lambda_partitions:
        I = immanant_lambda(M, lambda_partition)
        if I != 0:
            immanants.append(math.log2(1 + abs(I)))

    if not immanants:
        return 0.0

    mean = sum(immanants) / len(immanants)
    variance = sum((x - mean) ** 2 for x in immanants) / len(immanants)
    return variance

def generate_random_matrix(n, seed):
    random.seed(seed)
    return [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]

def generate_padded_matrix(n, seed):
    random.seed(seed)
    m = (n + 1) // 2
    M_prime = [[random.randint(0, 1) for _ in range(m)] for _ in range(m)]
    J = [[1 for _ in range(n - m)] for _ in range(n - m)]

    M_pad = [[0 for _ in range(n)] for _ in range(n)]
    for i in range(m):
        for j in range(m):
            M_pad[i][j] = M_prime[i][j]

    for i in range(n - m):
        for j in range(n - m):
            M_pad[m + i][m + j] = J[i][j]

    return M_pad

def run_trial(seed):
    n_values = [5, 6, 7]
    metric_values = []
    conjecture_holds_list = []
    counterexamples = []

    for n in n_values:
        M = generate_random_matrix(n, seed)
        M_pad = generate_padded_matrix(n, seed)

        V_uniform = compute_variance(M)
        V_padded = compute_variance(M_pad)

        metric_values.append((V_uniform, V_padded))
        conjecture_holds = V_uniform >= 4 * V_padded
        conjecture_holds_list.append(conjecture_holds)

        if not conjecture_holds:
            counterexamples.append(f"n={n}, seed={seed}, V_uniform={V_uniform}, V_padded={V_padded}")

    metric_value = sum(V_uniform for V_uniform, _ in metric_values) / len(metric_values)
    instances_tested = len(n_values)
    conjecture_holds = all(conjecture_holds_list)
    counterexample = "\n".join(counterexamples) if counterexamples else ""

    return {
        "metric_name": "log_variance_ratio",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]

    results = []
    for seed in seeds:
        result = run_trial(seed)
        result["seed"] = seed
        print(f"TRIAL: {result}")
        results.append(result)

    metric_values = [r["metric_value"] for r in results]
    mean_metric = sum(metric_values) / len(metric_values)
    std_metric = math.sqrt(sum((x - mean_metric) ** 2 for x in metric_values) / len(metric_values))

    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)

    if support_fraction >= 0.9:
        print(f"RESULT: SUPPORTED mean={mean_metric:.4f} std={std_metric:.4f} support_fraction={support_fraction:.4f}")
    else:
        counterexamples = [r["counterexample"] for r in results if r["counterexample"]]
        if counterexamples:
            first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
            print(f"RESULT: FALSIFIED counterexample=\"{counterexamples[0]}\" first_failing_seed={first_failing_seed}")
        else:
            print("RESULT: INCONCLUSIVE reason=insufficient_support")