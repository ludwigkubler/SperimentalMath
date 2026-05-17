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

def generate_parity_cnf(n):
    m = 2 ** (n - 1)
    M = [[0] * n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            if (i >> j) & 1:
                M[i][j] = -1 if (i >> (n - 1)) & 1 else 1
    return M

def generate_random_ac0(n, m, w):
    M = [[0] * n for _ in range(m)]
    for i in range(m):
        indices = random.sample(range(n), min(w, n))
        for j in indices:
            M[i][j] = random.choice([-1, 1])
    return M

def compute_psi(M):
    n = len(M[0]) if M else 0
    min_discrepancy = float('inf')
    for chi in itertools.product([-1, 1], repeat=n):
        max_row_sum = 0
        for row in M:
            row_sum = sum(row[j] * chi[j] for j in range(n))
            max_row_sum = max(max_row_sum, abs(row_sum))
        min_discrepancy = min(min_discrepancy, max_row_sum)
    return min_discrepancy

def compute_w(M):
    return max(sum(1 for x in row if x != 0) for row in M)

def is_parity_circuit(M, n):
    m = len(M)
    if m != 2 ** (n - 1):
        return False
    for i in range(m):
        for j in range(n):
            if (i >> j) & 1:
                if M[i][j] == 0:
                    return False
    return True

def run_trial(seed):
    random.seed(seed)
    n_values = [4, 6, 8, 10, 12]
    results = []
    for n in n_values:
        # Generate canonical PARITY CNF
        M_cnf = generate_parity_cnf(n)
        psi_cnf = compute_psi(M_cnf)
        w_cnf = compute_w(M_cnf)
        ratio_cnf = psi_cnf / w_cnf if w_cnf != 0 else 0
        is_parity_cnf = is_parity_circuit(M_cnf, n)

        # Generate depth-3 PARITY circuit
        m_depth3 = 2 ** (n // 2 - 1)
        w_depth3 = n // 2
        M_depth3 = generate_random_ac0(m_depth3, n, w_depth3)
        psi_depth3 = compute_psi(M_depth3)
        w_depth3 = compute_w(M_depth3)
        ratio_depth3 = psi_depth3 / w_depth3 if w_depth3 != 0 else 0
        is_parity_depth3 = is_parity_circuit(M_depth3, n)

        # Generate random non-PARITY AC0 circuits
        m_random = 2 ** (n - 1)
        w_random = n
        M_random = generate_random_ac0(m_random, n, w_random)
        psi_random = compute_psi(M_random)
        w_random = compute_w(M_random)
        ratio_random = psi_random / w_random if w_random != 0 else 0
        is_parity_random = is_parity_circuit(M_random, n)

        results.append({
            "n": n,
            "psi_cnf": psi_cnf,
            "w_cnf": w_cnf,
            "ratio_cnf": ratio_cnf,
            "is_parity_cnf": is_parity_cnf,
            "psi_depth3": psi_depth3,
            "w_depth3": w_depth3,
            "ratio_depth3": ratio_depth3,
            "is_parity_depth3": is_parity_depth3,
            "psi_random": psi_random,
            "w_random": w_random,
            "ratio_random": ratio_random,
            "is_parity_random": is_parity_random
        })

    # Aggregate results
    metric_values = []
    conjecture_holds = True
    counterexample = ""
    for result in results:
        if result["is_parity_cnf"] and result["ratio_cnf"] < 0.25:
            conjecture_holds = False
            counterexample = f"PARITY CNF with n={result['n']} has psi/w={result['ratio_cnf']} < 0.25"
            break
        if result["is_parity_depth3"] and result["ratio_depth3"] < 0.25:
            conjecture_holds = False
            counterexample = f"Depth-3 PARITY circuit with n={result['n']} has psi/w={result['ratio_depth3']} < 0.25"
            break
        metric_values.append(result["ratio_cnf"])

    return {
        "metric_name": "psi/w ratio",
        "metric_value": sum(metric_values) / len(metric_values) if metric_values else 0,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    metric_values = []
    conjecture_holds_counts = 0
    first_failing_seed = None

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        metric_values.append(result["metric_value"])
        if result["conjecture_holds"]:
            conjecture_holds_counts += 1
        else:
            if first_failing_seed is None:
                first_failing_seed = seed

    mean_metric = sum(metric_values) / len(metric_values) if metric_values else 0
    std_metric = math.sqrt(sum((x - mean_metric) ** 2 for x in metric_values) / len(metric_values)) if metric_values else 0
    support_fraction = conjecture_holds_counts / len(seeds)

    if first_failing_seed is not None:
        print(f'RESULT: FALSIFIED counterexample="{result["counterexample"]}" first_failing_seed={first_failing_seed}')
    elif support_fraction >= 0.8:
        print(f'RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}')
    else:
        print('RESULT: INCONCLUSIVE reason=insufficient_support')