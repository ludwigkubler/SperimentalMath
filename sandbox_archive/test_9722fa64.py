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
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i
            for j in range(i+1, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            pivot = A[i][i]
            for j in range(n):
                A[i][j] /= pivot
            for j in range(m):
                if j != i:
                    factor = A[j][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        return [row[:n-1] for row in A]

    def matrix_multiplication(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[0]*p for _ in range(m)]
        for i in range(m):
            for j in range(p):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def free_probability_distribution(P):
        n = len(P)
        I = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
        M = matrix_multiplication(P, P)
        rank = gaussian_elimination(M)
        return len(rank)

    def read_twice_branching_program(size):
        return [[random.choice([0, 1]) for _ in range(size)] for _ in range(2)]

    n = random.randint(5, 40)
    P = read_twice_branching_program(n)
    rank = free_probability_distribution(P)

    return {
        "metric_name": "Rank",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": False if rank > 1.5 * n**(1/3) else True,
        "counterexample": f"Rank({n}) = {rank}, expected <= {1.5 * n**(1/3)}"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i - 1 for i in range(5, 8)]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    ranks = [r["metric_value"] for r in results]
    median_rank = sorted(ranks)[len(ranks) // 2]
    max_rank = max(ranks)
    support_fraction = sum(1 for r in results if not r["conjecture_holds"]) / len(results)

    if all(not r["conjecture_holds"] for r in results):
        print(f"RESULT: FALSIFIED counterexample='max_rank={max_rank}, median_rank={median_rank}' first_failing_seed={seeds[0]}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={sum(ranks)/len(ranks)} std={math.sqrt(sum((x - sum(ranks)/len(ranks))**2 for x in ranks) / len(ranks))} support_fraction={support_fraction}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")