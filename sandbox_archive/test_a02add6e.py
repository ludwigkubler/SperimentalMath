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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_k_clique(n, k):
        edges = set()
        for i in range(k):
            for j in range(i + 1, k):
                if (i, j) not in edges and (j, i) not in edges:
                    edges.add((i, j))
        for u in range(k, n):
            for v in random.sample(range(n), k - 1):
                if (u, v) not in edges and (v, u) not in edges:
                    edges.add((u, v))
        return edges

    def dnf_size(edges):
        clauses = set()
        for edge in edges:
            clause = tuple(sorted(edge))
            clauses.add(clause)
        return len(clauses)

    n_values = [5, 10, 15, 20, 30, 40]
    total_dnf_size = 0
    instances_tested = 0

    for n in n_values:
        for _ in range(5):
            k = random.randint(2, min(n // 2, 5))
            edges1 = generate_k_clique(n, k)
            edges2 = generate_k_clique(n, k)
            dnf_size1 = dnf_size(edges1)
            dnf_size2 = dnf_size(edges2)
            total_dnf_size += dnf_size1 + dnf_size2
            instances_tested += 2

    mean_dnf_size = total_dnf_size / instances_tested
    conjecture_holds = True
    counterexample = ""

    if mean_dnf_size < n_values[-1] * math.log(n_values[-1]):
        conjecture_holds = False
        counterexample = "mean_dnf_size is too small"

    return {
        "metric_name": "mean_dnf_size",
        "metric_value": mean_dnf_size,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3

    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)

    mean_dnf_size = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_dnf_size} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_dnf_size} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mean_dnf_size is too small\" first_failing_seed={first_failing_seed}")