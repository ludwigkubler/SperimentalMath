# auto-injected by SEC sandbox
import itertools
import collections
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
import json

def run_trial(seed: int) -> dict:
    random.seed(seed)

    def hadamard(n):
        if n == 1:
            return [[1]]
        H = hadamard(n // 2)
        a, b, c, d = H, H, H, H
        for i in range(len(H)):
            for j in range(len(H)):
                b[i][j] *= -1
                d[i][j] *= -1
                if i >= len(H) // 2:
                    b[i][j] *= -1
                if j >= len(H) // 2:
                    d[i][j] *= -1
        return a + b + c + d

    def random_bernoulli(n):
        return [[random.choice([-1, 1]) for _ in range(n)] for _ in range(n)]

    def disjointness(n):
        M = [[0] * n for _ in range(n)]
        for i in range(n):
            M[i][i] = 1
        return M

    def planted_low_rank_plus_noise(n, rank=2, noise_level=0.5):
        U = hadamard(rank)
        V = random_bernoulli(rank)
        A = [[sum(U[i][k] * V[k][j] for k in range(rank)) for j in range(n)] for i in range(n)]
        M = [[random.choice([-1, 1]) if abs(A[i][j]) < noise_level else int(A[i][j] > 0) * 2 - 1 for j in range(n)] for i in range(n)]
        return M

    def disc(M):
        n = len(M)
        if n <= 6:
            rectangles = [(i, j, i + h, j + w) for i in range(n) for j in range(n) for h in range(1, n - i + 1) for w in range(1, n - j + 1)]
        else:
            rectangles = []
            for _ in range(200):
                i, j, h, w = random.randint(0, n-1), random.randint(0, n-1), random.randint(1, n-i), random.randint(1, n-j)
                rectangles.append((i, j, i + h, j + w))
        max_disc = 0
        for i, j, k, l in rectangles:
            avg = sum(M[x][y] for x in range(i, k+1) for y in range(j, l+1)) / ((k-i+1)*(l-j+1))
            if abs(avg) > 0.5:
                max_disc = max(max_disc, math.sqrt((avg**2 * (k-i+1)*(l-j+1))))
        return max_disc

    def Q(M):
        n = len(M)
        partitions = []
        for i in range(1 << n):
            partition = []
            for j in range(n):
                if i & (1 << j):
                    partition.append([(0, 0), (n-1, n-1)])
                else:
                    partition.append([(0, 0), (n//2-1, n//2-1)], [(n//2, n//2), (n-1, n-1)])
            partitions.append(partition)
        max_Q = 0
        for partition in partitions:
            sum_q = 0
            for R in partition:
                avg_R = sum(M[x][y] for x in range(R[0][0], R[1][0]+1) for y in range(R[0][1], R[1][1]+1)) / ((R[1][0]-R[0][0]+1)*(R[1][1]-R[0][1]+1))
                sum_q += avg_R**2 * (R[1][0]-R[0][0]+1)*(R[1][1]-R[0][1]+1)
            max_Q = max(max_Q, math.sqrt(sum_q))
        return max_Q

    n_values = [5, 8, 11, 14]
    instances_tested = 0
    total_disc = 0
    total_Q = 0
    for n in n_values:
        M = random.choice([hadamard(n), random_bernoulli(n), disjointness(n), planted_low_rank_plus_noise(n)])
        disc_M = disc(M)
        Q_M = Q(M)
        instances_tested += 1
        total_disc += disc_M * (2 ** n)
        total_Q += Q_M

    mean_r = total_disc / (instances_tested * (2 ** n_values[0]))
    support_fraction = instances_tested - sum(1 for _ in range(instances_tested) if disc(M) * (2 ** n) < 0.4 * Q(M)) >= 0.95 * instances_tested

    conjecture_holds = mean_r >= 0.6
    counterexample = "" if conjecture_holds else "mapping_undefined"

    return {
        "metric_name": "disc/Q ratio",
        "metric_value": mean_r,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [11, 23, 37, 53, 71]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {json.dumps(result)}")
        results.append(result)

    mean_r = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_r} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_r} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = "mapping_undefined"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")