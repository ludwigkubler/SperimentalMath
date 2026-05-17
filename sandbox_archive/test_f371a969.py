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

def generate_clique_dnf(v, k):
    terms = []
    for subset in itertools.combinations(range(v), k):
        terms.append(set(subset))
    return terms

def generate_random_dnf(N, s, k):
    terms = []
    for _ in range(s):
        term = set(random.sample(range(N), k))
        terms.append(term)
    return terms

def generate_simple_dnf(N, target):
    if target == "THRESHOLD-2":
        terms = [set([i]) for i in range(N)]
    elif target == "AND":
        terms = [set(range(N))]
    elif target == "OR":
        terms = [set([i]) for i in range(N)]
    elif target == "MAJ-on-5":
        terms = [set([i]) for i in range(5)]
    elif target.startswith("k-CLIQUE"):
        k = int(target.split("-")[0][0])
        terms = generate_clique_dnf(N, k)
    else:
        raise ValueError("Unknown target")
    return terms

def compute_forman_ricci(F, N):
    s = len(F)
    if s == 0:
        return 0.0, 0.0

    # Build adjacency list and edge weights
    adj = defaultdict(list)
    edge_weights = {}
    vertex_weights = [len(term) for term in F]

    for i in range(s):
        for j in range(i + 1, s):
            intersection = F[i] & F[j]
            if len(intersection) >= 1:
                adj[i].append(j)
                adj[j].append(i)
                edge_weights[(i, j)] = len(intersection)

    if not edge_weights:
        return 0.0, 0.0

    min_curvature = float('inf')

    for (i, j), w_ij in edge_weights.items():
        w_i = vertex_weights[i]
        w_j = vertex_weights[j]

        sum_i = 0.0
        for k in adj[i]:
            if k != j:
                w_ik = edge_weights.get((i, k), edge_weights.get((k, i), 0))
                if w_ij * w_ik > 0:
                    sum_i += w_i / math.sqrt(w_ij * w_ik)

        sum_j = 0.0
        for k in adj[j]:
            if k != i:
                w_jk = edge_weights.get((j, k), edge_weights.get((k, j), 0))
                if w_ij * w_jk > 0:
                    sum_j += w_j / math.sqrt(w_ij * w_jk)

        ric_ij = w_ij * (w_i / w_ij + w_j / w_ij - sum_i - sum_j)
        if ric_ij < min_curvature:
            min_curvature = ric_ij

    mu = math.log2(1 + max(0, -min_curvature))
    return min_curvature, mu

def run_trial(seed):
    random.seed(seed)
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""

    # Regime A: Canonical minterm DNF for k-CLIQUE on K_v
    for v in [4, 5, 6, 7, 8]:
        k = math.ceil(math.log2(v))
        F = generate_clique_dnf(v, k)
        _, mu = compute_forman_ricci(F, v)
        instances_tested += 1
        if mu < v / 4:
            conjecture_holds = False
            counterexample = f"K_{v} with mu={mu} < v/4={v/4}"
            break

    if not conjecture_holds:
        return {
            "seed": seed,
            "metric_name": "mu(F)",
            "metric_value": mu,
            "instances_tested": instances_tested,
            "conjecture_holds": conjecture_holds,
            "counterexample": counterexample
        }

    # Regime B: Simple monotone DNFs
    targets = ["THRESHOLD-2", "AND", "OR", "MAJ-on-5", "2-CLIQUE"]
    for target in targets:
        N = 36 if target == "MAJ-on-5" else 28
        F = generate_simple_dnf(N, target)
        _, mu = compute_forman_ricci(F, N)
        instances_tested += 1
        c = 1  # Polynomial degree for simple targets
        if mu > 6 * c * math.log2(1 + N):
            conjecture_holds = False
            counterexample = f"{target} with mu={mu} > 6c·log2(1+N)={6*c*math.log2(1+N)}"
            break

    if not conjecture_holds:
        return {
            "seed": seed,
            "metric_name": "mu(F)",
            "metric_value": mu,
            "instances_tested": instances_tested,
            "conjecture_holds": conjecture_holds,
            "counterexample": counterexample
        }

    # Regime C: Random monotone DNFs
    N = 20
    for s in [N, N * math.log(N), N ** 1.5]:
        for k in [3, 4, 5]:
            F = generate_random_dnf(N, int(s), k)
            _, mu = compute_forman_ricci(F, N)
            instances_tested += 1
            c = 1  # Polynomial degree for random DNFs
            if mu > 6 * c * math.log2(1 + N):
                conjecture_holds = False
                counterexample = f"Random DNF with mu={mu} > 6c·log2(1+N)={6*c*math.log2(1+N)}"
                break

    if not conjecture_holds:
        return {
            "seed": seed,
            "metric_name": "mu(F)",
            "metric_value": mu,
            "instances_tested": instances_tested,
            "conjecture_holds": conjecture_holds,
            "counterexample": counterexample
        }

    # Regime D: Pairs of monotone DNFs
    for _ in range(5):
        N = 20
        F = generate_random_dnf(N, N, 3)
        G = generate_random_dnf(N, N, 3)

        # Compute F ∧ G
        F_and_G = []
        for term_F in F:
            for term_G in G:
                intersection = term_F & term_G
                if len(intersection) >= 1:
                    F_and_G.append(intersection)

        if len(F_and_G) > 10000:
            F_and_G = F_and_G[:10000]

        _, mu_F = compute_forman_ricci(F, N)
        _, mu_G = compute_forman_ricci(G, N)
        _, mu_F_and_G = compute_forman_ricci(F_and_G, N)

        instances_tested += 1
        if mu_F_and_G > mu_F + mu_G + math.log2(1 + N):
            conjecture_holds = False
            counterexample = f"Pair (F,G) with mu(F∧G)={mu_F_and_G} > mu(F)+mu(G)+log2(1+N)={mu_F + mu_G + math.log2(1 + N)}"
            break

    return {
        "seed": seed,
        "metric_name": "mu(F)",
        "metric_value": mu_F if conjecture_holds else mu_F_and_G,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]

    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    metric_values = [r["metric_value"] for r in results]
    mean_metric = sum(metric_values) / len(metric_values)
    std_metric = math.sqrt(sum((x - mean_metric) ** 2 for x in metric_values) / len(metric_values))
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        counterexample = next(r["counterexample"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")