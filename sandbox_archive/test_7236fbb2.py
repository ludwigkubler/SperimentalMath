# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction
from itertools import combinations

def generate_xor_tautology(n):
    variables = [random.choice([0, 1]) for _ in range(n)]
    clauses = []
    for i in range(2**n):
        clause = []
        for j in range(n):
            if (i >> j) & 1:
                clause.append(variables[j])
            else:
                clause.append(1 - variables[j])
        clauses.append(clause)
    return clauses

def tropical_derivative(tau):
    n = len(tau)
    D = [0] * n
    for i in range(n):
        for j in range(i+1, n):
            if tau[i] == tau[j]:
                continue
            diff = abs(tau[i] - tau[j])
            if diff > 1:
                return float('inf')
            D[i] += 1 / (diff + 1)
    return sum(D)

def resolution_length(phi):
    clauses = phi[:]
    length = 0
    while True:
        new_clauses = []
        for i in range(len(clauses)):
            for j in range(i+1, len(clauses)):
                if set(clauses[i]) & set(clauses[j]):
                    new_clause = list(set(clauses[i]) ^ set(clauses[j]))
                    if not any(new_clause == c for c in clauses):
                        new_clauses.append(new_clause)
        if not new_clauses:
            break
        clauses.extend(new_clauses)
        length += 1
    return length

def spearman_rank_correlation(x, y):
    n = len(x)
    x_sorted = sorted(zip(x, range(n)))
    y_sorted = sorted(zip(y, range(n)))
    rank_x = [y[1] for y in x_sorted]
    rank_y = [x[1] for x in y_sorted]
    return 1 - (6 * sum((rank_x[i] - rank_y[i]) ** 2 for i in range(n)) / (n * (n**2 - 1)))

def polynomial_regression(x, y):
    n = len(x)
    X = [[x[i], x[i]**2] for i in range(n)]
    Y = y
    A = [sum(X[i][j] * Y[i] for i in range(n)) for j in range(2)]
    B = [sum(X[i][j] ** 2 for i in range(n)) for j in range(2)]
    det = B[0] * B[1] - B[0]**2
    if det == 0:
        return None
    a = (A[1] * B[0] - A[0] * B[1]) / det
    b = (A[0] * B[1] - A[1] * B[0]) / det
    return lambda n, eps: abs(a * n + b) <= eps

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    for _ in range(30):
        n = random.randint(4, 40)
        tau = generate_xor_tautology(n)
        D = tropical_derivative(tau)
        r = resolution_length(tau)
        if D == float('inf'):
            continue
        results.append((D, r))
    if not results:
        return {
            "metric_name": "Spearman rank correlation",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    x, y = zip(*results)
    rho = spearman_rank_correlation(x, y)
    g = polynomial_regression(x, y)
    if rho is None or g is None:
        return {
            "metric_name": "Spearman rank correlation",
            "metric_value": rho,
            "instances_tested": len(results),
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    return {
        "metric_name": "Spearman rank correlation",
        "metric_value": rho,
        "instances_tested": len(results),
        "conjecture_holds": rho > 0.7 and g(n, eps=1e-2) <= math.log(n),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)

    if all(r["conjecture_holds"] for r in results):
        mean = sum(r["metric_value"] for r in results) / len(results)
        std_dev = math.sqrt(sum((r["metric_value"] - mean) ** 2 for r in results) / len(results))
        support_fraction = 1.0
    else:
        mean = None
        std_dev = None
        support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        counterexample = f"seed={seeds[first_failing_seed]}"
    
    print(f"RESULT: {'SUPPORTED' if support_fraction >= 0.8 else 'FALSIFIED'} mean={mean} std={std_dev} support_fraction={support_fraction}")