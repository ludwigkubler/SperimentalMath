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
    for _ in range(5):
        base_term = random.sample(range(n), k)
        for _ in range(4):
            overlap = random.sample(base_term, k-1)
            new_term = overlap + [random.choice(list(set(range(n)) - set(overlap)))]
            terms.append(frozenset(new_term))
    return terms

def generate_clique_dnf(v):
    terms = []
    for i in range(v):
        for j in range(i+1, v):
            for k in range(j+1, v):
                terms.append(frozenset({i, j, k}))
    return terms

def compute_symdiff_distribution(terms):
    symdiff_counts = {}
    for i, term_i in enumerate(terms):
        for j, term_j in enumerate(terms):
            symdiff = len(term_i.symmetric_difference(term_j))
            symdiff_counts[symdiff] = symdiff_counts.get(symdiff, 0) + 1
    return symdiff_counts

def compute_D_rho(symdiff_counts, rho):
    total = sum(count for symdiff, count in symdiff_counts.items())
    if total == 0:
        return 0.0
    D_rho = sum(count * (rho ** symdiff) for symdiff, count in symdiff_counts.items()) / total
    return D_rho

def compute_eta(symdiff_counts):
    D_half = compute_D_rho(symdiff_counts, 0.5)
    D_quarter = compute_D_rho(symdiff_counts, 0.25)
    if D_half <= 0 or D_quarter <= 0:
        return 0.0
    eta = math.log2(D_half) - 2 * math.log2(D_quarter)
    return eta

def run_trial(seed):
    random.seed(seed)
    metric_values = []
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""

    # Family A: Random monotone DNFs
    for n in [12, 18, 24, 30, 36]:
        for k in [2, 3, 4]:
            for s in [n, 2*n, int(n**1.5)]:
                terms = generate_random_dnf(n, k, s)
                symdiff_counts = compute_symdiff_distribution(terms)
                eta = compute_eta(symdiff_counts)
                L = s * k
                if L <= 0:
                    continue
                eta_ratio = eta / math.log2(L + 2)
                metric_values.append(eta_ratio)
                instances_tested += 1
                if eta_ratio > 6:
                    conjecture_holds = False
                    counterexample = f"Random DNF with n={n}, k={k}, s={s} has eta_ratio={eta_ratio} > 6"

    # Family B: Pseudo-clique DNFs
    for n in [12, 18, 24, 30, 36]:
        for k in [2, 3, 4]:
            s = int(n**1.7)
            terms = generate_pseudo_clique_dnf(n, k, s)
            symdiff_counts = compute_symdiff_distribution(terms)
            eta = compute_eta(symdiff_counts)
            L = s * k
            if L <= 0:
                continue
            eta_ratio = eta / math.log2(L + 2)
            metric_values.append(eta_ratio)
            instances_tested += 1
            if eta_ratio > 6:
                conjecture_holds = False
                counterexample = f"Pseudo-clique DNF with n={n}, k={k}, s={s} has eta_ratio={eta_ratio} > 6"

    # Family C: Canonical 3-CLIQUE minimal DNFs
    for v in [5, 6, 7, 8, 9]:
        terms = generate_clique_dnf(v)
        symdiff_counts = compute_symdiff_distribution(terms)
        eta = compute_eta(symdiff_counts)
        eta_ratio = eta / math.sqrt(v)
        metric_values.append(eta_ratio)
        instances_tested += 1
        if eta_ratio < 0.10:
            conjecture_holds = False
            counterexample = f"3-CLIQUE minimal DNF with v={v} has eta_ratio={eta_ratio} < 0.10"

    if not metric_values:
        return {
            "metric_name": "eta_ratio",
            "metric_value": 0.0,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "No valid instances tested"
        }

    avg_metric = sum(metric_values) / len(metric_values)
    return {
        "metric_name": "eta_ratio",
        "metric_value": avg_metric,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = sys.argv[1:] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    metric_values = []
    for seed in seeds:
        trial = run_trial(int(seed))
        print(f"TRIAL: {trial}")
        metric_values.append(trial)

    if not metric_values:
        print("RESULT: INCONCLUSIVE reason=no_trials_completed")
        sys.exit(0)

    support_fraction = sum(1 for trial in metric_values if trial["conjecture_holds"]) / len(metric_values)
    mean_metric = sum(trial["metric_value"] for trial in metric_values) / len(metric_values)
    std_metric = math.sqrt(sum((trial["metric_value"] - mean_metric) ** 2 for trial in metric_values) / len(metric_values))

    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    else:
        counterexamples = [trial["counterexample"] for trial in metric_values if trial["counterexample"]]
        if counterexamples:
            first_failing_seed = seeds[metric_values.index(next(trial for trial in metric_values if trial["counterexample"]))]
            print(f"RESULT: FALSIFIED counterexample={counterexamples[0]} first_failing_seed={first_failing_seed}")
        else:
            print("RESULT: INCONCLUSIVE reason=no_counterexamples_found")