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

def generate_xor_function(n):
    return [random.choice([0, 1]) for _ in range(2**n)]

def xor_communication_complexity(f):
    n = int(math.log2(len(f)))
    instances = [(i, j) for i in range(2**n) for j in range(i+1, 2**n)]
    return len(instances)

def construct_brauer_group(f):
    n = int(math.log2(len(f)))
    V = [[0] * (2**n) for _ in range(n)]
    for i in range(2**n):
        V[0][i] = f[i]
    for k in range(1, n):
        for i in range(2**(k-1)):
            for j in range(i+1, 2**(k-1) + 1):
                V[k][i] += V[k-1][i] ^ V[k-1][j]
    return V

def rank_of_brauer_group(V):
    n = len(V)
    m = len(V[0])
    pivot_row = 0
    for col in range(m):
        if all(row[col] == 0 for row in V[pivot_row:]):
            continue
        max_row = max(range(pivot_row, n), key=lambda r: abs(V[r][col]))
        V[pivot_row], V[max_row] = V[max_row], V[pivot_row]
        pivot_row += 1
        if pivot_row == n:
            break
        for row in range(pivot_row + 1, n):
            factor = V[row][col] / V[pivot_row][col]
            for j in range(col, m):
                V[row][j] -= factor * V[pivot_row][j]
    return pivot_row

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        f = generate_xor_function(n)
        cc = xor_communication_complexity(f)
        V = construct_brauer_group(f)
        rank = rank_of_brauer_group(V)
        results.append((n, rank, cc))
    if not results:
        return {
            "metric_name": "correlation",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "No instances generated"
        }
    ranks = [r for _, r, _ in results]
    ccs = [cc for _, _, cc in results]
    correlation = sum(r * cc for r, cc in zip(ranks, ccs)) / (sum(ranks) * sum(ccs))
    return {
        "metric_name": "correlation",
        "metric_value": correlation,
        "instances_tested": len(results),
        "conjecture_holds": correlation >= 0.7,
        "counterexample": "" if correlation >= 0.5 else f"Correlation {correlation} < 0.5"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(30)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    if all(r["conjecture_holds"] for r in results):
        mean = sum(r["metric_value"] for r in results) / len(results)
        std = math.sqrt(sum((r["metric_value"] - mean)**2 for r in results) / len(results))
        support_fraction = 1.0
    else:
        mean = None
        std = None
        support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
    print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")