# auto-injected by SEC sandbox
import itertools
import os
import time
import re
from itertools import product, combinations, permutations, chain
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import sys
import random
import math
import json
from collections import defaultdict

def generate_monotone_dnf(s, N):
    dnf = []
    for _ in range(s):
        term = []
        for _ in range(random.randint(1, N)):
            var = random.randint(1, N)
            if var not in term:
                term.append(var)
        dnf.append(term)
    return dnf

def get_minterms(dnf, N):
    minterms = []
    for term in dnf:
        minterm = [0] * N
        for var in term:
            minterm[var - 1] = 1
        minterms.append(minterm)
    return minterms

def compute_mean_width(minterms, N, num_samples=2000):
    total = 0.0
    for _ in range(num_samples):
        u = [random.gauss(0, 1) for _ in range(N)]
        norm = math.sqrt(sum(x * x for x in u))
        if norm == 0:
            continue
        u = [x / norm for x in u]
        max_dot = max(sum(u[i] * m[i] for i in range(N)) for m in minterms)
        total += max_dot
    return 2 * total / num_samples

def generate_k_clique_dnf(v, k):
    dnf = []
    edges = v * (v - 1) // 2
    for i in range(v):
        for j in range(i + 1, v):
            term = [0] * edges
            term[i * (v - 1) + j - (i + 1) * i // 2] = 1
            dnf.append(term)
    return dnf

def run_trial(seed):
    random.seed(seed)
    metric_name = "mean_width"
    metric_value = 0.0
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""

    # Test monotone DNFs
    for s in [5, 10, 20, 40]:
        for N in [12, 18, 24, 28]:
            dnf = generate_monotone_dnf(s, N)
            minterms = get_minterms(dnf, N)
            mu = compute_mean_width(minterms, N)
            bound = 3 * math.log(s + 1) * (math.log(N) + 1)
            if mu > 2 * bound:
                conjecture_holds = False
                counterexample = f"Monotone DNF with s={s}, N={N} has μ={mu} > 2*bound={2*bound}"
                return {
                    "metric_name": metric_name,
                    "metric_value": mu,
                    "instances_tested": instances_tested,
                    "conjecture_holds": conjecture_holds,
                    "counterexample": counterexample
                }
            metric_value += mu
            instances_tested += 1

    # Test k-CLIQUE indicators
    v_values = list(range(4, 10))
    mu_values = []
    for v in v_values:
        k = math.ceil(math.log2(v))
        dnf = generate_k_clique_dnf(v, k)
        minterms = get_minterms(dnf, v * (v - 1) // 2)
        mu = compute_mean_width(minterms, v * (v - 1) // 2)
        mu_values.append(mu)
        if mu < 0.5 * v / 2:
            conjecture_holds = False
            counterexample = f"k-CLIQUE indicator with v={v} has μ={mu} < 0.5*v/2={0.5*v/2}"
            return {
                "metric_name": metric_name,
                "metric_value": mu,
                "instances_tested": instances_tested,
                "conjecture_holds": conjecture_holds,
                "counterexample": counterexample
            }
        metric_value += mu
        instances_tested += 1

    # Regression analysis for k-CLIQUE
    if len(v_values) == len(mu_values):
        n = len(v_values)
        sum_v = sum(v_values)
        sum_mu = sum(mu_values)
        sum_v_sq = sum(v * v for v in v_values)
        sum_v_mu = sum(v * mu for v, mu in zip(v_values, mu_values))

        slope = (n * sum_v_mu - sum_v * sum_mu) / (n * sum_v_sq - sum_v * sum_v)
        intercept = (sum_mu - slope * sum_v) / n

        ss_total = sum((mu - sum_mu / n) ** 2 for mu in mu_values)
        ss_res = sum((mu - (slope * v + intercept)) ** 2 for v, mu in zip(v_values, mu_values))
        r_squared = 1 - ss_res / ss_total if ss_total != 0 else 0

        if slope < 0.5 or r_squared < 0.9:
            conjecture_holds = False
            counterexample = f"Regression slope={slope} < 0.5 or R²={r_squared} < 0.9 for k-CLIQUE indicators"

    return {
        "metric_name": metric_name,
        "metric_value": metric_value / instances_tested if instances_tested > 0 else 0,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        result["seed"] = seed
        print(f"TRIAL: {json.dumps(result)}")
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