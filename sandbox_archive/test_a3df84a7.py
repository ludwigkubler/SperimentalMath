# auto-injected by SEC sandbox
import collections
import json
import os
import time
import re
from collections import defaultdict, Counter, deque
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import sys
import random
import math
from itertools import product
from fractions import Fraction

def matrix_multiply(a, b):
    """Multiply two matrices over F_2."""
    n = len(a)
    m = len(b[0])
    p = len(b)
    result = [[0 for _ in range(m)] for _ in range(n)]
    for i in range(n):
        for j in range(m):
            total = 0
            for k in range(p):
                total += a[i][k] * b[k][j]
            result[i][j] = total % 2
    return result

def gaussian_elimination(matrix):
    """Compute the rank of a matrix over F_2 using Gaussian elimination."""
    rank = 0
    n = len(matrix)
    if n == 0:
        return 0
    m = len(matrix[0])
    for col in range(m):
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
                for c in range(col, m):
                    matrix[row][c] = (matrix[row][c] + matrix[rank][c]) % 2
        rank += 1
    return rank

def patience_sorting(sequence):
    """Compute the length of the longest increasing subsequence using patience sorting."""
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

def generate_random_function(k, seed):
    """Generate a random Boolean function with |S(f)| in [2^{k-1}-2, 2^{k-1}+2]."""
    random.seed(seed)
    n = 2 ** k
    min_size = 2 ** (k - 1) - 2
    max_size = 2 ** (k - 1) + 2
    size = random.randint(min_size, max_size)
    truth_table = [0] * n
    ones = random.sample(range(n), size)
    for i in ones:
        truth_table[i] = 1
    return truth_table

def generate_structured_functions(k, seed):
    """Generate structured Boolean functions."""
    random.seed(seed)
    n = 2 ** k
    functions = []
    # Parity function
    parity = [sum(int(bit) for bit in format(i, f'0{k}b')) % 2 for i in range(n)]
    functions.append(parity)
    # Inner product function
    split = k // 2
    inner_product = [sum(int(bit) for bit in format(i, f'0{k}b')[:split]) * sum(int(bit) for bit in format(i, f'0{k}b')[split:]) % 2 for i in range(n)]
    functions.append(inner_product)
    # Addressing function
    addressing = [int(format(i, f'0{k}b')[0]) for i in range(n)]
    functions.append(addressing)
    # Majority function
    majority = [int(sum(int(bit) for bit in format(i, f'0{k}b')) > k // 2) for i in range(n)]
    functions.append(majority)
    return functions

def build_xor_matrix(truth_table, k):
    """Build the XOR-lifted matrix M_{f∘XOR_k}."""
    n = 2 ** k
    matrix = [[0 for _ in range(n)] for _ in range(n)]
    for a in range(n):
        for b in range(n):
            matrix[a][b] = truth_table[(a ^ b) % n]
    return matrix

def compute_mu(truth_table, k):
    """Compute μ(f) = max_{a∈{0,1}^k} LIS(τ_a)."""
    n = 2 ** k
    max_lis = 0
    for a in range(n):
        tau_a = [(b ^ a) % n for b in range(n) if truth_table[b] == 1]
        lis = patience_sorting(tau_a)
        if lis > max_lis:
            max_lis = lis
    return max_lis

def run_trial(seed):
    """Run a single trial for the given seed."""
    random.seed(seed)
    k_values = [3, 4, 5]
    metric_values = []
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""
    for k in k_values:
        # Generate random functions
        for _ in range(50):
            truth_table = generate_random_function(k, seed)
            if sum(truth_table) < 2:
                continue
            matrix = build_xor_matrix(truth_table, k)
            rank = gaussian_elimination(matrix)
            mu = compute_mu(truth_table, k)
            rho = mu / (rank + 1)
            metric_values.append(rho)
            instances_tested += 1
            if rho > 1:
                conjecture_holds = False
                counterexample = f"k={k}, truth_table={truth_table}, mu={mu}, rank={rank}, rho={rho}"
                break
        if not conjecture_holds:
            break
        # Generate structured functions
        structured_functions = generate_structured_functions(k, seed)
        for truth_table in structured_functions:
            if sum(truth_table) < 2:
                continue
            matrix = build_xor_matrix(truth_table, k)
            rank = gaussian_elimination(matrix)
            mu = compute_mu(truth_table, k)
            rho = mu / (rank + 1)
            metric_values.append(rho)
            instances_tested += 1
            if rho > 1:
                conjecture_holds = False
                counterexample = f"k={k}, truth_table={truth_table}, mu={mu}, rank={rank}, rho={rho}"
                break
        if not conjecture_holds:
            break
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
        "counterexample": counterexample if not conjecture_holds else ""
    }

if __name__ == "__main__":
    seeds = sys.argv[1:]
    if not seeds:
        seeds = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    trials = []
    for seed in seeds:
        trial = run_trial(int(seed))
        trials.append(trial)
        print(f"TRIAL: {trial}")
    metric_values = [trial["metric_value"] for trial in trials if trial["instances_tested"] > 0]
    if not metric_values:
        print("RESULT: INCONCLUSIVE reason=no_valid_instances")
        sys.exit(0)
    mean = sum(metric_values) / len(metric_values)
    std = math.sqrt(sum((x - mean) ** 2 for x in metric_values) / len(metric_values))
    support_fraction = sum(1 for trial in trials if trial["conjecture_holds"]) / len(trials)
    if all(trial["conjecture_holds"] for trial in trials):
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(trial["seed"] for trial in trials if not trial["conjecture_holds"])
        counterexample = next(trial["counterexample"] for trial in trials if not trial["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")