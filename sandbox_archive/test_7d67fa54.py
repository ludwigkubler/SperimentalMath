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
    for i in range(v):
        term = set()
        for j in range(i, v):
            if j != i:
                term.add((i, j))
        if len(term) >= k:
            terms.append(term)
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
    elif target == "k=2-CLIQUE":
        terms = [set([i, j]) for i in range(N) for j in range(i+1, N)]
    else:
        raise ValueError("Unknown target")
    return terms

def build_term_overlap_graph(terms):
    graph = defaultdict(dict)
    for i, term_i in enumerate(terms):
        for j, term_j in enumerate(terms):
            if i != j:
                intersection = len(term_i & term_j)
                if intersection >= 1:
                    graph[i][j] = intersection
    return graph

def compute_forman_ricci_curvature(graph, terms):
    ricci = {}
    for i in graph:
        for j in graph[i]:
            if (j, i) not in ricci:
                w_ij = graph[i][j]
                w_i = len(terms[i])
                w_j = len(terms[j])
                sum_i = sum(w_i / math.sqrt(w_ij * graph[i][k]) for k in graph[i] if k != j)
                sum_j = sum(w_j / math.sqrt(w_ij * graph[j][k]) for k in graph[j] if k != i)
                ricci[(i, j)] = w_ij * (w_i / w_ij + w_j / w_ij - sum_i - sum_j)
    return ricci

def compute_mu(ricci):
    if not ricci:
        return 0
    min_curvature = min(ricci.values())
    return math.log2(1 + max(0, -min_curvature))

def run_trial(seed):
    random.seed(seed)
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""
    metric_values = []

    # Regime A: Canonical minterm DNF for k-CLIQUE
    for v in [4, 5, 6, 7, 8]:
        k = math.ceil(math.log2(v))
        terms = generate_clique_dnf(v, k)
        graph = build_term_overlap_graph(terms)
        ricci = compute_forman_ricci_curvature(graph, terms)
        mu = compute_mu(ricci)
        metric_values.append(mu)
        instances_tested += 1
        if mu < v / 4:
            conjecture_holds = False
            counterexample = f"Regime A: v={v}, mu={mu} < v/4={v/4}"
            break

    if conjecture_holds:
        # Regime B: Simple monotone DNFs
        targets = ["THRESHOLD-2", "AND", "OR", "MAJ-on-5", "k=2-CLIQUE"]
        for target in targets:
            N = 36
            terms = generate_simple_dnf(N, target)
            graph = build_term_overlap_graph(terms)
            ricci = compute_forman_ricci_curvature(graph, terms)
            mu = compute_mu(ricci)
            metric_values.append(mu)
            instances_tested += 1
            c = math.log2(len(terms)) / math.log2(N) if len(terms) > 1 else 1
            if mu > 6 * c * math.log2(1 + N):
                conjecture_holds = False
                counterexample = f"Regime B: target={target}, mu={mu} > 6c·log2(1+N)={6*c*math.log2(1+N)}"
                break

    if conjecture_holds:
        # Regime C: Random monotone DNFs
        N = 36
        for s in [N, N * math.log2(N), N ** 1.5]:
            for k in [3, 4, 5]:
                terms = generate_random_dnf(N, int(s), k)
                graph = build_term_overlap_graph(terms)
                ricci = compute_forman_ricci_curvature(graph, terms)
                mu = compute_mu(ricci)
                metric_values.append(mu)
                instances_tested += 1

    if conjecture_holds:
        # Regime D: Pairs of DNFs
        N = 36
        for _ in range(5):
            terms1 = generate_random_dnf(N, N, 3)
            terms2 = generate_random_dnf(N, N, 3)
            terms_conj = [t1 & t2 for t1 in terms1 for t2 in terms2 if t1 & t2]
            if len(terms_conj) > 10000:
                terms_conj = terms_conj[:10000]
            graph_conj = build_term_overlap_graph(terms_conj)
            ricci_conj = compute_forman_ricci_curvature(graph_conj, terms_conj)
            mu_conj = compute_mu(ricci_conj)
            graph1 = build_term_overlap_graph(terms1)
            ricci1 = compute_forman_ricci_curvature(graph1, terms1)
            mu1 = compute_mu(ricci1)
            graph2 = build_term_overlap_graph(terms2)
            ricci2 = compute_forman_ricci_curvature(graph2, terms2)
            mu2 = compute_mu(ricci2)
            metric_values.append(mu_conj)
            instances_tested += 1
            if mu_conj - mu1 - mu2 > math.log2(1 + N):
                conjecture_holds = False
                counterexample = f"Regime D: mu_conj={mu_conj} > mu1+mu2+log2(1+N)={mu1+mu2+math.log2(1+N)}"
                break

    if not metric_values:
        metric_value = 0.0
    else:
        metric_value = sum(metric_values) / len(metric_values)

    return {
        "metric_name": "mu",
        "metric_value": metric_value,
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
        print(f"TRIAL: {result}")
        results.append(result)

    metric_values = [r["metric_value"] for r in results]
    mean_metric = sum(metric_values) / len(metric_values)
    std_metric = math.sqrt(sum((x - mean_metric) ** 2 for x in metric_values) / len(metric_values))
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={r['seed']}")
                break