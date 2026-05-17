# auto-injected by SEC sandbox
import json
import os
import time
import re
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import sys
import random
import math
import itertools
from collections import defaultdict

def compute_dt(f, n):
    if n == 0:
        return 0
    for i in range(n):
        fixed_f = defaultdict(int)
        for x in itertools.product([0, 1], repeat=n):
            x_list = list(x)
            x_list[i] = 0
            fixed_f[tuple(x_list)] = f[tuple(x)]
            x_list[i] = 1
            fixed_f[tuple(x_list)] = f[tuple(x)]
        if all(fixed_f[x] == f[x] for x in itertools.product([0, 1], repeat=n)):
            return compute_dt(fixed_f, n-1)
    return n

def hamming_distance(x, y):
    return sum(1 for a, b in zip(x, y) if a != b)

def run_trial(seed):
    random.seed(seed)
    n = random.choice([3, 4, 5])
    f = defaultdict(int)
    for x in itertools.product([0, 1], repeat=n):
        f[x] = random.randint(0, 1)

    d = compute_dt(f, n)
    if d == 0:
        return {
            "metric_name": "delta_bar_ratio",
            "metric_value": 0.0,
            "instances_tested": 1,
            "conjecture_holds": True,
            "counterexample": ""
        }

    M = []
    for x in itertools.product([0, 1], repeat=n):
        row = []
        for y in itertools.product([0, 1], repeat=n):
            xor = tuple(a ^ b for a, b in zip(x, y))
            row.append(f[xor])
        M.append(row)

    distances = []
    for i in range(len(M)):
        for j in range(i+1, len(M)):
            distances.append(hamming_distance(M[i], M[j]))

    delta = 0
    count = 0
    for a, b, c, d in itertools.combinations(range(len(M)), 4):
        s1 = distances[sum(range(a+1, b+1))] + distances[sum(range(c+1, d+1))]
        s2 = distances[sum(range(a+1, c+1))] + distances[sum(range(b+1, d+1))]
        s3 = distances[sum(range(a+1, d+1))] + distances[sum(range(b+1, c+1))]
        sorted_s = sorted([s1, s2, s3], reverse=True)
        delta = max(delta, (sorted_s[0] - sorted_s[1]) / 2)
        count += 1

    diam = max(distances)
    delta_bar = delta / diam if diam != 0 else 0
    ratio = delta_bar * (n + 1) / (n + 1 - d) if (n + 1 - d) != 0 else float('inf')

    conjecture_holds = ratio <= 1
    counterexample = "" if conjecture_holds else f"delta_bar_ratio={ratio} > 1"

    return {
        "metric_name": "delta_bar_ratio",
        "metric_value": ratio,
        "instances_tested": count,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]

    metric_values = []
    conjecture_holds_counts = 0
    total_instances = 0

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        metric_values.append(result["metric_value"])
        conjecture_holds_counts += 1 if result["conjecture_holds"] else 0
        total_instances += result["instances_tested"]

    mean = sum(metric_values) / len(metric_values) if metric_values else 0
    std = math.sqrt(sum((x - mean) ** 2 for x in metric_values) / len(metric_values)) if metric_values else 0
    support_fraction = conjecture_holds_counts / len(seeds) if seeds else 0

    if all(result["conjecture_holds"] for result in [run_trial(seed) for seed in seeds]):
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    else:
        for seed in seeds:
            result = run_trial(seed)
            if not result["conjecture_holds"]:
                print(f"RESULT: FALSIFIED counterexample={result['counterexample']} first_failing_seed={seed}")
                break