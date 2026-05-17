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

def cycle_type(perm):
    cycles = []
    visited = [False] * len(perm)
    for i in range(len(perm)):
        if not visited[i]:
            cycle = []
            j = i
            while not visited[j]:
                visited[j] = True
                cycle.append(j)
                j = perm[j]
            cycles.append(tuple(sorted(cycle)))
    return tuple(sorted(cycles))

def murnaghan_nakayama(n):
    if n == 0:
        return {(): 1}
    chi = murnaghan_nakayama(n - 1)
    new_chi = defaultdict(int)
    for part, val in chi.items():
        for i in range(len(part)):
            new_part = list(part)
            new_part[i] -= 1
            new_part = tuple(sorted([x for x in new_part if x > 0], reverse=True))
            sign = (-1) ** (i + 1)
            new_chi[new_part] += sign * val
    return dict(new_chi)

def immanant(M, chi_lambda):
    n = len(M)
    total = 0
    for perm in itertools.permutations(range(n)):
        ct = cycle_type(perm)
        if ct in chi_lambda:
            product = 1
            for i in range(n):
                product *= M[i][perm[i]]
            total += chi_lambda[ct] * product
    return total

def compute_variance(M, chi_tables):
    n = len(M)
    I_lambdas = []
    for chi_lambda in chi_tables.values():
        I_lambda = immanant(M, chi_lambda)
        I_lambdas.append(math.log2(1 + abs(I_lambda)))
    mean = sum(I_lambdas) / len(I_lambdas)
    variance = sum((x - mean) ** 2 for x in I_lambdas) / len(I_lambdas)
    return variance

def run_trial(seed):
    random.seed(seed)
    n_values = [5, 6, 7]
    chi_tables = {n: murnaghan_nakayama(n) for n in n_values}

    results = []
    for n in n_values:
        # Uniform matrix
        M = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
        V_uniform = compute_variance(M, chi_tables[n])

        # Padded matrix
        m = n // 2
        M_prime = [[random.randint(0, 1) for _ in range(m)] for _ in range(m)]
        J = [[1 for _ in range(n - m)] for _ in range(n - m)]
        M_pad = [[0 for _ in range(n)] for _ in range(n)]
        for i in range(m):
            for j in range(m):
                M_pad[i][j] = M_prime[i][j]
        for i in range(m, n):
            for j in range(m, n):
                M_pad[i][j] = J[i - m][j - m]

        V_pad = compute_variance(M_pad, chi_tables[n])

        conjecture_holds = V_uniform >= 4 * V_pad
        counterexample = "" if conjecture_holds else f"V_uniform={V_uniform} < 4*V_pad={4*V_pad}"

        results.append({
            "n": n,
            "metric_name": "log_variance_ratio",
            "metric_value": V_uniform / V_pad,
            "instances_tested": 2,
            "conjecture_holds": conjecture_holds,
            "counterexample": counterexample
        })

    overall_holds = all(r["conjecture_holds"] for r in results)
    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    counterexample = next((r["counterexample"] for r in results if not r["conjecture_holds"]), "")

    return {
        "seed": seed,
        "metric_name": "log_variance_ratio",
        "metric_value": mean_ratio,
        "instances_tested": len(results) * 2,
        "conjecture_holds": overall_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]

    trials = []
    for seed in seeds:
        trial = run_trial(seed)
        print(f"TRIAL: {trial}")
        trials.append(trial)

    metric_values = [t["metric_value"] for t in trials]
    mean_metric = sum(metric_values) / len(metric_values)
    std_metric = math.sqrt(sum((x - mean_metric) ** 2 for x in metric_values) / len(metric_values))
    support_fraction = sum(t["conjecture_holds"] for t in trials) / len(trials)

    if all(t["conjecture_holds"] for t in trials) and mean_metric >= 4:
        print(f"RESULT: SUPPORTED mean={mean_metric:.2f} std={std_metric:.2f} support_fraction={support_fraction:.2f}")
    elif any(not t["conjecture_holds"] for t in trials):
        first_failing_seed = next(t["seed"] for t in trials if not t["conjecture_holds"])
        counterexample = next(t["counterexample"] for t in trials if not t["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_support")