# auto-injected by SEC sandbox
import collections
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
import json
from itertools import product

def hadamard(n):
    if n == 1:
        return [[1]]
    H = hadamard(n // 2)
    size = len(H)
    new_H = [[0 for _ in range(size * 2)] for _ in range(size * 2)]
    for i in range(size):
        for j in range(size):
            new_H[i][j] = H[i][j]
            new_H[i][j + size] = H[i][j]
            new_H[i + size][j] = H[i][j]
            new_H[i + size][j + size] = -H[i][j]
    return new_H

def random_bernoulli(n):
    return [[random.choice([-1, 1]) for _ in range(2**n)] for _ in range(2**n)]

def disjointness(n):
    M = [[0 for _ in range(2**n)] for _ in range(2**n)]
    for i in range(2**n):
        M[i][i] = 1
    return M

def planted_low_rank_plus_noise(n, rank=3, noise_level=0.5):
    U = [[random.choice([-1, 1]) for _ in range(rank)] for _ in range(2**n)]
    V = [[random.choice([-1, 1]) for _ in range(rank)] for _ in range(2**n)]
    M = [[sum(U[i][k] * V[j][k] for k in range(rank)) + random.gauss(0, noise_level) for j in range(2**n)] for i in range(2**n)]
    return M

def avg(M, R):
    sum_val = 0
    area = len(R)
    for r in R:
        for c in R:
            sum_val += M[r][c]
    return sum_val / area

def quadratic_variation(M, P):
    total = 0
    for R in P:
        avg_R = avg(M, R)
        if abs(avg_R) > 1/2:
            total += (avg_R ** 2) * len(R)
    return math.sqrt(total)

def generate_partitions(n):
    partitions = []
    for depth in range(1, n + 1):
        current_partition = [[i for i in range(2**n)]]
        while len(current_partition[0]) > 1:
            new_partition = []
            for R in current_partition:
                mid = len(R) // 2
                new_partition.append(R[:mid])
                new_partition.append(R[mid:])
            current_partition = new_partition
        partitions.extend(current_partition)
    return partitions

def discrepancy(M):
    n = int(math.log2(len(M)))
    if n <= 6:
        rectangles = list(product(range(2**n), repeat=4))
        min_disc = float('inf')
        for r1, c1, r2, c2 in rectangles:
            submatrix = [row[c1:c2+1] for row in M[r1:r2+1]]
            avg_val = sum(sum(row) for row in submatrix) / ((r2 - r1 + 1) * (c2 - c1 + 1))
            disc = abs(avg_val)
            if disc < min_disc:
                min_disc = disc
        return min_disc
    else:
        partitions = generate_partitions(n)
        max_disc = 0
        for partition in partitions:
            avg_val = avg(M, partition)
            if abs(avg_val) > 1/2:
                disc = (avg_val ** 2) * len(partition)
                if disc > max_disc:
                    max_disc = disc
        return math.sqrt(max_disc)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [3, 4, 5, 6, 7, 8, 9, 10]
    results = []
    
    for n in n_values:
        M = random.choice([hadamard(n), random_bernoulli(n), disjointness(n), planted_low_rank_plus_noise(n)])
        disc_M = discrepancy(M)
        Q_M = quadratic_variation(M, generate_partitions(n))
        r_M = disc_M * 2**n / Q_M
        results.append({
            "metric_name": "discrepancy_ratio",
            "metric_value": r_M,
            "instances_tested": 1,
            "conjecture_holds": r_M >= 0.4,
            "counterexample": "" if r_M >= 0.4 else f"n={n}, disc(M)={disc_M}, Q(M)={Q_M}"
        })
    
    return {
        "seed": seed,
        "metric_name": "discrepancy_ratio",
        "metric_value": sum(result["metric_value"] for result in results),
        "instances_tested": len(results),
        "conjecture_holds": all(result["conjecture_holds"] for result in results),
        "counterexample": next((result["counterexample"] for result in results if not result["conjecture_holds"]), "")
    }

if __name__ == "__main__":
    seeds = list(map(int, sys.argv[1:])) or [11, 23, 37, 53, 71]
    all_results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(json.dumps({"TRIAL": result}))
        all_results.append(result)
    
    mean_r = sum(result["metric_value"] for result in all_results) / len(all_results)
    support_fraction = sum(1 for result in all_results if result["conjecture_holds"]) / len(all_results)
    
    if support_fraction >= 0.95:
        print(f"RESULT: SUPPORTED mean={mean_r} std=0 support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in all_results):
        first_failing_seed = next(seed for seed, result in zip(seeds, all_results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{next(result['counterexample'] for result in all_results if not result['conjecture_holds'])}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient data")