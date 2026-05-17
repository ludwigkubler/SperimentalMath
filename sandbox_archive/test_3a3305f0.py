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

def gaussian_elimination(matrix):
    rows = len(matrix)
    if rows == 0:
        return 0
    cols = len(matrix[0])
    rank = 0
    for col in range(cols):
        pivot = -1
        for row in range(rank, rows):
            if matrix[row][col] == 1:
                pivot = row
                break
        if pivot == -1:
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        for row in range(rows):
            if row != rank and matrix[row][col] == 1:
                for c in range(col, cols):
                    matrix[row][c] ^= matrix[rank][c]
        rank += 1
    return rank

def compute_mu_2(minterms):
    if not minterms:
        return 0
    n = len(minterms[0])
    matrix = [list(minterm) for minterm in minterms]
    rank = gaussian_elimination(matrix)
    return len(minterms) - rank

def generate_clique_minterms(v):
    minterms = []
    for i in range(v):
        for j in range(i + 1, v):
            for k in range(j + 1, v):
                minterm = [0] * v
                minterm[i] = 1
                minterm[j] = 1
                minterm[k] = 1
                minterms.append(minterm)
    return minterms

def generate_random_monotone_function(n, s, w, seed):
    random.seed(seed)
    terms = set()
    while len(terms) < s:
        term = tuple(sorted(random.sample(range(n), w)))
        terms.add(term)
    minterms = set()
    for term in terms:
        minterm = [0] * n
        for i in term:
            minterm[i] = 1
        minterms.add(tuple(minterm))
    return list(minterms)

def generate_threshold_minterms(n, k):
    minterms = []
    for indices in itertools.combinations(range(n), k):
        minterm = [0] * n
        for i in indices:
            minterm[i] = 1
        minterms.append(minterm)
    return minterms

def run_trial(seed):
    random.seed(seed)
    results = []
    # Test CLIQUE instances
    for v in range(4, 9):
        n = v * (v - 1) // 2
        minterms = generate_clique_minterms(v)
        mu_2 = compute_mu_2(minterms)
        expected_mu_2 = (v - 1) * (v - 2) * (v - 3) // 6
        conjecture_holds = (mu_2 == expected_mu_2)
        counterexample = "" if conjecture_holds else f"CLIQUE_({v}, 3) has mu_2={mu_2} != {expected_mu_2}"
        results.append({
            "seed": seed,
            "metric_name": "mu_2",
            "metric_value": mu_2,
            "instances_tested": 1,
            "conjecture_holds": conjecture_holds,
            "counterexample": counterexample
        })
    # Test random monotone functions
    for n in [8, 12, 16, 20]:
        for s in [3, 5, 8]:
            for w in [3]:
                minterms = generate_random_monotone_function(n, s, w, seed)
                mu_2 = compute_mu_2(minterms)
                L_DNF = s * w
                bound = L_DNF * math.log2(L_DNF + 2)
                conjecture_holds = (mu_2 <= bound)
                counterexample = "" if conjecture_holds else f"Random monotone function with n={n}, s={s}, w={w} has mu_2={mu_2} > {bound}"
                results.append({
                    "seed": seed,
                    "metric_name": "mu_2_over_L_DNF_log2_L_DNF_plus_2",
                    "metric_value": mu_2 / bound if bound != 0 else 0.0,
                    "instances_tested": 1,
                    "conjecture_holds": conjecture_holds,
                    "counterexample": counterexample
                })
    # Test threshold instances
    for k in [2, 3]:
        for n in [6, 8, 10, 12, 14, 16]:
            minterms = generate_threshold_minterms(n, k)
            mu_2 = compute_mu_2(minterms)
            L_DNF = k * math.comb(n, k)
            bound = L_DNF * math.log2(L_DNF + 2)
            conjecture_holds = (mu_2 <= bound)
            counterexample = "" if conjecture_holds else f"Threshold function with n={n}, k={k} has mu_2={mu_2} > {bound}"
            results.append({
                "seed": seed,
                "metric_name": "mu_2_over_L_DNF_log2_L_DNF_plus_2",
                "metric_value": mu_2 / bound if bound != 0 else 0.0,
                "instances_tested": 1,
                "conjecture_holds": conjecture_holds,
                "counterexample": counterexample
            })
    # Aggregate results
    metric_values = [r["metric_value"] for r in results]
    mean_metric = sum(metric_values) / len(metric_values) if metric_values else 0.0
    std_metric = math.sqrt(sum((x - mean_metric) ** 2 for x in metric_values) / len(metric_values)) if metric_values else 0.0
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results) if results else 0.0
    first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
    first_counterexample = next((r["counterexample"] for r in results if not r["conjecture_holds"]), "")
    if first_failing_seed is not None:
        print(f"RESULT: FALSIFIED counterexample=\"{first_counterexample}\" first_failing_seed={first_failing_seed}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_support")

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    for seed in seeds:
        run_trial(seed)