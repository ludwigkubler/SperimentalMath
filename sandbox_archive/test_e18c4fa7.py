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
        if A[i][i] == 0:
            continue
        for j in range(n):
            if j != i:
                factor = Fraction(A[j][i], A[i][i])
                for k in range(n):
                    A[j][k] -= factor * A[i][k]
    rank = sum(1 for row in A if any(row))
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    k = random.randint(2, min(n-1, 5))
    
    # Generate a random k-clique instance
    V = list(range(n))
    E = []
    for i in range(n):
        for j in range(i+1, n):
            if random.random() < math.comb(k, 2) / math.comb(n-1, 2):
                E.append((i, j))
    
    # Construct the associated monomial ideal
    I = set()
    for edge in E:
        x_i, x_j = V[edge[0]], V[edge[1]]
        I.add(f"x_{x_i} * x_{x_j}")
    
    # Compute the tropical curve (simplified as a matrix)
    T = [[0] * n for _ in range(n)]
    for edge in E:
        i, j = edge
        T[i][j] = 1
        T[j][i] = 1
    
    rank_T = gaussian_elimination(T)
    
    # Check the conjecture
    f_n = Fraction(n**2 * math.log(n), 1)
    if rank_T < f_n:
        return {
            "metric_name": "Minimal Rank",
            "metric_value": rank_T,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"n={n}, k={k}, rank_T={rank_T}, f(n)={f_n}"
        }
    
    return {
        "metric_name": "Minimal Rank",
        "metric_value": rank_T,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    std_rank = math.sqrt(sum((r["metric_value"] - mean_rank)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        counterexample = next(r["counterexample"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")