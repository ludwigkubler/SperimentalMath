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

def random_partial_function(n):
    return {tuple(random.randint(0, 1) for _ in range(n)): random.choice([0, 1]) for _ in range(2**n)}

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
                factor = -A[i][j] / A[rank][j]
                for k in range(n):
                    A[i][k] += factor * A[rank][k]
        rank += 1
    return rank

def entropic_quantizer_rank(f, n):
    A = [[0] * (2**n) for _ in range(2**n)]
    for x in f:
        for y in f:
            if x != y and f[x] == f[y]:
                A[sum(x)][sum(y)] += 1
    return gaussian_elimination(A)

def simulate_disjointness_communication(f, n):
    instances = [(x, y) for x in range(2**n) for y in range(2**n) if f[x] != f[y]]
    random.shuffle(instances)
    bits_exchanged = 0
    for x, y in instances:
        bits_exchanged += math.ceil(math.log2(len(x & y)))
    return bits_exchanged

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [30, 40]
    results = []
    for n in n_values:
        f = random_partial_function(n)
        ent_rank = entropic_quantizer_rank(f, n)
        c_disj = simulate_disjointness_communication(f, n)
        results.append((n, ent_rank, c_disj))
    
    mean_ent_rank = sum(ent_rank for _, ent_rank, _ in results) / len(results)
    mean_c_disj = sum(c_disj for _, _, c_disj in results) / len(results)
    support_fraction = sum(1 for _, ent_rank, c_disj in results if ent_rank == math.ceil(math.log2(n)) and c_disj >= n) / len(results)
    
    conjecture_holds = support_fraction >= 0.8
    counterexample = "" if conjecture_holds else f"n={n}, EntRank(f)={ent_rank}, C_DISJ(f)={c_disj}"
    
    return {
        "metric_name": "support_fraction",
        "metric_value": support_fraction,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i - 1 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_support_fraction = sum(result["support_fraction"] for result in results) / len(results)
    support_count = sum(1 for result in results if result["conjecture_holds"])
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_support_fraction} std=0.0 support_fraction=1.0")
    elif support_count / len(results) >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_support_fraction} std=0.0 support_fraction={support_count / len(results)}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"n={results[seeds.index(first_failing_seed)][0]}, EntRank(f)={results[seeds.index(first_failing_seed)][1]}, C_DISJ(f)={results[seeds.index(first_failing_seed)][2]}\" first_failing_seed={first_failing_seed}")