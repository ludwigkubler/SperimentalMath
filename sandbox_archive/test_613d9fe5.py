# auto-injected by SEC sandbox
import collections
import json
import os
import time
import re
from collections import defaultdict, Counter, deque
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import sys
import random
import math
import itertools
from fractions import Fraction

def matrix_mult(A, B):
    n = len(A)
    m = len(B[0])
    p = len(B)
    result = [[0 for _ in range(m)] for _ in range(n)]
    for i in range(n):
        for j in range(m):
            for k in range(p):
                result[i][j] += A[i][k] * B[k][j]
    return result

def matrix_det(M):
    n = len(M)
    if n == 1:
        return M[0][0]
    det = 0
    for col in range(n):
        minor = [row[:col] + row[col+1:] for row in M[1:]]
        det += ((-1) ** col) * M[0][col] * matrix_det(minor)
    return det

def compute_c_perm_n(n):
    return [1] * math.factorial(n)

def compute_rs_shape(sigma):
    piles = []
    for num in sigma:
        placed = False
        for pile in piles:
            if num > pile[-1]:
                pile.append(num)
                placed = True
                break
        if not placed:
            piles.append([num])
    return tuple(len(pile) for pile in piles)

def compute_K_perm_n(n):
    c_perm_n = compute_c_perm_n(n)
    shapes = {}
    for sigma in itertools.permutations(range(1, n+1)):
        shape = compute_rs_shape(sigma)
        shapes[shape] = shapes.get(shape, 0) + 1
    total = sum(c_perm_n)
    if total == 0:
        return 0
    max_prob = max(shapes.values()) / total
    return max_prob

def compute_c_padded_det(n, m, l, L, seed):
    random.seed(seed)
    c = [0] * math.factorial(n)
    x = [[random.randint(-2, 2) for _ in range(n)] for _ in range(n)]
    for sigma in itertools.permutations(range(n)):
        sigma_list = list(sigma)
        term = 1
        for i in range(n):
            term *= l[i] * x[i][sigma_list[i]]
        for rho in itertools.permutations(range(m)):
            for T in itertools.combinations(range(n), m):
                for pi in itertools.permutations(range(m)):
                    if len(set(pi)) != m:
                        continue
                    coef = 1
                    for i in range(m):
                        if i not in T:
                            continue
                        coef *= L[pi[i]][rho[pi[i]]]
                    term *= coef
        c[sigma] = term
    return c

def run_trial(seed):
    random.seed(seed)
    n = random.choice([5, 6, 7, 8])
    m = random.randint(1, 3)
    l = [random.randint(-2, 2) for _ in range(n)]
    L = [[random.randint(-1, 1) for _ in range(m)] for _ in range(m)]
    c_padded_det = compute_c_padded_det(n, m, l, L, seed)
    K_perm_n = compute_K_perm_n(n)
    shapes = {}
    total = sum(c_padded_det)
    if total == 0:
        return {
            "metric_name": "K(g)/K(perm_n)",
            "metric_value": 0,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "denominator_zero"
        }
    for sigma in itertools.permutations(range(n)):
        shape = compute_rs_shape(list(sigma))
        shapes[shape] = shapes.get(shape, 0) + c_padded_det[sigma] ** 2
    max_prob = max(shapes.values()) / total
    ratio = max_prob / K_perm_n
    conjecture_holds = ratio >= 2
    counterexample = "" if conjecture_holds else f"n={n}, m={m}, ratio={ratio}"
    return {
        "metric_name": "K(g)/K(perm_n)",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    trials = []
    for seed in seeds:
        trial = run_trial(seed)
        trials.append(trial)
        print(f"TRIAL: {trial}")
    metric_values = [trial["metric_value"] for trial in trials]
    mean = sum(metric_values) / len(metric_values)
    std = math.sqrt(sum((x - mean) ** 2 for x in metric_values) / len(metric_values))
    support_fraction = sum(1 for trial in trials if trial["conjecture_holds"]) / len(trials)
    if all(trial["conjecture_holds"] for trial in trials):
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    else:
        for trial in trials:
            if not trial["conjecture_holds"]:
                print(f"RESULT: FALSIFIED counterexample={trial['counterexample']} first_failing_seed={seeds[trials.index(trial)]}")
                break