# auto-injected by SEC sandbox
import itertools
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from itertools import product, combinations, permutations, chain
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math

def gaussian_elimination(A):
    m, n = len(A), len(A[0])
    rank = 0
    for j in range(n):
        pivot_row = -1
        for i in range(rank, m):
            if A[i][j] == 1:
                pivot_row = i
                break
        if pivot_row == -1:
            continue
        A[pivot_row], A[rank] = A[rank], A[pivot_row]
        rank += 1
        for i in range(m):
            if i != rank - 1 and A[i][j] == 1:
                for k in range(n):
                    A[i][k] ^= A[rank - 1][k]
    return rank

def generate_k_clique_dnf(n, k):
    edges = [(i, j) for i in range(n) for j in range(i + 1, n)]
    cliques = [edges for _ in range(math.comb(n, k))]
    dnf = []
    for clique in cliques:
        term = [0] * (n * n)
        for u, v in clique:
            term[u * n + v] = 1
        dnf.append(term)
    return dnf

def generate_random_dnf(n, m, w):
    terms = random.sample(range(n * n), m)
    dnf = []
    for term in terms:
        row = [0] * (n * n)
        for i in range(w):
            u, v = divmod(term, n)
            row[u * n + v] = 1
            term -= 1
        dnf.append(row)
    return dnf

def compute_delta(dnf, N):
    m = len(dnf)
    A = [term[:] for term in dnf]
    rank = gaussian_elimination(A)
    return math.log2(m + 1) - math.log2(rank + 1)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    n_values = [6, 8, 10, 12]
    k_values = [3, 4, n // 2]
    
    for n in n_values:
        clique_dnf = generate_k_clique_dnf(n, k_values[2])
        for _ in range(30):
            dnf = generate_random_dnf(n, random.choice([n, n**2, n * math.floor(math.log(n))]), random.choice([2, 3, math.floor(math.log(n))]))
            delta = compute_delta(dnf, n)
            results.append((delta, "random", n))
        
        for k in k_values:
            dnf = clique_dnf
            delta = compute_delta(dnf, n)
            results.append((delta, f"clique_{k}", n))
    
    total_instances = len(results)
    support_count = 0
    counterexample = ""
    
    for delta, type_, n in results:
        if type_ == "random":
            if delta > math.log2(n + 1) + 1:
                counterexample = f"Random DNF with Δ > log_2({n}+1)+1"
                break
        elif type_.startswith("clique"):
            k = int(type_[6:])
            expected_delta = n / 2 - 3 * math.log2(n) - 4
            if delta < expected_delta:
                counterexample = f"Clique DNF with Δ(F^{n},{k}) < {expected_delta}"
                break
    
    support_fraction = sum(1 for _, type_, _ in results if type_ == "random" and compute_delta(generate_random_dnf(n, n, 2), n) <= math.log2(n + 1)) / total_instances
    conjecture_holds = support_fraction >= 0.99
    
    return {
        "metric_name": "Delta",
        "metric_value": sum(delta for delta, _, _ in results) / total_instances,
        "instances_tested": total_instances,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(3, 6)]
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
    
    deltas = [result["metric_value"] for result in results if result["type"] == "random"]
    support_fraction = sum(result["conjecture_holds"] for result in results if result["type"] == "random") / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={sum(deltas)/len(deltas):.2f} std={math.sqrt(sum((d - sum(deltas)/len(deltas))**2 for d in deltas) / len(deltas)):.2f} support_fraction={support_fraction:.2f}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")