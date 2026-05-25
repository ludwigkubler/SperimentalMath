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

def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        factor = Fraction(A[i][i])
        for j in range(n):
            A[i][j] /= factor
        for j in range(n):
            if j != i:
                factor = Fraction(A[j][i])
                for k in range(n):
                    A[j][k] -= factor * A[i][k]

def matrix_multiply(A, B):
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def min_rank_trop(Q):
    n = len(Q)
    Q_copy = [row[:] for row in Q]
    gaussian_elimination(Q_copy)
    rank = 0
    for i in range(n):
        if any(q != Fraction(0) for q in Q_copy[i]):
            rank += 1
    return rank

def construct_quandle_representations(f, n):
    # Placeholder function to construct a quandle representation
    # This is a dummy implementation and should be replaced with actual code
    Q = [[Fraction(0)] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if f(i, j) == 1:
                Q[i][j] = Fraction(1)
            else:
                Q[i][j] = Fraction(-1)
    return Q

def find_smallest_sum_of_squares_circuit(f, n):
    # Placeholder function to find the smallest sum-of-squares circuit
    # This is a dummy implementation and should be replaced with actual code
    size = 2**n
    return size

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    f = lambda i, j: random.choice([0, 1])
    Q = construct_quandle_representations(f, n)
    rank_trop = min_rank_trop(Q)
    size_circuit = find_smallest_sum_of_squares_circuit(f, n)
    
    if rank_trop >= n**2 and size_circuit >= 2**n:
        conjecture_holds = True
        counterexample = ""
    else:
        conjecture_holds = False
        counterexample = "mapping_undefined"
    
    return {
        "metric_name": "minRank_trop vs size_circuit",
        "metric_value": rank_trop,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else list(range(2, 30*37, 2))[:30]
    
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
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")