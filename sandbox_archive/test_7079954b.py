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

def matrix_multiply(A, B):
    return [[sum(a * b for a, b in zip(row, col)) for col in zip(*B)] for row in A]

def matrix_transpose(A):
    return [list(row) for row in zip(*A)]

def gaussian_elimination(matrix):
    nrows = len(matrix)
    ncols = len(matrix[0]) if nrows > 0 else 0
    rank = 0
    for col in range(ncols):
        pivot = -1
        for row in range(rank, nrows):
            if matrix[row][col] != 0:
                pivot = row
                break
        if pivot == -1:
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        pivot_val = matrix[rank][col]
        for c in range(col, ncols):
            matrix[rank][c] = Fraction(matrix[rank][c], pivot_val)
        for r in range(nrows):
            if r != rank and matrix[r][col] != 0:
                factor = matrix[r][col]
                for c in range(col, ncols):
                    matrix[r][c] -= factor * matrix[rank][c]
        rank += 1
    return rank

def generate_acc0_circuit(n, s, seed):
    random.seed(seed)
    if s < 3:
        return "AND"
    depth = 2
    circuit = []
    for _ in range(s):
        if random.random() < 0.5:
            circuit.append("AND")
        else:
            circuit.append("MOD_6")
    return circuit

def evaluate_circuit(circuit, inputs):
    if circuit == "AND":
        return math.prod(inputs)
    elif circuit == "MOD_6":
        return sum(inputs) % 6
    else:
        return random.choice([-1, 1])

def walsh_hadamard_transform(f, n):
    f_hat = {}
    for S in itertools.product([0, 1], repeat=n):
        f_hat[S] = sum(f[x] * math.prod([(-1)**(S[i] * x[i]) for i in range(n)]) for x in itertools.product([-1, 1], repeat=n))
    return f_hat

def compute_lie_stabilizer(f_hat, n):
    A = []
    for alpha in itertools.product([0, 1, 2], repeat=n):
        row = []
        for i in range(n):
            for j in range(n):
                if i == j:
                    term = sum(f_hat[tuple((alpha[k] + (1 if k == i else 0)) % 3 for k in range(n))] for k in range(n))
                else:
                    term = sum(f_hat[tuple((alpha[k] + (1 if k == i or k == j else 0)) % 3 for k in range(n))] for k in range(n))
                row.append(term)
        A.append(row)
    rank = gaussian_elimination(A)
    return n**2 - rank

def run_trial(seed):
    n_values = [4, 5, 6, 7]
    s_values = [3, 8, 20, 50]
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""
    metric_values = []

    for n in n_values:
        for s in s_values:
            random.seed(seed)
            circuit = generate_acc0_circuit(n, s, seed)
            f = {}
            for x in itertools.product([-1, 1], repeat=n):
                f[x] = evaluate_circuit(circuit, x)
            f_hat = walsh_hadamard_transform(f, n)
            gamma = compute_lie_stabilizer(f_hat, n)
            slack = gamma - (n**2 - 10 * s)
            metric_values.append(slack)
            if slack < 0:
                conjecture_holds = False
                counterexample = f"n={n}, s={s}, circuit={circuit}"
            instances_tested += 1

    metric_value = sum(metric_values) / len(metric_values) if metric_values else 0
    return {
        "metric_name": "slack",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    metric_values = [r["metric_value"] for r in results]
    mean_metric = sum(metric_values) / len(metric_values) if metric_values else 0
    std_metric = math.sqrt(sum((x - mean_metric) ** 2 for x in metric_values) / len(metric_values)) if metric_values else 0
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results) if results else 0

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = next((r["counterexample"] for r in results if not r["conjecture_holds"]), "")
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")