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

def generate_minterms(s, N):
    minterms = []
    for _ in range(s):
        minterm = [0] * N
        for i in range(N):
            if random.random() < 0.5:
                minterm[i] = 1
        minterms.append(minterm)
    return minterms

def convex_hull(minterms):
    if not minterms:
        return []
    N = len(minterms[0])
    hull = [minterms[0]]
    for m in minterms[1:]:
        new_hull = []
        for h in hull:
            for i in range(N):
                if h[i] < m[i]:
                    new_point = h.copy()
                    new_point[i] = m[i]
                    if new_point not in new_hull:
                        new_hull.append(new_point)
        hull.extend(new_hull)
    return hull

def monte_carlo_mean_width(K, num_samples=2000):
    if not K:
        return 0.0
    N = len(K[0])
    total = 0.0
    for _ in range(num_samples):
        u = [random.gauss(0, 1) for _ in range(N)]
        norm = math.sqrt(sum(x*x for x in u))
        if norm == 0:
            continue
        u = [x/norm for x in u]
        max_dot = max(sum(u[i]*x[i] for i in range(N)) for x in K)
        total += max_dot
    return 2 * total / num_samples

def generate_clique_dnf(v):
    k = math.ceil(math.log2(v))
    N = v * (v - 1) // 2
    minterms = []
    for edges in itertools.combinations(range(N), k):
        minterm = [0] * N
        for e in edges:
            minterm[e] = 1
        minterms.append(minterm)
    return minterms

def run_trial(seed):
    random.seed(seed)
    s_values = [5, 10, 20, 40]
    N_values = [12, 18, 24, 28]
    v_values = [4, 5, 6, 7, 8, 9]

    metric_values = []
    conjecture_holds = True
    counterexample = ""

    for s in s_values:
        for N in N_values:
            minterms = generate_minterms(s, N)
            K = convex_hull(minterms)
            if not K:
                continue
            mu = monte_carlo_mean_width(K)
            bound = 3 * math.log(s + 1) * (math.log(N) + 1)
            if mu > 2 * bound:
                conjecture_holds = False
                counterexample = f"DNF with s={s}, N={N} has mu={mu} > 2*bound={2*bound}"
                break
            metric_values.append(mu)

    if conjecture_holds:
        for v in v_values:
            minterms = generate_clique_dnf(v)
            K = convex_hull(minterms)
            if not K:
                continue
            mu = monte_carlo_mean_width(K)
            if mu < 0.5 * v:
                conjecture_holds = False
                counterexample = f"k-CLIQUE with v={v} has mu={mu} < 0.5*v={0.5*v}"
                break
            metric_values.append(mu)

    return {
        "metric_name": "mu",
        "metric_value": sum(metric_values) / len(metric_values) if metric_values else 0.0,
        "instances_tested": len(metric_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]

    metric_values = []
    conjecture_holds_counts = 0
    total_trials = 0

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        metric_values.append(result["metric_value"])
        if result["conjecture_holds"]:
            conjecture_holds_counts += 1
        total_trials += 1

    mean_metric = sum(metric_values) / len(metric_values) if metric_values else 0.0
    std_metric = math.sqrt(sum((x - mean_metric) ** 2 for x in metric_values) / len(metric_values)) if metric_values else 0.0
    support_fraction = conjecture_holds_counts / total_trials if total_trials > 0 else 0.0

    if all(result["conjecture_holds"] for result in [run_trial(seed) for seed in seeds]):
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in [run_trial(seed) for seed in seeds]):
        first_failing_seed = next(seed for seed in seeds if not run_trial(seed)["conjecture_holds"])
        counterexample = run_trial(first_failing_seed)["counterexample"]
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")