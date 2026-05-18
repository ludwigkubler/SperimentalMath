# auto-injected by SEC sandbox
import json
import os
import time
import re
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import sys
import random
import math
import itertools
from collections import defaultdict

def matrix_mult(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]

def matrix_transpose(m):
    return [list(row) for row in zip(*m)]

def matrix_minor(m, i, j):
    return [row[:j] + row[j+1:] for row in (m[:i] + m[i+1:])]

def matrix_det(m):
    if len(m) == 1:
        return m[0][0]
    det = 0
    for c in range(len(m)):
        det += ((-1)**c) * m[0][c] * matrix_det(matrix_minor(m, 0, c))
    return det

def generate_permutation(n):
    sigma = list(range(n))
    random.shuffle(sigma)
    return sigma

def generate_linear_form(n, seed):
    random.seed(seed)
    coeffs = [random.randint(-2, 2) for _ in range(n)]
    return coeffs

def generate_matrix_of_linear_forms(n, m, seed):
    random.seed(seed)
    matrix = []
    for _ in range(m):
        row = []
        for _ in range(m):
            coeffs = [random.randint(-1, 1) for _ in range(n)]
            row.append(coeffs)
        matrix.append(row)
    return matrix

def evaluate_linear_form(l, x):
    return sum(l[i] * x[i] for i in range(len(l)))

def evaluate_matrix_form(L, x):
    return [[sum(L[i][j][k] * x[k] for k in range(len(x))) for j in range(len(L[0]))] for i in range(len(L))]

def compute_c_perm_n(n):
    return [1] * math.factorial(n)

def compute_c_padded_det(n, m, l, L, seed):
    random.seed(seed)
    c = [0] * math.factorial(n)
    for sigma in itertools.permutations(range(n)):
        sigma_list = list(sigma)
        for T in itertools.combinations(range(n), m):
            for rho in itertools.permutations(range(m)):
                rho_list = list(rho)
                pi = {T[i]: i for i in range(m)}
                term = 1
                for i in range(n):
                    if i not in T:
                        term *= l[i] * x[sigma_list[i]]
                    else:
                        term *= L[pi[i]][rho_list[pi[i]]][sigma_list[i]]
                c[sigma] += term
    return c

def compute_shape(sigma):
    piles = []
    for card in sigma:
        placed = False
        for pile in piles:
            if card < pile[-1]:
                pile.append(card)
                placed = True
                break
        if not placed:
            piles.append([card])
    return tuple(len(pile) for pile in piles)

def compute_k(c, n):
    shapes = defaultdict(float)
    total = sum(x**2 for x in c)
    if total == 0:
        return 0
    for sigma in itertools.permutations(range(n)):
        shape = compute_shape(sigma)
        shapes[shape] += c[sigma]**2 / total
    return max(shapes.values()) if shapes else 0

def run_trial(seed):
    n = random.choice([5, 6, 7, 8])
    m = random.randint(1, 3)
    random.seed(seed)
    l = generate_linear_form(n, seed)
    L = generate_matrix_of_linear_forms(n, m, seed)
    c_perm_n = compute_c_perm_n(n)
    c_padded_det = compute_c_padded_det(n, m, l, L, seed)
    k_perm_n = compute_k(c_perm_n, n)
    k_padded_det = compute_k(c_padded_det, n)
    ratio = k_padded_det / k_perm_n if k_perm_n != 0 else 0
    conjecture_holds = ratio >= 2
    counterexample = f"n={n}, m={m}, ratio={ratio}" if not conjecture_holds else ""
    return {
        "metric_name": "K(g)/K(perm_n)",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else [random.randint(1, 1000000) for _ in range(30)]
    trials = []
    for seed in seeds:
        trial = run_trial(seed)
        trials.append(trial)
        print(f"TRIAL: {trial}")

    metric_values = [trial["metric_value"] for trial in trials]
    mean = sum(metric_values) / len(metric_values)
    std = math.sqrt(sum((x - mean) ** 2 for x in metric_values) / len(metric_values))
    support_fraction = sum(trial["conjecture_holds"] for trial in trials) / len(trials)

    if all(trial["conjecture_holds"] for trial in trials):
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    elif any(not trial["conjecture_holds"] for trial in trials):
        first_failing_seed = next(trial["seed"] for trial in trials if not trial["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample={trials[first_failing_seed]['counterexample']} first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")