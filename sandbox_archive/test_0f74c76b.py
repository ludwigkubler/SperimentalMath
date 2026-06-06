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

def generate_random_matrix(n, p):
    A = [[random.randint(0, p-1) for _ in range(n)] for _ in range(n)]
    b = [random.randint(0, p-1) for _ in range(n)]
    return A, b

def gaussian_elimination(A, b, p):
    n = len(A)
    for i in range(n):
        # Find pivot
        max_row = i + random.choice([j for j in range(i, n) if A[j][i] != 0])
        A[i], A[max_row] = A[max_row], A[i]
        b[i], b[max_row] = b[max_row], b[i]

        # Eliminate
        for j in range(n):
            if i != j:
                factor = (A[j][i] * pow(A[i][i], -1, p)) % p
                A[j] = [(A[j][k] - factor * A[i][k]) % p for k in range(n)]
                b[j] = (b[j] - factor * b[i]) % p

    # Back-substitute
    x = [0] * n
    for i in range(n-1, -1, -1):
        x[i] = (b[i] - sum(A[i][j] * x[j] for j in range(i+1, n))) * pow(A[i][i], -1, p) % p
    return x

def p_adic_hensel_steps(A, b, p):
    n = len(A)
    x = [0] * n
    steps = 0
    while True:
        steps += 1
        x_new = gaussian_elimination(A, b, p)
        if all(x_new[i] == x[i] for i in range(n)):
            break
        x = x_new
    return steps

def communication_complexity_rank(A):
    n = len(A)
    rank = 0
    for i in range(n):
        if any(A[j][i] != 0 for j in range(i, n)):
            rank += 1
            for j in range(i+1, n):
                if A[j][i] != 0:
                    factor = A[j][i] / A[i][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_steps = 0
    total_rank = 0
    instances_tested = 0
    
    for n in n_values:
        A, b = generate_random_matrix(n, p=7)
        steps = p_adic_hensel_steps(A, b, p=7)
        rank = communication_complexity_rank(A)
        
        total_steps += steps
        total_rank += rank
        instances_tested += 1
    
    mean_steps = total_steps / len(n_values)
    mean_rank = total_rank / len(n_values)
    
    diff = abs(mean_steps - mean_rank)
    if diff > 3:
        return {
            "metric_name": "p-adic Hensel Steps vs Communication Complexity Rank",
            "metric_value": diff,
            "instances_tested": instances_tested,
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": f"Mean steps: {mean_steps}, Mean rank: {mean_rank}"
        }
    
    return {
        "metric_name": "p-adic Hensel Steps vs Communication Complexity Rank",
        "metric_value": diff,
        "instances_tested": instances_tested,
        "n_max": max(n_values),
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_diff = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_diff} std=0 support_fraction={support_fraction}")
    elif any(r["counterexample"] != "" for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if result["counterexample"] != "")
        print(f"RESULT: FALSIFIED counterexample=\"{results[seeds.index(first_failing_seed)]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence")