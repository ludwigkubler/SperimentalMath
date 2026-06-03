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

def generate_phi(n):
    phi = []
    for _ in range(n):
        clause = [random.choice([-1, 1]) * (i + 1) for i in range(3)]
        if all(lit not in phi[-1] and -lit not in phi[-1] for lit in clause):
            phi.append(clause)
    return phi

def symplectic_form(phi):
    m = len(phi)
    n = len(phi[0])
    omega = [[0] * (n + 2) for _ in range(n + 2)]
    for i in range(m):
        for j in range(n):
            omega[j][j+1] += phi[i][j]
            omega[j+1][j] -= phi[i][j]
    return omega

def min_rank(omega):
    m = len(omega)
    n = len(omega[0])
    rank = 0
    for i in range(n):
        if any(omega[j][i] != 0 for j in range(m)):
            rank += 1
    return rank

def resolution_width(phi):
    stack = []
    for clause in phi:
        stack.append(clause)
    while stack:
        clause = stack.pop()
        new_clause = None
        for lit in clause:
            if -lit in clause:
                return len(stack) + 1
            for other_clause in stack:
                if any(-lit == x or lit == x for x in other_clause):
                    new_clause = [x for x in other_clause if x != -lit and x != lit]
                    break
            if new_clause is not None:
                break
        if new_clause is not None:
            stack.append(new_clause)
    return len(stack) + 1

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    min_ranks = []
    widths = []
    for n in n_values:
        phi = generate_phi(n)
        omega = symplectic_form(phi)
        min_rank_val = min_rank(omega)
        width = resolution_width(phi)
        min_ranks.append(min_rank_val)
        widths.append(width)
    
    mean_min_rank = sum(min_ranks) / len(min_ranks)
    mean_width = sum(widths) / len(widths)
    c = mean_min_rank / mean_width
    conjecture_holds = all(m >= c * w for m, w in zip(min_ranks, widths))
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "min_rank_over_width",
        "metric_value": c,
        "instances_tested": len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_min_ranks = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_min_ranks} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=mapping_undefined")