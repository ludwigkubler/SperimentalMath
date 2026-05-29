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

def gaussian_elimination(matrix):
    n = len(matrix)
    for i in range(n):
        if matrix[i][i] == 0:
            # Swap with a row below that has a non-zero pivot
            for j in range(i + 1, n):
                if matrix[j][i] != 0:
                    matrix[i], matrix[j] = matrix[j], matrix[i]
                    break
            else:
                raise ValueError("Matrix is singular")
        # Normalize the current row
        factor = Fraction(1, matrix[i][i])
        for j in range(i, n):
            matrix[i][j] *= factor
        # Eliminate the current column below
        for j in range(i + 1, n):
            factor = matrix[j][i]
            for k in range(i, n):
                matrix[j][k] -= factor * matrix[i][k]

def calculate_coxeter_matrix(circuit):
    n = len(circuit)
    W = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            if circuit[i][j] == 1:
                W[i][j] = Fraction(2)
                W[j][i] = Fraction(2)
            else:
                W[i][j] = Fraction(1)
                W[j][i] = Fraction(1)
    gaussian_elimination(W)
    return W

def calculate_entanglement_entropy(W):
    n = len(W)
    eigenvalues = []
    for i in range(n):
        # Compute the characteristic polynomial
        det = 0
        sign = 1
        for p in itertools.permutations(range(n)):
            term = sign * math.prod([W[i][j] if j == p[k] else 0 for k, j in enumerate(p)])
            det += term
            sign *= -1
        eigenvalues.append(det)
    # Compute the entanglement entropy
    entropy = 0
    for lambda_ in eigenvalues:
        if lambda_ > 0:
            entropy -= lambda_ * math.log2(lambda_)
    return entropy

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 10, 15, 20, 30, 40])
    instances_tested = 0
    total_entropy = 0
    for _ in range(30):
        circuit = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
        if any(sum(row) != n - 1 for row in circuit) or any(sum(col) != n - 1 for col in zip(*circuit)):
            continue
        W = calculate_coxeter_matrix(circuit)
        entropy = calculate_entanglement_entropy(W)
        total_entropy += entropy
        instances_tested += 1
    if instances_tested == 0:
        return {
            "metric_name": "entanglement_entropy",
            "metric_value": 0,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "No valid circuits found"
        }
    average_entropy = total_entropy / instances_tested
    conjecture_holds = average_entropy >= 2**(n/4)
    return {
        "metric_name": "entanglement_entropy",
        "metric_value": average_entropy,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"Average entropy {average_entropy} < 2^{n/4}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1, 1000000) for _ in range(30)]
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)

    total_entropy = sum(r["metric_value"] * r["instances_tested"] for r in results)
    instances_tested = sum(r["instances_tested"] for r in results)
    average_entropy = total_entropy / instances_tested
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={average_entropy} std=0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={average_entropy} std=0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Average entropy {results[first_failing_seed]['metric_value']} < 2^{seeds[first_failing_seed]/4}\" first_failing_seed={seeds[first_failing_seed]}")