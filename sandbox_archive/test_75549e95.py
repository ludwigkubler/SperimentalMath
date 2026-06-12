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

def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        if A[i][i] == 0:
            # Swap with a row below
            for j in range(i + 1, n):
                if A[j][i] != 0:
                    A[i], A[j] = A[j], A[i]
                    break
            else:
                raise ValueError("Matrix is singular")
        # Eliminate above and below
        pivot = A[i][i]
        for j in range(n):
            A[i][j] /= pivot
        for k in range(n):
            if k != i:
                factor = A[k][i]
                for j in range(n):
                    A[k][j] -= factor * A[i][j]
    rank = sum(1 for row in A if any(row))
    return rank

def quadratic_form_rank(cnf):
    n = len(cnf)
    M = [[0] * n for _ in range(n)]
    for clause in cnf:
        for lit in clause:
            var = abs(lit) - 1
            M[var][var] += 1
    return gaussian_elimination(M)

def generate_cnf(n, m):
    cnf = []
    literals = list(range(1, n + 1)) + [-i for i in range(1, n + 1)]
    for _ in range(m):
        clause = random.sample(literals, random.randint(2, n))
        cnf.append(clause)
    return cnf

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_max = 0
    instances_tested = 0
    r_q_values = []
    w_c_values = []

    for n in [5, 10, 15, 20, 30, 40]:
        if n > n_max:
            n_max = n
        for _ in range(5):
            cnf = generate_cnf(n, random.randint(n, 2 * n))
            instances_tested += 1
            try:
                r_q = quadratic_form_rank(cnf)
                w_c = max(len(clause) for clause in cnf)
                r_q_values.append(r_q)
                w_c_values.append(w_c)
            except Exception as e:
                return {
                    "metric_name": "r_q vs w_c",
                    "metric_value": None,
                    "instances_tested": instances_tested,
                    "n_max": n_max,
                    "conjecture_holds": False,
                    "counterexample": str(e),
                }

    if len(r_q_values) < 10:
        return {
            "metric_name": "r_q vs w_c",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "Insufficient data points",
        }

    r_q_mean = sum(r_q_values) / len(r_q_values)
    w_c_mean = sum(w_c_values) / len(w_c_values)

    # Calculate Pearson correlation coefficient
    covariance = sum((r_q - r_q_mean) * (w_c - w_c_mean) for r_q, w_c in zip(r_q_values, w_c_values))
    r_q_var = sum((r_q - r_q_mean) ** 2 for r_q in r_q_values)
    w_c_var = sum((w_c - w_c_mean) ** 2 for w_c in w_c_values)
    correlation_coefficient = covariance / math.sqrt(r_q_var * w_c_var)

    return {
        "metric_name": "r_q vs w_c",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": abs(correlation_coefficient) > 0.9,
        "counterexample": "",
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)

    if all("conjecture_holds" in r and r["conjecture_holds"] for r in results):
        mean = sum(r["metric_value"] for r in results) / len(results)
        std_dev = math.sqrt(sum((r["metric_value"] - mean) ** 2 for r in results) / len(results))
        support_fraction = sum(1 for r in results if "conjecture_holds" in r and r["conjecture_holds"]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
    elif any("counterexample" in r and r["counterexample"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if "counterexample" in result and result["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[seeds.index(first_failing_seed)]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")