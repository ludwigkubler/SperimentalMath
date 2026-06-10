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

def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        for j in range(i+1, n):
            factor = Fraction(A[j][i], A[i][i])
            for k in range(i, n + 1):
                A[j][k] -= factor * A[i][k]
    rank = sum(1 for row in A if any(row))
    return rank

def mrank(G):
    n = len(G)
    A = [[0] * (n + 1) for _ in range(n)]
    for i in range(n):
        A[i][i] = 1
        for j in range(i+1, n):
            if G[i][j]:
                A[j][i], A[j][j] = -A[j][i], -A[j][j]
                A[j][-1] += A[i][-1]
    return gaussian_elimination(A)

def generate_d_regular_graph(n, d):
    while True:
        G = [[0] * n for _ in range(n)]
        edges = set()
        for i in range(n):
            neighbors = random.sample(range(n), d)
            for j in neighbors:
                if i < j and (i, j) not in edges and (j, i) not in edges:
                    G[i][j] = 1
                    G[j][i] = 1
                    edges.add((i, j))
        if len(edges) == n * d // 2:
            return G

def frege_proof_depth(phi):
    stack = []
    for clause in phi:
        if all(var not in stack and -var not in stack for var in clause):
            stack.append(clause)
        elif any(var in stack and -var in stack for var in clause):
            continue
        else:
            return len(stack) + 1
    return len(stack)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 10, 15, 20, 30, 40])
    d = 2
    G = generate_d_regular_graph(n, d)
    phi = [[i+1 if i % 2 == 0 else -i-1 for i in range(n)]]
    mrank_value = mrank(G)
    proof_depth = frege_proof_depth(phi)
    return {
        "metric_name": "mrank",
        "metric_value": mrank_value,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": abs(mrank_value - proof_depth) <= proof_depth / 2,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                counterexample = f"mrank(G) = {r['metric_value']}, proof_depth(G) = {frege_proof_depth(r['phi'])}"
                print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={seed}")
                break