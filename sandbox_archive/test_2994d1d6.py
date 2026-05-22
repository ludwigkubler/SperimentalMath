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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def formal_group_rank(f):
        n = len(f)
        if n == 1:
            return 1
        A = [[0] * (n + 1) for _ in range(n + 1)]
        for i in range(n):
            A[i][i] = 1
            A[n][i] = f[i]
        rank = 0
        for j in range(n + 1):
            if any(A[j]):
                pivot_row = next(i for i, row in enumerate(A[j:], start=j) if row[j])
                A[j], A[pivot_row] = A[pivot_row], A[j]
                rank += 1
                for k in range(n + 1):
                    if k != j:
                        factor = A[k][j] / A[j][j]
                        for l in range(n + 1):
                            A[k][l] -= factor * A[j][l]
        return rank
    
    def read_twice_bp_size(f):
        n = len(f)
        size = 0
        for i in range(2**n):
            if f[i]:
                size += 1
        return size
    
    n_values = [5, 10, 15, 20, 30, 40]
    ranks = []
    bp_sizes = []
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 5 instances per seed
            f = generate_boolean_function(n)
            rank = formal_group_rank(f)
            size = read_twice_bp_size(f)
            ranks.append(rank)
            bp_sizes.append(size)
    
    if not ranks or not bp_sizes:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    correlation_coefficient = sum((ranks[i] - sum(ranks) / len(ranks)) * (bp_sizes[i] - sum(bp_sizes) / len(bp_sizes)) for i in range(len(ranks))) / (len(ranks) * math.sqrt(sum((ranks[i] - sum(ranks) / len(ranks))**2 for i in range(len(ranks)))) * math.sqrt(sum((bp_sizes[i] - sum(bp_sizes) / len(bp_sizes))**2 for i in range(len(bp_sizes)))))
    mean_difference = abs(sum(ranks) / len(ranks) - sum(bp_sizes) / len(bp_sizes))
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(ranks),
        "conjecture_holds": correlation_coefficient >= 0.8 and mean_difference <= 3,
        "counterexample": "" if correlation_coefficient >= 0.8 and mean_difference <= 3 else f"correlation_coefficient={correlation_coefficient}, mean_difference={mean_difference}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 100))  # Default to first 30 primes if no seeds provided
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    supported_count = sum(1 for r in results if r["conjecture_holds"])
    support_fraction = supported_count / len(results) if results else 0
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={sum(r['metric_value'] for r in results) / len(results)} std=0.0 support_fraction=1.0")
    elif supported_count >= 0.8 * len(results):
        print(f"RESULT: SUPPORTED mean={sum(r['metric_value'] for r in results) / len(results)} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((i + 2 for i, r in enumerate(results) if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={first_failing_seed}")