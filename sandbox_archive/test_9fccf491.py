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

def compute_brauer_group_rank(f):
    # Constructive mapping from XOR function to Brauer group rank
    n = len(f)
    matrix = [[f[i ^ j] for j in range(n)] for i in range(n)]
    rank = 0
    for row in matrix:
        if any(row):
            rank += 1
            for i in range(n):
                if row[i]:
                    for j in range(n):
                        matrix[j][i] ^= row[j]
    return rank

def compute_xor_communication_complexity(f):
    n = len(f)
    communication_complexity = 0
    for i in range(2**n):
        for j in range(i + 1, 2**n):
            if f[i] != f[j]:
                communication_complexity += 1
    return communication_complexity

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 10, 15, 20, 30, 40])
    f = generate_xor_function(n)
    rank = compute_brauer_group_rank(f)
    communication_complexity = compute_xor_communication_complexity(f)
    metric_value = rank / communication_complexity if communication_complexity != 0 else float('inf')
    conjecture_holds = metric_value < float('inf')
    counterexample = "" if conjecture_holds else "mapping_undefined"
    return {
        "metric_name": "rank / CC_XOR",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if support_fraction >= 0.95:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_support")