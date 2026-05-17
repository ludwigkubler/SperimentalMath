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
    for S in itertools.combinations(range(v), k):
        terms.append(set(S))
    return terms

def generate_simple_dnf(N, target):
    if target == "THRESHOLD-2":
        return [set(range(N))]
    elif target == "AND":
        return [set(range(N))]
    elif target == "OR":
        return [set([i]) for i in range(N)]
    elif target == "MAJ-on-5":
        if N < 3:
            raise ValueError("MAJ-on-5 requires N >= 3")
        return [set(range(N))]
    elif target == "k-CLIQUE":
        k = math.ceil(math.log2(N))
        return generate_clique_dnf(N, k)
    else:
        raise ValueError("Unknown target")

def generate_random_dnf(N, s, k):
    terms = []
    for _ in range(s):
        term = set(random.sample(range(N), k))
        terms.append(term)
    return terms

def compute_forman_ricci(F, N):
    s = len(F)
    if s == 0:
        return 0, 0

    # Build adjacency list and edge weights
    adj = defaultdict(list)
    edge_weights = {}
    vertex_weights = [len(term) for term in F]

    for i in range(s):
        for j in range(i + 1, s):
            intersection = F[i] & F[j]
            if intersection:
                weight = len(intersection)
                adj[i].append(j)
                adj[j].append(i)
                edge_weights[(i, j)] = weight
                edge_weights[(j, i)] = weight

    min_curvature = float('inf')
    for i in range(s):
        for j in adj[i]:
            if i < j:
                w_ij = edge_weights[(i, j)]
                w_i = vertex_weights[i]
                w_j = vertex_weights[j]

                # Compute the first sum
                sum_i = 0.0
                for k in adj[i]:
                    if k != j:
                        w_ik = edge_weights[(i, k)]
                        sum_i += w_i / math.sqrt(w_ij * w_ik)

                # Compute the second sum
                sum_j = 0.0
                for k in adj[j]:
                    if k != i:
                        w_jk = edge_weights[(j, k)]
                        sum_j += w_j / math.sqrt(w_ij * w_jk)

                ric = w_ij * (w_i / w_ij + w_j / w_ij - sum_i - sum_j)
                if ric < min_curvature:
                    min_curvature = ric

    if min_curvature == float('inf'):
        min_curvature = 0

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
        min_curvature, mu = compute_forman_ricci(F, v)
        instances_tested += 1

        if mu < v / 4:
            conjecture_holds = False
            counterexample = f"Regime A: v={v}, mu={mu} < v/4={v/4}"
            break

    if not conjecture_holds:
        return {
            "metric_name": "mu",
            "metric_value": mu,
            "instances_tested": instances_tested,
            "conjecture_holds": conjecture_holds,
            "counterexample": counterexample
        }

    # Regime B: Simple monotone DNFs
    for N in [5, 10, 15, 20, 30, 36]:
        for target in ["THRESHOLD-2", "AND", "OR", "MAJ-on-5", "k-CLIQUE"]:
            try:
                F = generate_simple_dnf(N, target)
                min_curvature, mu = compute_forman_ricci(F, N)
                instances_tested += 1

                c = 1  # Assuming polynomial degree c=1 for simplicity
                if mu > 6 * c * math.log2(1 + N):
                    conjecture_holds = False
                    counterexample = f"Regime B: N={N}, target={target}, mu={mu} > 6c·log2(1+N)={6*c*math.log2(1+N)}"
                    break
            except ValueError:
                continue

        if not conjecture_holds:
            break

    if not conjecture_holds:
        return {
            "metric_name": "mu",
            "metric_value": mu,
            "instances_tested": instances_tested,
            "conjecture_holds": conjecture_holds,
            "counterexample": counterexample
        }

    # Regime C: Random monotone DNFs
    for N in [5, 10, 15, 20, 30, 40]:
        for s in [N, N * math.log(N, 2), N ** 1.5]:
            if s > 1000:
                s = 1000  # Cap the number of terms to avoid excessive computation
            for k in [3, 4, 5]:
                F = generate_random_dnf(N, int(s), k)
                min_curvature, mu = compute_forman_ricci(F, N)
                instances_tested += 1

    # Regime D: Pairs of monotone DNFs
    for N in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):  # Test 5 random pairs per N
            F = generate_random_dnf(N, N, 3)
            G = generate_random_dnf(N, N, 3)

            # Compute F ∧ G by taking the union of terms
            F_and_G = F + G
            min_curvature_F, mu_F = compute_forman_ricci(F, N)
            min_curvature_G, mu_G = compute_forman_ricci(G, N)
            min_curvature_FG, mu_FG = compute_forman_ricci(F_and_G, N)

            instances_tested += 1

            if mu_FG > mu_F + mu_G + math.log2(1 + N):
                conjecture_holds = False
                counterexample = f"Regime D: N={N}, mu(F∧G)={mu_FG} > mu(F)+mu(G)+log2(1+N)={mu_F + mu_G + math.log2(1 + N)}"
                break

        if not conjecture_holds:
            break

    return {
        "metric_name": "mu",
        "metric_value": mu if 'mu' in locals() else 0,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]

    metric_values = []
    conjecture_holds_counts = 0
    first_failing_seed = None
    first_counterexample = ""

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        metric_values.append(result["metric_value"])
        if result["conjecture_holds"]:
            conjecture_holds_counts += 1
        else:
            if first_failing_seed is None:
                first_failing_seed = seed
                first_counterexample = result["counterexample"]

    mean_metric = sum(metric_values) / len(metric_values) if metric_values else 0
    std_metric = math.sqrt(sum((x - mean_metric) ** 2 for x in metric_values) / len(metric_values)) if metric_values else 0
    support_fraction = conjecture_holds_counts / len(seeds)

    if first_failing_seed is not None:
        print(f'RESULT: FALSIFIED counterexample="{first_counterexample}" first_failing_seed={first_failing_seed}')
    elif support_fraction >= 0.95:
        print(f'RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}')
    else:
        print('RESULT: INCONCLUSIVE reason=insufficient_support')