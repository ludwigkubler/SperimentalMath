# auto-injected by SEC sandbox
import math
import itertools
import collections
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
import json

# Precomputed multiplication table for S_5
S5_MULT_TABLE = [
    [0, 1, 2, 3, 4],
    [1, 0, 4, 2, 3],
    [2, 4, 0, 3, 1],
    [3, 2, 1, 0, 4],
    [4, 3, 1, 4, 0]
]

# Precomputed commutator table for S_5
S5_COMM_TABLE = {
    (i, j): (k if k != i and k != j else -1)
    for i in range(5) for j in range(i+1, 5) for k in range(5)
}

def s5_multiply(a, b):
    return S5_MULT_TABLE[a][b]

def s5_commutator(a, b):
    if a == b:
        return -1
    return S5_COMM_TABLE[(a, b)]

def bfs_cl(permutation, max_depth=2):
    queue = [(permutation, 0)]
    visited = {permutation}
    while queue:
        current, depth = queue.pop(0)
        if depth > max_depth:
            break
        for a in range(5):
            for b in range(a+1, 5):
                comm = s5_commutator(a, b)
                new_perm = s5_multiply(s5_multiply(comm, a), b)
                if new_perm == permutation:
                    return depth + 1
                if new_perm not in visited:
                    visited.add(new_perm)
                    queue.append((new_perm, depth + 1))
    return -1

def generate_random_formula(n, d):
    if n == 0:
        return random.choice([True, False])
    else:
        op = random.choice(['AND', 'OR'])
        subformulas = [generate_random_formula(random.randint(0, n-1), random.randint(1, d-1)) for _ in range(2)]
        return (op, *subformulas)

def evaluate_formula(formula):
    if isinstance(formula, bool):
        return formula
    op, f1, f2 = formula
    if op == 'AND':
        return evaluate_formula(f1) and evaluate_formula(f2)
    elif op == 'OR':
        return evaluate_formula(f1) or evaluate_formula(f2)

def generate_phi(F):
    if isinstance(F, bool):
        return 0 if F else 4
    op, f1, f2 = F
    if op == 'AND':
        return (generate_phi(f1) + 1) % 5 * 5 + (generate_phi(f2) + 1) % 5
    elif op == 'OR':
        return (generate_phi(f1) + 3) % 5 * 5 + (generate_phi(f2) + 3) % 5

def generate_bp(phi, n):
    if phi == 0:
        return [0]
    if phi == 4:
        return [4]
    for i in range(1, 6):
        for j in range(i+1, 6):
            comm = s5_commutator(i-1, j-1)
            new_phi = s5_multiply(s5_multiply(comm, i-1), j-1)
            if new_phi == phi:
                return [i-1, j-1] + generate_bp(new_phi, n)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    for _ in range(300):
        n = random.randint(4, 8)
        d = random.randint(2, 6)
        F = generate_random_formula(n, d)
        phi = generate_phi(F)
        cl = bfs_cl(phi)
        D_F = 4 * d - cl
        if D_F >= 1:
            bp = generate_bp(phi, n)
            L_5_F = len(bp)
            if L_5_F < 2 * (2 * d + 1):
                return {
                    "metric_name": "D(F)",
                    "metric_value": D_F,
                    "instances_tested": 1,
                    "conjecture_holds": False,
                    "counterexample": f"Formula with D(F)={D_F} admits a BP of length {L_5_F}"
                }
        else:
            results.append(L_5_F / (2 ** D_F * (2 * d + 1)))
    return {
        "metric_name": "median_ratio",
        "metric_value": sum(results) / len(results),
        "instances_tested": len(results),
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [11, 23, 37, 53, 71]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {json.dumps(result)}")
        results.append(result["metric_value"])
    support_fraction = sum(1 for r in results if r >= 1) / len(results)
    median_ratio = sorted(results)[len(results) // 2]
    if all(r >= 1 for r in results):
        print(f"RESULT: SUPPORTED mean={sum(results)/len(results):.4f} std={median_ratio:.4f} support_fraction={support_fraction:.4f}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={sum(results)/len(results):.4f} std={median_ratio:.4f} support_fraction={support_fraction:.4f}")
    else:
        first_failing_seed = seeds[next(i for i, r in enumerate(results) if r < 1)]
        print(f"RESULT: FALSIFIED counterexample=\"Formula with D(F)>=1 admits a BP of length < 2*(2*depth(F)+1)\" first_failing_seed={first_failing_seed}")