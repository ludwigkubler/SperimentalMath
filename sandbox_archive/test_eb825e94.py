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

def generate_random_symmetric_function(n):
    f = [random.randint(0, 1) for _ in range(2**n)]
    for i in range(2**n):
        x = i
        while x != 0:
            if f[x] != f[i ^ ((1 << (n - 1)) - 1)]:
                return None
            x = x & (x - 1)
    return f

def is_symmetric(f, n):
    for i in range(2**n):
        if f[i] != f[i ^ ((1 << (n - 1)) - 1)]:
            return False
    return True

def compute_syntactic_monoid(f, n):
    monoid = set()
    for x in range(2**n):
        for y in range(2**n):
            if f[x] == f[y]:
                monoid.add((x, y))
    return monoid

def apply_quandle_operation(monoid, operation):
    new_monoid = set()
    for (x, y) in monoid:
        new_x = operation(x)
        new_y = operation(y)
        if (new_x, new_y) not in new_monoid:
            new_monoid.add((new_x, new_y))
    return new_monoid

def compute_quandle_rank(monoid):
    n = len(monoid)
    if n == 0:
        return 0
    adjacency_matrix = [[0] * n for _ in range(n)]
    for i, (x1, y1) in enumerate(monoid):
        for j, (x2, y2) in enumerate(monoid):
            if x1 == x2 and y1 == y2:
                adjacency_matrix[i][j] = 1
    rank = 0
    for _ in range(n):
        found = False
        for i in range(n):
            if sum(adjacency_matrix[i]) > 0:
                rank += 1
                for j in range(n):
                    if adjacency_matrix[i][j]:
                        for k in range(n):
                            if adjacency_matrix[j][k]:
                                adjacency_matrix[i][k] = 1
                        found = True
                        break
        if not found:
            break
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36, 38, 40]
    results = []
    for n in n_values:
        f = generate_random_symmetric_function(n)
        if f is None:
            continue
        if not is_symmetric(f, n):
            continue
        monoid = compute_syntactic_monoid(f, n)
        rank = compute_quandle_rank(monoid)
        results.append(rank)
    if len(results) == 0:
        return {
            "metric_name": "quandle_rank",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    mean_rank = sum(results) / len(results)
    expected_rank = n_values[-1] / math.log(n_values[-1])
    return {
        "metric_name": "quandle_rank",
        "metric_value": mean_rank,
        "instances_tested": len(results),
        "conjecture_holds": abs(mean_rank - expected_rank) <= 0.5 * expected_rank,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i + 3 for i in range(5, 8)]
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result["metric_value"])
    mean_rank = sum(results) / len(results)
    support_fraction = sum(1 for r in results if abs(r - n_values[-1] / math.log(n_values[-1])) <= 0.5 * (n_values[-1] / math.log(n_values[-1])))
    if support_fraction >= 24:
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction/len(results)}")
    elif any(not r for r in results):
        first_failing_seed = seeds[results.index(None)]
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence")