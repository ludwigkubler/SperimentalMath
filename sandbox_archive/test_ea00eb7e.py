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

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    return abs(a*b) // gcd(a, b)

def gaussian_elimination(matrix, n):
    for i in range(n):
        max_row = i
        for j in range(i+1, n):
            if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                max_row = j
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        factor = 1 / matrix[i][i]
        for j in range(n):
            matrix[i][j] *= factor
        for j in range(n):
            if i != j:
                factor = matrix[j][i]
                for k in range(n):
                    matrix[j][k] -= factor * matrix[i][k]
    return [sum(row) % 2 for row in matrix]

def rank(matrix, n):
    return sum(1 for row in gaussian_elimination(matrix[:], n) if any(row))

def ind_lifted_matrix(f, k):
    n = 2**k
    M = [[0] * (4*n) for _ in range(n)]
    for i in range(n):
        alpha = bin(i)[2:].zfill(k)
        beta = bin(j)[2:].zfill(k)
        M[i][j*4:(j+1)*4] = [int(f(beta[b]*alpha[a]) for b in range(k) for a in range(k))]
    return M

def hochster_betti_sum(Δ_f, k):
    β = 0
    for σ in range(1 << k):
        Δ_fσ = [S for S in Δ_f if all(x in S for x in range(k) if (σ >> x) & 1)]
        n = len(Δ_fσ)
        C = [[0] * n for _ in range(n+1)]
        for i, S in enumerate(Δ_fσ):
            for j in range(len(S)):
                C[j][i] = int(all(x not in S for x in range(k) if (σ >> x) & 1))
        rank_C = rank(C, n)
        nullity_C = n - rank_C
        β += sum(nullity_C - rank(C[i+1:]) for i in range(n))
    return β

def run_trial(seed: int) -> dict:
    random.seed(seed)
    k_values = [3, 4, 5, 6]
    instances_tested = 0
    total_metric_value = 0
    conjecture_holds = True
    counterexample = ""

    for k in k_values:
        for _ in range(30):
            n = 2**k
            f = lambda x: any(x[i] > x[j] for i, j in itertools.combinations(range(k), 2))
            Δ_f = [S for S in range(1 << k) if all(f(bin(S)[2:].zfill(k)[:i+1]) == 0 for i in range(len(bin(S)[2:])-1))]
            β = hochster_betti_sum(Δ_f, k)
            M = ind_lifted_matrix(f, k)
            rank_M = rank(M, n)
            metric_value = math.log2(1 + β) + 1
            if rank_M < math.ceil(metric_value):
                conjecture_holds = False
                counterexample = f"Monotone function for k={k} does not satisfy the inequality."
            total_metric_value += metric_value
            instances_tested += 1

    return {
        "metric_name": "log2_rank_F2",
        "metric_value": total_metric_value / instances_tested,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 8)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")