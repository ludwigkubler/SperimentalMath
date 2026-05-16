# auto-injected by SEC sandbox
import itertools
import os
import time
import re
from itertools import product, combinations, permutations, chain
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import sys
import random
import math
import json
from collections import defaultdict

def matrix_multiply(a, b):
    n = len(a)
    m = len(b[0])
    p = len(b)
    result = [[0 for _ in range(m)] for _ in range(n)]
    for i in range(n):
        for j in range(m):
            for k in range(p):
                result[i][j] += a[i][k] * b[k][j]
    return result

def matrix_transpose(a):
    return [list(row) for row in zip(*a)]

def matrix_norm_inf(a):
    return max(sum(abs(x) for x in row) for row in a)

def generate_random_matrix(n, seed):
    random.seed(seed)
    return [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]

def compute_herdisc_k(a, k):
    n = len(a)
    if k > n:
        return 0
    max_discrepancy = 0
    from itertools import combinations
    for cols in combinations(range(n), k):
        a_subset = [[a[i][j] for j in cols] for i in range(n)]
        min_discrepancy = float('inf')
        for _ in range(10):  # Beck-Fiala rounding iterations
            chi = [random.choice([-1, 1]) for _ in range(k)]
            discrepancy = matrix_norm_inf(matrix_multiply(a_subset, [[x] for x in chi]))
            if discrepancy < min_discrepancy:
                min_discrepancy = discrepancy
        if min_discrepancy > max_discrepancy:
            max_discrepancy = min_discrepancy
    return max_discrepancy

def compute_l(a, seed):
    n = len(a)
    leaves = set()
    random.seed(seed)
    for _ in range(2000):  # Sample 2000 random input pairs
        x = [random.randint(0, 1) for _ in range(n)]
        y = [random.randint(0, 1) for _ in range(n)]
        transcript = []
        for i in range(n):
            if x[i] == 1 and y[i] == 1:
                transcript.append(i)
                break
        leaves.add(tuple(transcript))
    return len(leaves)

def run_trial(seed):
    n_values = [4, 6, 8, 10, 12, 16, 20, 24, 32, 40]
    results = []
    for n in n_values:
        a = generate_random_matrix(n, seed)
        k_max = min(5, math.floor(math.log2(n)) + 2)
        for k in range(2, k_max + 1):
            herdisc = compute_herdisc_k(a, k)
            l = compute_l(a, seed)
            if l == 0:
                continue
            log_l = math.log2(l)
            denominator = 8 * math.sqrt(k * math.log(n))
            if denominator == 0:
                continue
            ratio = (k * herdisc) / denominator
            conjecture_holds = log_l >= ratio
            counterexample = "" if conjecture_holds else f"n={n}, k={k}, seed={seed}"
            results.append({
                "n": n,
                "k": k,
                "herdisc_k": herdisc,
                "L": l,
                "log2_L": log_l,
                "ratio": ratio,
                "conjecture_holds": conjecture_holds,
                "counterexample": counterexample
            })
    if not results:
        return {
            "metric_name": "log2_L / ratio",
            "metric_value": 0.0,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    metric_values = [r["log2_L"] / r["ratio"] for r in results if r["ratio"] != 0]
    mean_metric = sum(metric_values) / len(metric_values) if metric_values else 0.0
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    counterexamples = [r["counterexample"] for r in results if not r["conjecture_holds"]]
    return {
        "metric_name": "log2_L / ratio",
        "metric_value": mean_metric,
        "instances_tested": len(results),
        "conjecture_holds": support_fraction >= 0.95,
        "counterexample": counterexamples[0] if counterexamples else ""
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [42 + i for i in range(30)]
    trials = []
    for seed in seeds:
        result = run_trial(seed)
        print(f'TRIAL: {json.dumps({"seed": seed, **result})}')
        trials.append(result)
    metric_values = [t["metric_value"] for t in trials if t["metric_value"] != 0.0]
    if not metric_values:
        print('RESULT: INCONCLUSIVE reason=metric_saturation')
        sys.exit(0)
    mean_metric = sum(metric_values) / len(metric_values)
    std_metric = math.sqrt(sum((x - mean_metric) ** 2 for x in metric_values) / len(metric_values))
    support_fraction = sum(1 for t in trials if t["conjecture_holds"]) / len(trials)
    counterexamples = [t["counterexample"] for t in trials if not t["conjecture_holds"]]
    if counterexamples:
        print(f'RESULT: FALSIFIED counterexample="{counterexamples[0]}" first_failing_seed={seeds[trials.index(next(t for t in trials if not t["conjecture_holds"]))]}')
    elif support_fraction >= 0.95:
        print(f'RESULT: SUPPORTED mean={mean_metric:.4f} std={std_metric:.4f} support_fraction={support_fraction:.4f}')
    else:
        print('RESULT: INCONCLUSIVE reason=insufficient_support')