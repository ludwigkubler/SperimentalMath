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

def generate_boolean_function(n):
    return [random.choice([0, 1]) for _ in range(2**n)]

def communication_distance(f, g):
    n = int(math.log2(len(f)))
    return sum(f[i] != g[i] for i in range(2**n))

def min_plus_representation(f):
    n = int(math.log2(len(f)))
    M = [[float('inf')] * (2**n) for _ in range(2**n)]
    for i in range(2**n):
        for j in range(2**n):
            if 2**i + 2**j < len(f):
                M[i][j] = f[2**i + 2**j]
    return M

def symplectic_hull_rank(M):
    n = len(M)
    I = [[Fraction(1, 1) if i == j else Fraction(0, 1) for j in range(n)] for i in range(n)]
    A = [row[:] for row in M]
    rank = 0
    for k in range(n):
        max_row = -1
        for i in range(k, n):
            if A[i][k] > A[max_row][k]:
                max_row = i
        if A[max_row][k] == Fraction(0, 1):
            continue
        rank += 1
        A[k], A[max_row] = A[max_row], A[k]
        for i in range(n):
            if i != k:
                factor = -A[i][k] / A[k][k]
                for j in range(k, n):
                    A[i][j] += factor * A[k][j]
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    for d in range(2, 41):
        f = generate_boolean_function(d)
        g = generate_boolean_function(d)
        while communication_distance(f, g) != d:
            g = generate_boolean_function(d)
        M_f = min_plus_representation(f)
        rank_f = symplectic_hull_rank(M_f)
        results.append((d, rank_f))
    metric_value = sum(rank for _, rank in results) / len(results)
    conjecture_holds = all(rank <= d**2 for d, rank in results)
    counterexample = "" if conjecture_holds else f"Failed at communication distance {results[0][0]} with rank {results[0][1]}"
    return {
        "metric_name": "Symplectic Hull Rank",
        "metric_value": metric_value,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result["metric_value"])
    
    mean = sum(results) / len(results)
    std = math.sqrt(sum((x - mean)**2 for x in results) / len(results))
    support_fraction = sum(1 for r in results if r <= max(d**2 for d, _ in result["instances"])) / len(results)
    print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")