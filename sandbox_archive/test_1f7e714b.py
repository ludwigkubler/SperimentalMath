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
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction

def generate_cnf(n):
    clauses = []
    for _ in range(2 * n):
        clause = [random.randint(-n, -1), random.randint(1, n)]
        if random.choice([True, False]):
            clause = [-x for x in clause]
        clauses.append(clause)
    return clauses

def kneser_graph(n, k):
    V = set()
    E = []
    for i in range(n + 1):
        for j in range(i + 1, n + 1):
            if abs(i - j) == k:
                V.add((i, j))
                for l in range(n + 1):
                    if l != i and l != j and abs(l - i) == k and abs(l - j) == k:
                        E.append(((i, j), (l,)))
    return V, E

def automorphism_group(V, E):
    n = len(V)
    perm_count = 0
    for p in range(math.factorial(n)):
        if all((V.index(u), V.index(v)) in E == ((p % n) + i, (p // n) + j) in E for u, v in E):
            perm_count += 1
    return perm_count

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        cnf = generate_cnf(n)
        V, E = kneser_graph(n, 1)
        perm_count = automorphism_group(V, E)
        min_degree = len(E) / len(V)
        satisfying_assignments = 2**n - len(cnf)
        results.append({
            "metric_name": "perm_count",
            "metric_value": perm_count,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": perm_count <= n**2 * math.log(n) and min_degree >= satisfying_assignments,
            "counterexample": "" if perm_count <= n**2 * math.log(n) and min_degree >= satisfying_assignments else f"perm_count={perm_count}, min_degree={min_degree}, satisfying_assignments={satisfying_assignments}"
        })
    return {
        "seed": seed,
        "metric_name": "perm_count",
        "metric_value": sum(res["metric_value"] for res in results),
        "instances_tested": len(results),
        "n_max": max(res["n_max"] for res in results),
        "conjecture_holds": all(res["conjecture_holds"] for res in results),
        "counterexample": next((res["counterexample"] for res in results if not res["conjecture_holds"]), "")
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 30))  # Default to first 30 primes if no seeds provided
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_metric_value = sum(res["metric_value"] for res in results) / len(results)
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] for res in results):
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=unknown")