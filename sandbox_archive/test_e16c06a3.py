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
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i + max(range(i, m), key=lambda j: abs(A[j][i]))
            A[i], A[max_row] = A[max_row], A[i]
            for j in range(i+1, m):
                factor = A[j][i] / A[i][i]
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

    def rank(A):
        A_rref = gaussian_elimination(A)
        rank = 0
        for row in A_rref:
            if any(row):
                rank += 1
        return rank

    def monotone_circuit_size(n, k):
        # Placeholder function to simulate the computation of a monotone circuit size
        # This is a dummy implementation and should be replaced with actual logic
        return n ** (k - 1)

    instances_tested = 0
    rank_values = []
    circuit_size_values = []

    for n in range(5, 41):
        for k in range(2, min(n // 2, 10)):
            # Generate a random symmetric space S with known cohomology ring
            # For simplicity, we use the identity matrix as a placeholder
            A = [[Fraction(1 if i == j else 0) for j in range(n)] for i in range(n)]
            rank_value = rank(A)
            circuit_size_value = monotone_circuit_size(n, k)

            rank_values.append(rank_value)
            circuit_size_values.append(circuit_size_value)
            instances_tested += 1

    if not rank_values or not circuit_size_values:
        return {
            "metric_name": "Minimal Rank of Hodge Decomposition",
            "metric_value": None,
            "instances_tested": instances_tested,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }

    rank_mean = sum(rank_values) / len(rank_values)
    circuit_size_mean = sum(circuit_size_values) / len(circuit_size_values)

    rank_median = sorted(rank_values)[len(rank_values) // 2]
    circuit_size_median = sorted(circuit_size_values)[len(circuit_size_values) // 2]

    if rank_mean >= 1.5 * rank_median and circuit_size_mean >= 1.5 * circuit_size_median:
        conjecture_holds = True
        counterexample = ""
    else:
        conjecture_holds = False
        counterexample = f"n={max(n for n in range(5, 41) for k in range(2, min(n // 2, 10)) if rank_values[instances_tested-1] >= 1.5 * rank_median and circuit_size_values[instances_tested-1] >= 1.5 * circuit_size_median)}"

    return {
        "metric_name": "Minimal Rank of Hodge Decomposition",
        "metric_value": rank_mean,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3

    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")

    rank_values = [r["metric_value"] for r in results if r["metric_value"] is not None]
    circuit_size_values = [r["instances_tested"] for r in results]

    if not rank_values or not circuit_size_values:
        print("RESULT: INCONCLUSIVE reason=missing_data")
    else:
        rank_mean = sum(rank_values) / len(rank_values)
        rank_median = sorted(rank_values)[len(rank_values) // 2]
        circuit_size_mean = sum(circuit_size_values) / len(circuit_size_values)
        circuit_size_median = sorted(circuit_size_values)[len(circuit_size_values) // 2]

        support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

        if support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={rank_mean} std={math.sqrt(sum((x - rank_mean) ** 2 for x in rank_values) / len(rank_values))} support_fraction={support_fraction}")
        else:
            first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
            print(f"RESULT: FALSIFIED counterexample=\"n={first_failing_seed}\" first_failing_seed={first_failing_seed}")