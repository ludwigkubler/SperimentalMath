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

def compute_chi_tables(max_n):
    chi_tables = {}
    for n in range(1, max_n + 1):
        chi_tables[n] = {}
        for partition in itertools.product(range(n, 0, -1), repeat=n):
            if sum(partition) == n:
                chi_tables[n][partition] = {}
                for sigma in itertools.permutations(range(n)):
                    cycle_type = tuple(sorted(len(list(g)) for k, g in itertools.groupby(sigma)))
                    if cycle_type not in chi_tables[n][partition]:
                        chi_tables[n][partition][cycle_type] = 0
                    chi_tables[n][partition][cycle_type] += 1
    return chi_tables

def compute_immanants(M, chi_tables):
    n = len(M)
    I_lambdas = defaultdict(int)
    for sigma in itertools.permutations(range(n)):
        cycle_type = tuple(sorted(len(list(g)) for k, g in itertools.groupby(sigma)))
        for partition in chi_tables[n]:
            if cycle_type in chi_tables[n][partition]:
                product = 1
                for i in range(n):
                    product *= M[i][sigma[i]]
                I_lambdas[partition] += chi_tables[n][partition][cycle_type] * product
    return I_lambdas

def compute_variance(M, chi_tables):
    I_lambdas = compute_immanants(M, chi_tables)
    if not I_lambdas:
        return 0.0
    log_values = [math.log2(1 + abs(I)) for I in I_lambdas.values()]
    mean = sum(log_values) / len(log_values)
    variance = sum((x - mean) ** 2 for x in log_values) / len(log_values)
    return variance

def generate_random_matrix(n, seed):
    random.seed(seed)
    return [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]

def generate_padded_matrix(n, seed):
    random.seed(seed)
    m = (n + 1) // 2
    M_prime = [[random.randint(0, 1) for _ in range(m)] for _ in range(m)]
    J = [[1 for _ in range(n - m)] for _ in range(n - m)]
    M_pad = [[0 for _ in range(n)] for _ in range(n)]
    for i in range(m):
        for j in range(m):
            M_pad[i][j] = M_prime[i][j]
    for i in range(m, n):
        for j in range(m, n):
            M_pad[i][j] = J[i - m][j - m]
    return M_pad

def run_trial(seed):
    chi_tables = compute_chi_tables(7)
    results = []
    for n in [5, 6, 7]:
        M_uniform = generate_random_matrix(n, seed)
        M_pad = generate_padded_matrix(n, seed)
        V_uniform = compute_variance(M_uniform, chi_tables)
        V_pad = compute_variance(M_pad, chi_tables)
        results.append({
            "n": n,
            "V_uniform": V_uniform,
            "V_pad": V_pad,
            "conjecture_holds": V_uniform >= 4 * V_pad
        })
    overall_holds = all(r["conjecture_holds"] for r in results)
    counterexample = ""
    if not overall_holds:
        for r in results:
            if not r["conjecture_holds"]:
                counterexample = f"n={r['n']} V_uniform={r['V_uniform']} V_pad={r['V_pad']}"
                break
    return {
        "metric_name": "V_ratio",
        "metric_value": sum(r["V_uniform"] / (r["V_pad"] + 1e-10) for r in results) / len(results),
        "instances_tested": len(results),
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
    support_fraction = sum(1 for t in trials if t["conjecture_holds"]) / len(trials)

    if all(t["conjecture_holds"] for t in trials):
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    else:
        for t in trials:
            if not t["conjecture_holds"]:
                print(f"RESULT: FALSIFIED counterexample={t['counterexample']} first_failing_seed={seeds[trials.index(t)]}")
                break