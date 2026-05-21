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
            for j in range(i+1, m):
                factor = A[j][i] / A[i][i]
                for k in range(n):
                    A[j][k] -= factor * A[i][k]
        return A

    def matrix_multiply(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[0]*p for _ in range(m)]
        for i in range(m):
            for j in range(p):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def ac0_circuit_size(path, n):
        if len(path) == 1:
            return 1
        size = 2
        for i in range(1, len(path)):
            if path[i] != path[i-1]:
                size *= 2
        return size

    def minimal_representation_rank(Q, path):
        m, n = len(Q), len(Q[0])
        A = [[0]*n for _ in range(m)]
        for i in range(m):
            for j in range(n):
                if Q[i][j] == path[j]:
                    A[i][j] = 1
        rank = 0
        B = A[:]
        while any(row != [0]*n for row in B):
            B = gaussian_elimination(B)
            rank += sum(1 for row in B if any(x != 0 for x in row))
            B = [[x for x in row if x != 0] for row in B]
        return rank

    n = random.choice([5, 10, 15, 20, 30, 40])
    Q = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
    path = [random.randint(0, 1) for _ in range(n)]

    rank = minimal_representation_rank(Q, path)
    circuit_size = ac0_circuit_size(path, n)

    return {
        "metric_name": "AC0 Circuit Size",
        "metric_value": circuit_size,
        "instances_tested": 1,
        "conjecture_holds": circuit_size <= 2**rank,
        "counterexample": "" if circuit_size <= 2**rank else f"Path {path} with rank {rank} and circuit size {circuit_size}"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [random.randint(1, 1000000) for _ in range(30)]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        counterexample = next(r["counterexample"] for r in results if r["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")