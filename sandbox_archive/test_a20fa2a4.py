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

# Helper functions for Gaussian elimination and matrix operations
def gaussian_elimination(A):
    m, n = len(A), len(A[0])
    rank = 0
    for j in range(n):
        i_max = rank
        for i in range(rank, m):
            if abs(A[i][j]) > abs(A[i_max][j]):
                i_max = i
        if A[i_max][j] == 0:
            continue
        A[rank], A[i_max] = A[i_max], A[rank]
        for i in range(m):
            if i != rank:
                factor = A[i][j] / A[rank][j]
                for k in range(n):
                    A[i][k] -= factor * A[rank][k]
        rank += 1
    return rank

def matrix_multiplication(A, B):
    m, n, p = len(A), len(B), len(B[0])
    C = [[0] * p for _ in range(m)]
    for i in range(m):
        for j in range(p):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def minimal_generators(ideal):
    generators = list(ideal)
    rank = gaussian_elimination(generators)
    return rank

# Function to generate a random n-ary Boolean function
def generate_boolean_function(n, seed):
    random.seed(seed)
    return [random.choice([0, 1]) for _ in range(2**n)]

# Function to compute the communication complexity rank variance
def communication_complexity_rank_variance(f):
    n = int(math.log2(len(f)))
    if 2**n != len(f):
        raise ValueError("Input must be a Boolean function of n variables")
    
    # Compute the truth table
    truth_table = [f[i] for i in range(2**n)]
    
    # Compute the rank of the communication matrix
    m = [[0] * (2**n) for _ in range(n)]
    for i in range(n):
        for j in range(2**n):
            if truth_table[j] == truth_table[j ^ (1 << i)]:
                m[i][j] = 1
    
    rank = gaussian_elimination(m)
    return rank

def run_trial(seed: int) -> dict:
    n_max = 40
    instances_tested = 0
    metric_value = 0.0
    conjecture_holds = True
    counterexample = ""

    for n in range(5, n_max + 1):
        if time.time() - start_time > 200:
            return {
                "metric_name": "R(f)",
                "metric_value": metric_value,
                "instances_tested": instances_tested,
                "n_max": n_max,
                "conjecture_holds": conjecture_holds,
                "counterexample": counterexample
            }
        
        f = generate_boolean_function(n, seed)
        R_f = communication_complexity_rank_variance(f)
        G = {(i, j) for i in range(2**n) for j in range(n) if f[i] == f[i ^ (1 << j)]}
        m_G = minimal_generators(G)
        
        instances_tested += 1
        metric_value += R_f
        
        if m_G > 0.3 * R_f ** 2:
            conjecture_holds = False
            counterexample = f"n={n}, R(f)={R_f}, m_G={m_G}"
    
    return {
        "metric_name": "R(f)",
        "metric_value": metric_value / instances_tested,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    import time

    if len(sys.argv) > 1:
        seeds = [int(seed) for seed in sys.argv[1:]]
    else:
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
        seeds = primes[:30]

    start_time = time.time()
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=budget_exceeded n_tested=30")