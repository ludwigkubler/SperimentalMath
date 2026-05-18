# auto-injected by SEC sandbox
import itertools
import collections
import json
import os
import time
import re
from collections import defaultdict, Counter, deque
from itertools import product, combinations, permutations, chain
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import sys
import random
import math
from fractions import Fraction

def generate_truth_table(k, seed):
    random.seed(seed)
    n = 2 ** k
    min_size = 2 ** (k - 1) - 2
    max_size = 2 ** (k - 1) + 2
    size = random.randint(min_size, max_size)
    truth_table = [0] * n
    indices = random.sample(range(n), size)
    for i in indices:
        truth_table[i] = 1
    return truth_table

def generate_structured_truth_tables(k, seed):
    random.seed(seed)
    n = 2 ** k
    truth_tables = []

    # Parity function
    parity = [sum(int(bit) for bit in bin(i)[2:].zfill(k)) % 2 for i in range(n)]
    truth_tables.append(parity)

    # Inner product on k/2 + k/2 split
    half = k // 2
    inner_product = [sum(int(bit) for bit in bin(i)[2:].zfill(k)[:half]) * sum(int(bit) for bit in bin(i)[2:].zfill(k)[half:]) % 2 for i in range(n)]
    truth_tables.append(inner_product)

    # Addressing function
    addressing = [int(bin(i)[2:].zfill(k)[0]) for i in range(n)]
    truth_tables.append(addressing)

    # Majority function
    majority = [sum(int(bit) for bit in bin(i)[2:].zfill(k)) > k // 2 for i in range(n)]
    truth_tables.append(majority)

    return truth_tables

def xor_lifted_matrix(truth_table, k):
    n = 2 ** k
    matrix = [[0] * n for _ in range(n)]
    for a in range(n):
        for b in range(n):
            if truth_table[b] == 1:
                matrix[a][b] = truth_table[a ^ b]
    return matrix

def gaussian_elimination(matrix):
    n = len(matrix)
    rank = 0
    for col in range(n):
        pivot = -1
        for row in range(rank, n):
            if matrix[row][col] == 1:
                pivot = row
                break
        if pivot == -1:
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        for row in range(n):
            if row != rank and matrix[row][col] == 1:
                for c in range(col, n):
                    matrix[row][c] ^= matrix[rank][c]
        rank += 1
    return rank

def patience_sorting(sequence):
    piles = []
    for num in sequence:
        left, right = 0, len(piles)
        while left < right:
            mid = (left + right) // 2
            if piles[mid][-1] < num:
                left = mid + 1
            else:
                right = mid
        if left == len(piles):
            piles.append([num])
        else:
            piles[left].append(num)
    return len(piles)

def run_trial(seed):
    random.seed(seed)
    k_values = [3, 4, 5]
    metric_values = []
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""

    for k in k_values:
        # Generate random truth tables
        for _ in range(50):
            truth_table = generate_truth_table(k, random.randint(0, 2**32 - 1))
            matrix = xor_lifted_matrix(truth_table, k)
            rank = gaussian_elimination([row.copy() for row in matrix])

            mu_values = []
            for a in range(2 ** k):
                row_permutation = [b ^ a for b in range(2 ** k) if truth_table[b] == 1]
                mu = patience_sorting(row_permutation)
                mu_values.append(mu)

            mu = max(mu_values)
            rho = mu / (rank + 1)
            metric_values.append(rho)
            instances_tested += 1

            if rho > 1:
                conjecture_holds = False
                counterexample = f"k={k}, truth_table={truth_table}, mu={mu}, rank={rank}, rho={rho}"

        # Generate structured truth tables
        structured_truth_tables = generate_structured_truth_tables(k, seed)
        for truth_table in structured_truth_tables:
            matrix = xor_lifted_matrix(truth_table, k)
            rank = gaussian_elimination([row.copy() for row in matrix])

            mu_values = []
            for a in range(2 ** k):
                row_permutation = [b ^ a for b in range(2 ** k) if truth_table[b] == 1]
                mu = patience_sorting(row_permutation)
                mu_values.append(mu)

            mu = max(mu_values)
            rho = mu / (rank + 1)
            metric_values.append(rho)
            instances_tested += 1

            if rho > 1:
                conjecture_holds = False
                counterexample = f"k={k}, truth_table={truth_table}, mu={mu}, rank={rank}, rho={rho}"

    if not metric_values:
        return {
            "metric_name": "rho",
            "metric_value": 0.0,
            "instances_tested": 0,
            "conjecture_holds": True,
            "counterexample": ""
        }

    mean_rho = sum(metric_values) / len(metric_values)
    max_rho = max(metric_values)

    return {
        "metric_name": "rho",
        "metric_value": mean_rho,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = sys.argv[1:]
    if not seeds:
        seeds = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]

    trials = []
    for seed in seeds:
        trial = run_trial(int(seed))
        trial["seed"] = int(seed)
        trials.append(trial)
        print(f"TRIAL: {trial}")

    metric_values = [trial["metric_value"] for trial in trials]
    mean_metric = sum(metric_values) / len(metric_values)
    std_metric = math.sqrt(sum((x - mean_metric) ** 2 for x in metric_values) / len(metric_values))
    support_fraction = sum(1 for trial in trials if trial["conjecture_holds"]) / len(trials)

    if all(trial["conjecture_holds"] for trial in trials):
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(trial["seed"] for trial in trials if not trial["conjecture_holds"])
        counterexample = next(trial["counterexample"] for trial in trials if not trial["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")