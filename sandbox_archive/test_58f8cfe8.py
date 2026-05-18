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

def matrix_transpose(A):
    return [list(row) for row in zip(*A)]

def matrix_minor(A, i, j):
    return [row[:j] + row[j+1:] for row in (A[:i] + A[i+1:])]

def matrix_determinant(A):
    n = len(A)
    if n == 1:
        return A[0][0]
    det = 0
    for j in range(n):
        det += ((-1) ** j) * A[0][j] * matrix_determinant(matrix_minor(A, 0, j))
    return det

def generate_permutation(n):
    perm = list(range(n))
    random.shuffle(perm)
    return perm

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

def evaluate_linear_form(form, values):
    return sum(c * v for c, v in zip(form, values))

def evaluate_matrix_form(matrix, values):
    return [[evaluate_linear_form(row, values) for row in matrix_row] for matrix_row in matrix]

def compute_c_perm_n(n):
    return [1] * math.factorial(n)

def compute_c_padded_det(g, n, m, l, L):
    c = [0] * math.factorial(n)
    for sigma in itertools.permutations(range(n)):
        for rho in itertools.permutations(range(m)):
            for T in itertools.combinations(range(n), m):
                for pi in itertools.permutations(T):
                    if len(set(pi)) != m:
                        continue
                    term = 1
                    for i in range(n):
                        if i in T:
                            term *= L[pi.index(i)][rho[pi.index(i)]][sigma[i]]
                        else:
                            term *= l[sigma[i]]
                    term *= (-1) ** sum(rho[i] > rho[j] for i in range(m) for j in range(i))
                    c[sigma] += term
    return c

def compute_rs_shape(perm):
    shape = []
    for num in perm:
        inserted = False
        for i, row in enumerate(shape):
            if num < row[-1]:
                row.append(num)
                inserted = True
                break
        if not inserted:
            shape.append([num])
    return tuple(len(row) for row in shape)

def compute_k(f, n):
    c = f(n)
    shapes = defaultdict(int)
    total = sum(c_sigma ** 2 for c_sigma in c)
    if total == 0:
        return 0
    for sigma in itertools.permutations(range(n)):
        shape = compute_rs_shape(sigma)
        shapes[shape] += c[sigma] ** 2
    max_prob = max(shapes.values()) / total
    return max_prob

def run_trial(seed):
    random.seed(seed)
    n = random.choice([5, 6, 7, 8])
    m = random.choice([1, 2, 3])
    l = generate_linear_form(n, seed)
    L = generate_matrix_of_linear_forms(n, m, seed)

    def f_perm_n(n):
        return compute_c_perm_n(n)

    def f_padded_det(n):
        return compute_c_padded_det(g, n, m, l, L)

    k_perm_n = compute_k(f_perm_n, n)
    k_padded_det = compute_k(f_padded_det, n)

    if k_perm_n == 0:
        return {
            "metric_name": "K(g)/K(perm_n)",
            "metric_value": 0,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "K(perm_n) is zero"
        }

    ratio = k_padded_det / k_perm_n
    conjecture_holds = ratio >= 2
    counterexample = "" if conjecture_holds else f"K(g)/K(perm_n) = {ratio} < 2"

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
        print(f"TRIAL: {trial}")
        trials.append(trial)

    metric_values = [trial["metric_value"] for trial in trials]
    mean = sum(metric_values) / len(metric_values)
    std = math.sqrt(sum((x - mean) ** 2 for x in metric_values) / len(metric_values))
    support_fraction = sum(trial["conjecture_holds"] for trial in trials) / len(trials)

    if all(trial["conjecture_holds"] for trial in trials):
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    else:
        for trial in trials:
            if not trial["conjecture_holds"]:
                print(f"RESULT: FALSIFIED counterexample=\"{trial['counterexample']}\" first_failing_seed={seeds[trials.index(trial)]}")
                break