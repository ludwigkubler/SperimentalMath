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

def generate_random_dnf(seed, n, k, s, L):
    random.seed(seed)
    terms = []
    for _ in range(s):
        term = set(random.sample(range(n), k))
        terms.append(term)
    return terms

def generate_pseudo_clique_dnf(seed, n, k, s, L):
    random.seed(seed)
    terms = []
    for _ in range(s):
        term = set(random.sample(range(n), k))
        terms.append(term)
    # Plant high-overlap blocks
    for _ in range(5):
        base_term = set(random.sample(range(n), k))
        for _ in range(4):
            new_term = base_term.copy()
            new_term.update(random.sample(range(n), 1))
            terms.append(new_term)
    return terms[:s]

def generate_clique_dnf(v):
    n = v
    s = math.comb(v, 3)
    terms = []
    for i, j, k in itertools.combinations(range(v), 3):
        term = {i, j, k}
        terms.append(term)
    return terms

def compute_D_rho(F, rho):
    s = len(F)
    total = 0.0
    for i in range(s):
        for j in range(s):
            sym_diff = len(F[i] ^ F[j])
            total += rho ** sym_diff
    return total / (s * s)

def compute_eta(F):
    D_half = compute_D_rho(F, 0.5)
    D_quarter = compute_D_rho(F, 0.25)
    if D_half <= 0 or D_quarter <= 0:
        return float('inf')
    log_D_half = math.log2(D_half)
    log_D_quarter = math.log2(D_quarter)
    return log_D_half - 2 * log_D_quarter

def run_trial(seed):
    random.seed(seed)
    n_values = [12, 18, 24, 30, 36]
    k_values = [2, 3, 4]
    s_values = [n * n, 2 * n * n, n * n * n]  # n^{1.5} is n^3 in this context

    # Family A: Random monotone DNFs
    for n in n_values:
        for k in k_values:
            for s in s_values:
                if s > n * n * n:  # Ensure s is reasonable
                    continue
                L = s * k
                F = generate_random_dnf(seed, n, k, s, L)
                eta = compute_eta(F)
                log_L_plus_2 = math.log2(L + 2)
                if log_L_plus_2 <= 0:
                    continue
                ratio = eta / log_L_plus_2
                if ratio > 6:
                    return {
                        "metric_name": "eta/log2(L+2)",
                        "metric_value": ratio,
                        "instances_tested": 1,
                        "conjecture_holds": False,
                        "counterexample": f"Random DNF with n={n}, k={k}, s={s}, L={L}, eta={eta}, ratio={ratio}"
                    }

    # Family B: Adversarial pseudo-clique DNFs
    for n in n_values:
        for k in k_values:
            s = int(n ** 1.7)
            L = s * k
            F = generate_pseudo_clique_dnf(seed, n, k, s, L)
            eta = compute_eta(F)
            log_L_plus_2 = math.log2(L + 2)
            if log_L_plus_2 <= 0:
                continue
            ratio = eta / log_L_plus_2
            if ratio > 6:
                return {
                    "metric_name": "eta/log2(L+2)",
                    "metric_value": ratio,
                    "instances_tested": 1,
                    "conjecture_holds": False,
                    "counterexample": f"Pseudo-clique DNF with n={n}, k={k}, s={s}, L={L}, eta={eta}, ratio={ratio}"
                }

    # Family C: Canonical 3-CLIQUE minimal DNFs
    v_values = [5, 6, 7, 8, 9]
    for v in v_values:
        F = generate_clique_dnf(v)
        eta = compute_eta(F)
        sqrt_v = math.sqrt(v)
        if sqrt_v <= 0:
            continue
        ratio = eta / sqrt_v
        if ratio < 0.10:
            return {
                "metric_name": "eta/sqrt(v)",
                "metric_value": ratio,
                "instances_tested": 1,
                "conjecture_holds": False,
                "counterexample": f"3-CLIQUE DNF with v={v}, eta={eta}, ratio={ratio}"
            }

    return {
        "metric_name": "eta/log2(L+2) or eta/sqrt(v)",
        "metric_value": 0.0,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    metric_values = []
    conjecture_holds_all = True
    counterexample = ""

    for seed in seeds:
        trial = run_trial(seed)
        print(f"TRIAL: {trial}")
        metric_values.append(trial["metric_value"])
        if not trial["conjecture_holds"]:
            conjecture_holds_all = False
            counterexample = trial["counterexample"]

    mean_metric = sum(metric_values) / len(metric_values) if metric_values else 0.0
    std_metric = math.sqrt(sum((x - mean_metric) ** 2 for x in metric_values) / len(metric_values)) if metric_values else 0.0
    support_fraction = sum(1 for trial in metric_values if trial["conjecture_holds"]) / len(metric_values) if metric_values else 0.0

    if not conjecture_holds_all:
        print(f'RESULT: FALSIFIED counterexample="{counterexample}" first_failing_seed={seeds[0]}')
    elif support_fraction >= 0.8:
        print(f'RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}')
    else:
        print('RESULT: INCONCLUSIVE reason=insufficient_support')