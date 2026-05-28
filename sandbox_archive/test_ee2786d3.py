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
            factor = A[i][i]
            for j in range(n):
                A[i][j] /= factor
            for j in range(m):
                if j != i:
                    factor = A[j][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        return A

    def matrix_multiplication(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[0] * p for _ in range(m)]
        for i in range(m):
            for j in range(p):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def determinant(A):
        m, n = len(A), len(A[0])
        if m != n:
            raise ValueError("Matrix must be square")
        if n == 1:
            return A[0][0]
        det = 0
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for row in A[1:]]
            det += (-1) ** j * A[0][j] * determinant(submatrix)
        return det

    def rank(A):
        rref = gaussian_elimination(A)
        rank = 0
        for row in rref:
            if any(row):
                rank += 1
        return rank

    def read_twice_bp(n):
        # Generate a random read-twice branching program of size n
        bp = [[random.choice([0, 1]) for _ in range(2)] for _ in range(n)]
        return bp

    def trivial_bp(n):
        # Construct the trivial BP by IP_2
        bp = [[1] * 2 for _ in range(n)]
        return bp

    def quotient_sheaf(bp):
        m, n = len(bp), len(bp[0])
        A = [[0] * (n + 1) for _ in range(m)]
        for i in range(m):
            A[i][bp[i][0]] += 1
            A[i][bp[i][1]] -= 1
        return rank(A)

    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        bp = read_twice_bp(n)
        trivial_bp_rank = quotient_sheaf(trivial_bp(n))
        if trivial_bp_rank < n**2:
            return {
                "metric_name": "Trivial BP Rank",
                "metric_value": trivial_bp_rank,
                "instances_tested": 1,
                "conjecture_holds": False,
                "counterexample": "trivial_BP_rank_too_low"
            }
        bp_rank = quotient_sheaf(bp)
        results.append({
            "n": n,
            "bp_rank": bp_rank
        })

    mean_bp_rank = sum(result["bp_rank"] for result in results) / len(results)
    std_bp_rank = math.sqrt(sum((result["bp_rank"] - mean_bp_rank)**2 for result in results) / len(results))
    support_fraction = all(bp_rank <= math.log(2**n) for result in results)

    return {
        "metric_name": "BP Quotient Sheaf Rank",
        "metric_value": mean_bp_rank,
        "instances_tested": len(results),
        "conjecture_holds": support_fraction,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_bp_rank = sum(result["metric_value"] for result in results) / len(results)
    std_bp_rank = math.sqrt(sum((result["metric_value"] - mean_bp_rank)**2 for result in results) / len(results))
    support_fraction = all(result["conjecture_holds"] for result in results)

    if support_fraction:
        print(f"RESULT: SUPPORTED mean={mean_bp_rank} std={std_bp_rank} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"trivial_BP_rank_too_low\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")