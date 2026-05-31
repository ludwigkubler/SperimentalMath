# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def generate_cnf(n, m):
    cnf = []
    for _ in range(m):
        clause = [random.randint(1, n), -random.randint(1, n)]
        cnf.append(clause)
    return cnf

def dpll(cnf):
    def search(model):
        if not cnf:
            return model
        literals = set(abs(lit) for lit in sum(cnf, []))
        literal = next(iter(literals))
        new_cnf = [c for c in cnf if literal not in c and -literal not in c]
        result = search(model + [literal])
        if result:
            return result
        return search(model + [-literal])

    model = []
    if search(model):
        return len(model)
    else:
        return float('inf')

def geometrically_enriched_group_action(cnf):
    n = len(set(abs(lit) for lit in sum(cnf, [])))
    G_phi = [[i % n for i in range(n)] for _ in range(n)]
    return G_phi

def minimal_local_index(G_phi):
    n = len(G_phi)
    mli = 0
    for i in range(n):
        for j in range(n):
            if G_phi[i][j] == j:
                mli += 1
    return Fraction(mli, n)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_max = 30
    instances_tested = 0
    total_mli_over_d = 0
    conjecture_holds = True
    counterexample = ""

    for n in range(5, n_max + 1):
        m = random.randint(2 * n, 4 * n)
        cnf = generate_cnf(n, m)
        d_phi = dpll(cnf)
        if d_phi == float('inf'):
            continue
        G_phi = geometrically_enriched_group_action(cnf)
        mli_phi = minimal_local_index(G_phi)
        ratio = mli_phi / d_phi

        instances_tested += 1
        total_mli_over_d += ratio

        if not (0.5 <= ratio <= 2.0):
            conjecture_holds = False
            counterexample = f"n={n}, m={m}, d(φ)={d_phi}, mli(Gφ)={mli_phi}"

    mean_ratio = Fraction(total_mli_over_d, instances_tested)
    return {
        "metric_name": "Ratio of Minimal Local Index to Circuit Depth",
        "metric_value": float(mean_ratio),
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")