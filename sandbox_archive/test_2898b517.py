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

def is_symplectic_form(M):
    n = len(M)
    I = [[0 if i != j else 1 for j in range(n)] for i in range(n)]
    return M @ M == -I and M.T @ M == -I

def symplectic_rank(M, c=0.25):
    n = len(M)
    rank = 0
    while rank < n:
        found = False
        for i in range(n):
            if all(M[i][j] == 0 for j in range(rank)):
                for j in range(rank, n):
                    if M[j][i] != 0:
                        M[i], M[j] = M[j], M[i]
                        found = True
                        break
                if not found:
                    return float('inf')
        rank += 1
    return rank

def generate_disjointness_matrix(n):
    M = [[0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        M[i][i] = 1
    random.shuffle(M)
    return M

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""

    for n in n_values:
        M = generate_disjointness_matrix(n)
        if not is_symplectic_form(M):
            return {
                "metric_name": "symplectic_rank",
                "metric_value": float('inf'),
                "instances_tested": 1,
                "conjecture_holds": False,
                "counterexample": "not_symplectic"
            }
        rank = symplectic_rank(M)
        if rank < c * n:
            conjecture_holds = False
            counterexample = f"rank={rank} < {c}*{n}"
        total_metric_value += rank
        instances_tested += 1

    return {
        "metric_name": "symplectic_rank",
        "metric_value": total_metric_value / instances_tested,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]]
    if not seeds:
        from sympy.ntheory import primerange
        seeds = list(primerange(2, 100))[:30]

    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **{result}**}}")
        results.append(result)

    total_metric_value = sum(r["metric_value"] * r["instances_tested"] for r in results) / sum(r["instances_tested"] for r in results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={total_metric_value} std=0.0 support_fraction=1.0")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient evidence")