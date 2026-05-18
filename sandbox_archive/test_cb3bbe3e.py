# auto-injected by SEC sandbox
import collections
import json
import os
import time
import re
from collections import defaultdict, Counter, deque
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import sys
import random
import math
from itertools import combinations

def generate_random_dnf(n, k, s):
    terms = []
    for _ in range(s):
        term = random.sample(range(n), k)
        terms.append(frozenset(term))
    return terms

def generate_pseudo_clique_dnf(n, k, s):
    terms = []
    for _ in range(s):
        term = random.sample(range(n), k)
        terms.append(frozenset(term))
    # Plant high-overlap blocks
    for _ in range(s // 5):
        base = random.sample(range(n), k)
        for _ in range(5):
            term = set(base)
            term.update(random.sample(range(n), k - len(base)))
            terms.append(frozenset(term))
    return terms

def generate_clique_dnf(v):
    n = v * (v - 1) // 2
    terms = []
    for i, j in combinations(range(v), 2):
        term = []
        for k in range(v):
            if k != i and k != j:
                term.append(i * (v - 1) + k if i < k else k * (v - 1) + i)
                term.append(j * (v - 1) + k if j < k else k * (v - 1) + j)
        terms.append(frozenset(term))
    return terms, n

def compute_d_rho(terms, rho):
    s = len(terms)
    total = 0.0
    for i in range(s):
        for j in range(s):
            sym_diff = len(terms[i] ^ terms[j])
            total += rho ** sym_diff
    return total / (s * s)

def compute_eta(terms):
    d_half = compute_d_rho(terms, 0.5)
    d_quarter = compute_d_rho(terms, 0.25)
    if d_half <= 0 or d_quarter <= 0:
        return float('inf')
    return math.log2(d_half) - 2 * math.log2(d_quarter)

def run_trial(seed):
    random.seed(seed)
    n_values = [12, 18, 24, 30, 36]
    k_values = [2, 3, 4]
    s_values = [n * n for n in n_values] + [2 * n for n in n_values] + [int(n ** 1.5) for n in n_values]
    v_values = [5, 6, 7, 8, 9]

    metric_values = []
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""

    # Test family A and B
    for n in n_values:
        for k in k_values:
            for s in s_values:
                if s > n:
                    continue
                # Family A: random DNF
                terms = generate_random_dnf(n, k, s)
                eta = compute_eta(terms)
                L = s * k
                if L <= 0:
                    continue
                ratio = eta / math.log2(L + 2)
                metric_values.append(ratio)
                instances_tested += 1
                if ratio > 6.5:
                    conjecture_holds = False
                    counterexample = f"Random DNF with n={n}, k={k}, s={s}, eta={eta}, L={L}, ratio={ratio}"

                # Family B: pseudo-clique DNF
                terms = generate_pseudo_clique_dnf(n, k, s)
                eta = compute_eta(terms)
                L = s * k
                if L <= 0:
                    continue
                ratio = eta / math.log2(L + 2)
                metric_values.append(ratio)
                instances_tested += 1
                if ratio > 6.5:
                    conjecture_holds = False
                    counterexample = f"Pseudo-clique DNF with n={n}, k={k}, s={s}, eta={eta}, L={L}, ratio={ratio}"

    # Test family C
    for v in v_values:
        terms, n = generate_clique_dnf(v)
        eta = compute_eta(terms)
        ratio = eta / math.sqrt(v)
        metric_values.append(ratio)
        instances_tested += 1
        if ratio < 0.05:
            conjecture_holds = False
            counterexample = f"Clique DNF with v={v}, eta={eta}, ratio={ratio}"

    if not metric_values:
        return {
            "metric_name": "eta_ratio",
            "metric_value": 0.0,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "No valid instances generated"
        }

    mean_metric = sum(metric_values) / len(metric_values)
    return {
        "metric_name": "eta_ratio",
        "metric_value": mean_metric,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = sys.argv[1:]
    if not seeds:
        seeds = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]

    metric_values = []
    instances_tested = 0
    conjecture_holds_all = True
    counterexample = ""

    for seed in seeds:
        trial = run_trial(int(seed))
        print(f"TRIAL: {trial}")
        metric_values.append(trial["metric_value"])
        instances_tested += trial["instances_tested"]
        if not trial["conjecture_holds"]:
            conjecture_holds_all = False
            counterexample = trial["counterexample"]

    if not metric_values:
        print("RESULT: INCONCLUSIVE reason=no_valid_instances")
        sys.exit(0)

    mean_metric = sum(metric_values) / len(metric_values)
    std_metric = math.sqrt(sum((x - mean_metric) ** 2 for x in metric_values) / len(metric_values))
    support_fraction = sum(1 for trial in metric_values if trial["conjecture_holds"]) / len(metric_values)

    if conjecture_holds_all:
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    else:
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={seeds[0]}")