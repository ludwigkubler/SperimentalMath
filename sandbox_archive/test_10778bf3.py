# auto-injected by SEC sandbox
import math
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
from itertools import product

def gaussian_elimination(A):
    m, n = len(A), len(A[0])
    rank = 0
    for j in range(n):
        i_max = rank
        for i in range(rank, m):
            if abs(A[i][j]) > abs(A[i_max][j]):
                i_max = i
        A[rank], A[i_max] = A[i_max], A[rank]
        if A[rank][j] != 0:
            factor = 1 / A[rank][j]
            for j2 in range(n):
                A[rank][j2] *= factor
            for i in range(m):
                if i != rank:
                    factor = A[i][j]
                    for j2 in range(n):
                        A[i][j2] -= factor * A[rank][j2]
            rank += 1
    return rank

def matrix_multiplication(A, B):
    m, n, p = len(A), len(B), len(B[0])
    C = [[0 for _ in range(p)] for _ in range(m)]
    for i in range(m):
        for j in range(n):
            for k in range(p):
                C[i][k] += A[i][j] * B[j][k]
    return C

def compute_disc(D, M):
    ℓ = len(M)
    disc = float('inf')
    for coloring in product([-1, 1], repeat=ℓ):
        y = [sum(M[i][j] * coloring[j] for j in range(ℓ)) for i in range(len(D))]
        disc = min(disc, max(abs(y)))
    return disc

def compute_as(f):
    a = len(f)
    count = 0
    for x in product([0, 1], repeat=a):
        for y in product([0, 1], repeat=a):
            if x != y and f(x) == f(y):
                count += 1
    return count / (2 ** a)

def compute_beta(NW_D_f, m):
    n = len(NW_D_f)
    width = (n.bit_length() - 1)
    beta = float('-inf')
    for T in product([0, 1], repeat=n * width):
        T = [T[i:i+width] for i in range(0, n * width, width)]
        pr_s = sum(NW_D_f(s) == 1 for s in product([0, 1], repeat=len(NW_D_f))) / (2 ** len(NW_D_f))
        pr_y = sum(T[y].count(1) / (2 ** y.count(1)) for y in product([0, 1], repeat=n)) / (2 ** n)
        beta = max(beta, abs(pr_s - pr_y))
    return beta

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [6, 8, 11, 14]
    a_values = [2, 3, 4]
    results = []
    
    for n in n_values:
        for a in a_values:
            m = min(2 * n, 16)
            ℓ = random.randint(5, 16)
            
            # Generate an (ℓ, a)-NW design
            D = [set() for _ in range(m)]
            while len(D[0]) < a:
                S = set(random.sample(range(ℓ), a))
                if all(len(S.intersection(T)) <= a for T in D):
                    D[random.randint(0, m-1)].update(S)
            
            # Build the incidence matrix M
            M = [[int(i in S) for i in range(ℓ)] for S in D]
            
            # Compute disc(D)
            disc = compute_disc(D, M)
            
            # Define a random Boolean function f
            f = lambda x: random.choice([0, 1])
            
            # Compute AS(f)
            as_f = compute_as(f)
            
            # Generate NW_{D,f}
            NW_D_f = [f(tuple(random.choices([0, 1], k=ℓ))) for _ in range(2 ** ℓ)]
            
            # Compute β(NW_{D,f})
            beta = compute_beta(NW_D_f, m)
            
            results.append({
                "metric_name": "beta",
                "metric_value": beta,
                "instances_tested": 1,
                "conjecture_holds": beta <= 4 * (disc / m) * 2 ** as_f + 2 ** (-a / 2),
                "counterexample": ""
            })
    
    mean_beta = sum(result["metric_value"] for result in results) / len(results)
    std_beta = (sum((result["metric_value"] - mean_beta) ** 2 for result in results) / len(results)) ** 0.5
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    return {
        "seed": seed,
        "mean_beta": mean_beta,
        "std_beta": std_beta,
        "support_fraction": support_fraction,
        "results": results
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [11, 23, 37, 53, 71]
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        
    mean_beta = sum(result["mean_beta"] for result in result["results"]) / len(result["results"])
    std_beta = (sum((result["mean_beta"] - mean_beta) ** 2 for result in result["results"]) / len(result["results"])) ** 0.5
    support_fraction = sum(1 for result in result["results"] if result["support_fraction"] >= 0.8) / len(result["results"])
    
    if support_fraction == 1:
        print(f"RESULT: SUPPORTED mean={mean_beta} std={std_beta} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print("RESULT: INCONCLUSIVE less than 80% seeds support")
    else:
        first_failing_seed = next(seed for seed, result in enumerate(result["results"], start=1) if result["support_fraction"] < 0.8)
        print(f"RESULT: FALSIFIED counterexample=\"first failing seed\" first_failing_seed={first_failing_seed}")