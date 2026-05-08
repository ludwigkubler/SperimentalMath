# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from itertools import combinations

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    return abs(a*b) // gcd(a, b)

def matrix_multiply(A, B):
    m, n = len(A), len(B[0])
    result = [[0] * n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            for k in range(len(B)):
                result[i][j] += A[i][k] * B[k][j]
    return result

def gaussian_elimination(A, b):
    m, n = len(A), len(A[0])
    augmented = [row + [b[i]] for i, row in enumerate(A)]
    for i in range(n):
        max_row = max(range(i, m), key=lambda r: abs(augmented[r][i]))
        augmented[i], augmented[max_row] = augmented[max_row], augmented[i]
        for j in range(i+1, m):
            factor = augmented[j][i] / augmented[i][i]
            for k in range(n + 1):
                augmented[j][k] -= factor * augmented[i][k]
    x = [0] * n
    for i in range(n-1, -1, -1):
        x[i] = (augmented[i][-1] - sum(augmented[i][j] * x[j] for j in range(i+1, n))) / augmented[i][i]
    return x

def rank(A):
    m, n = len(A), len(A[0])
    A_rref = gaussian_elimination(A, [0]*n)
    rank = 0
    for row in A_rref:
        if any(row[j] != 0 for j in range(n)):
            rank += 1
    return rank

def closure(DNF_terms, groundset):
    closure_set = set(groundset)
    changed = True
    while changed:
        changed = False
        for term in DNF_terms:
            if all(x in closure_set for x in term):
                for x in term:
                    if x not in closure_set:
                        closure_set.add(x)
                        changed = True
    return closure_set

def matroid_rank_deficit(M, DNF_terms):
    groundset = set(range(len(M)))
    closure_set = closure(DNF_terms, groundset)
    rank_M = rank(M)
    rank_closure_diff = rank_M - rank(groundset - closure_set)
    return rank_closure_diff

def generate_k_clique_dnf(n, k):
    edges = list(combinations(range(n), 2))
    clique_edges = random.sample(edges, k*(k-1)//2)
    DNF_terms = []
    for i in range(k):
        term = set()
        for j in range(i+1, k):
            term.add(clique_edges[i*k + j - (i+1)*(i//2)][0])
            term.add(clique_edges[i*k + j - (i+1)*(i//2)][1])
        DNF_terms.append(term)
    return DNF_terms

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""

    for n in n_values:
        for _ in range(5):
            M = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
            DNF_terms = generate_k_clique_dnf(n, k=3)
            mu_M = matroid_rank_deficit(M, DNF_terms)
            total_metric_value += mu_M
            instances_tested += 1

    if instances_tested > 0:
        mean_metric_value = total_metric_value / instances_tested
        support_fraction = sum(1 for n in n_values for _ in range(5) if matroid_rank_deficit(M, DNF_terms) <= math.log(n)) / (len(n_values) * 5)
    else:
        mean_metric_value = None
        support_fraction = 0

    return {
        "metric_name": "mu_M",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": support_fraction >= 0.8,
        "counterexample": counterexample if not conjecture_holds else ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_metric_value = sum(r["metric_value"] for r in results if r["instances_tested"] > 0) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no seeds tested")