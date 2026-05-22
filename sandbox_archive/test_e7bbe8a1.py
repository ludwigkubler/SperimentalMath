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

def formal_group_rank(f):
    n = int(math.log2(len(f)))
    A = [[0] * (n + 1) for _ in range(n + 1)]
    for i in range(n + 1):
        for j in range(n + 1):
            if i == 0 and j == 0:
                A[i][j] = 1
            elif i == 0 or j == 0:
                A[i][j] = 0
            else:
                A[i][j] = f[2**(i-1) + 2**(j-1)]
    rank = 0
    for row in A:
        if any(row):
            rank += 1
    return rank

def read_twice_bp_size(f):
    n = int(math.log2(len(f)))
    size = 1
    for i in range(n + 1):
        if f[2**i]:
            size += 1
    return size

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):  # Ensure at least 5 instances per size
            f = generate_boolean_function(n)
            rank = formal_group_rank(f)
            size = read_twice_bp_size(f)
            results.append((rank, size))
    if not results:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "empty_results"
        }
    
    ranks = [r for r, _ in results]
    sizes = [s for _, s in results]
    mean_rank = sum(ranks) / len(ranks)
    mean_size = sum(sizes) / len(sizes)
    correlation_coefficient = sum((r - mean_rank) * (s - mean_size) for r, s in results) / (len(results) * math.sqrt(sum((r - mean_rank)**2 for r in ranks)) * math.sqrt(sum((s - mean_size)**2 for s in sizes)))
    mean_difference = abs(mean_rank - mean_size)
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "conjecture_holds": correlation_coefficient >= 0.8 and mean_difference <= 3,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 6)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")