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

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    return abs(a * b) // gcd(a, b)

def reduce_dnf(dnf):
    terms = set()
    for term in dnf:
        if any(term.issubset(t) for t in terms):
            continue
        for other_term in list(terms):
            if term & other_term:
                terms.remove(other_term)
        terms.add(term)
    return terms

def compute_delta(F, G):
    F_and_G = reduce_dnf([t for t in F + G if any(t1 & t2 for t1 in F for t2 in G)])
    F_or_G = reduce_dnf(F | G)
    delta = compute_mu(F_and_G) + compute_mu(F_or_G) - compute_mu(F) - compute_mu(G)
    return delta

def compute_mu(dnf):
    if not dnf:
        return 0
    n = len(dnf)
    A = [[0] * n for _ in range(n)]
    for i, t1 in enumerate(dnf):
        for j, t2 in enumerate(dnf):
            if i != j and t1 & t2:
                A[i][j] = 1
    deg = [sum(row) for row in A]
    tri = sum(sum(A[i][k] * A[k][j] for k in range(n)) for i, j in itertools.combinations(range(n), 2))
    mu = (4 * n - sum(deg)) / len(A)
    return mu

def run_trial(seed: int) -> dict:
    random.seed(seed)
    N = random.choice([10, 15, 20, 25, 30, 40])
    k = math.ceil(math.log2(N))
    F = set(random.sample(range(1, N+1), k) for _ in range(20))
    G = set(random.sample(range(1, N+1), k) for _ in range(20))
    F = reduce_dnf(F)
    G = reduce_dnf(G)
    delta = compute_delta(F, G)
    return {
        "metric_name": "Delta",
        "metric_value": abs(delta),
        "instances_tested": 1,
        "n_max": N,
        "conjecture_holds": abs(delta) <= 4 * math.sqrt(N),
        "counterexample": "" if abs(delta) <= 4 * math.sqrt(N) else f"Delta={delta} > 4*sqrt({N})"
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_delta = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_delta) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_delta} std={std_dev} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[seeds.index(first_failing_seed)]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")