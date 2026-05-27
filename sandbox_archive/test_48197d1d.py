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
            max_row = i + max(range(i, m), key=lambda x: abs(A[x][i]))
            A[i], A[max_row] = A[max_row], A[i]
            for j in range(n):
                if j != i:
                    factor = A[j][i] / A[i][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        return A

    def matrix_multiply(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[0] * p for _ in range(m)]
        for i in range(m):
            for j in range(p):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def symplectic_rank(f, n):
        F = [[0] * (2**n) for _ in range(2**n)]
        for x in range(2**n):
            for y in range(2**n):
                F[x][y] = f(x ^ y)
        A = []
        for i in range(2**n):
            row = [F[i][j] for j in range(2**n) if (i & j) == 0]
            A.append(row)
        rank = 0
        for i in range(n):
            pivot_row = next((r for r, x in enumerate(A) if x[0] != 0), None)
            if pivot_row is not None:
                A[pivot_row], A[rank] = A[rank], A[pivot_row]
                rank += 1
                for j in range(rank, len(A)):
                    factor = A[j][0] / A[rank-1][0]
                    for k in range(n):
                        A[j][k] -= factor * A[rank-1][k]
        return rank

    def xor_and_tree_width(f, n):
        if n == 1:
            return 1
        x = random.randint(0, n-1)
        f1 = lambda y: f(y ^ (1 << x))
        f2 = lambda y: f(y & ~(1 << x))
        return max(xor_and_tree_width(f1, n-1), xor_and_tree_width(f2, n-1)) + 1

    def random_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]

    n = random.randint(5, 40)
    f = lambda x: random.choice([0, 1])
    # f = random_boolean_function(n)

    rank = symplectic_rank(f, n)
    width = xor_and_tree_width(f, n)

    return {
        "metric_name": "Symplectic Rank vs XOR-AND Tree Width",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": rank <= width,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    if all(r["conjecture_holds"] for r in results):
        mean = sum(r["metric_value"] for r in results) / len(results)
        std = math.sqrt(sum((r["metric_value"] - mean)**2 for r in results) / len(results))
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        counterexample = "mapping_undefined"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")