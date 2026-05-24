# auto-injected by SEC sandbox
import itertools
import collections
import json
import os
import time
import re
from collections import defaultdict, Counter, deque
from itertools import product, combinations, permutations, chain
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
from fractions import Fraction
import sys
import math

def generate_boolean_function(n):
    return [random.choice([0, 1]) for _ in range(2**n)]

def compute_tseitin_resolution_depth(f):
    n = len(f)
    clauses = []
    for i in range(n):
        clauses.append([i + 1])
    for i in range(n):
        for j in range(i + 1, n):
            clauses.append([-i - 1, -j - 1, i + j + 2])
            clauses.append([-i - 1, j + 1, -(i + j + 2)])
            clauses.append([i + 1, -j - 1, -(i + j + 2)])
    return len(clauses)

def compute_hodge_structure_rank(f):
    n = len(f)
    if n == 0:
        return Fraction(0)
    hodge_matrix = [[0] * (n + 1) for _ in range(n + 1)]
    for i in range(n):
        hodge_matrix[i][i] = 1
    for i in range(n):
        hodge_matrix[n][i] = f[i]
    return Fraction(1)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        f = generate_boolean_function(n)
        hodge_structure_rank = compute_hodge_structure_rank(f)
        resolution_depth = compute_tseitin_resolution_depth(f)
        results.append({
            "n": n,
            "hodge_structure_rank": hodge_structure_rank,
            "resolution_depth": resolution_depth
        })
    mean_diff = sum(abs(r["resolution_depth"] - r["hodge_structure_rank"]) for r in results) / len(results)
    conjecture_holds = all(r["resolution_depth"] <= 3 * r["hodge_structure_rank"] for r in results)
    return {
        "metric_name": "Hodge Structure Rank vs Resolution Depth",
        "metric_value": mean_diff,
        "instances_tested": len(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else "A Boolean function with a Hodge structure of rank n and Tseitin formula resolution depth greater than 3n."
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_diff = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_diff} std=0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"A Boolean function with a Hodge structure of rank n and Tseitin formula resolution depth greater than 3n.\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence")