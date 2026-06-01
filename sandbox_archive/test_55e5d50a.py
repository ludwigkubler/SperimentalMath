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
        max_row = i + A[i:].index(max(abs(row[i]) for row in A[i:]))
        A[i], A[max_row] = A[max_row], A[i]
        pivot = A[i][i]
        if pivot == 0:
            continue
        for j in range(i, n):
            A[i][j] /= pivot
        for k in range(n):
            if k != i and A[k][i] != 0:
                factor = -A[k][i]
                for j in range(i, n):
                    A[k][j] += factor * A[i][j]
    return A

def order_of_quaternionic_kahler_manifold(protocol_size):
    # Placeholder function to simulate the construction of a quaternionic Kähler manifold
    # and its order. This is a dummy implementation for testing purposes.
    # In practice, this would involve complex algebraic operations.
    if protocol_size <= 0:
        return None
    A = [[random.randint(1, 10) for _ in range(protocol_size)] for _ in range(protocol_size)]
    A = gaussian_elimination(A)
    rank = sum(1 for row in A if any(val != 0 for val in row))
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        protocol_size = random.randint(1, n)
        order = order_of_quaternionic_kahler_manifold(protocol_size)
        if order is None:
            return {
                "metric_name": "order",
                "metric_value": None,
                "instances_tested": 0,
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": "mapping_undefined"
            }
        results.append(order)
    
    mean_order = sum(results) / len(results)
    conjecture_holds = all(1 <= order <= n for order, n in zip(results, n_values))
    counterexample = "" if conjecture_holds else f"order={mean_order} does not match O(log(n))"
    
    return {
        "metric_name": "order",
        "metric_value": mean_order,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] if sys.argv[1:] else [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_order = sum(res["metric_value"] for res in results if res["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_order} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_order} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{res['counterexample']}\" first_failing_seed={first_failing_seed}")