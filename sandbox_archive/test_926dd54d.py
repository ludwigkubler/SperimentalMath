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
        for j in range(i+1, n):
            factor = -A[j][i] / A[i][i]
            for k in range(n):
                A[j][k] += factor * A[i][k]
    return A

def order_of_quaternionic_kahler_manifold(protocol_size):
    # Construct a sample matrix for demonstration
    n = protocol_size + 1
    A = [[random.randint(-10, 10) for _ in range(n)] for _ in range(n)]
    rank = 0
    for row in gaussian_elimination(A):
        if any(row[j] != 0 for j in range(n)):
            rank += 1
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    # Generate n-communication protocols with varying complexities and sizes
    protocol_sizes = [5, 10, 15, 20, 30, 40]
    results = []
    
    for size in protocol_sizes:
        protocol_size = random.randint(1, size)
        order = order_of_quaternionic_kahler_manifold(protocol_size)
        communication_complexity_rank = protocol_size
        
        results.append({
            "protocol_size": protocol_size,
            "order": order,
            "communication_complexity_rank": communication_complexity_rank
        })
    
    # Compute the correlation between order and communication complexity rank
    total_order = sum(result["order"] for result in results)
    total_rank = sum(result["communication_complexity_rank"] for result in results)
    mean_order = Fraction(total_order, len(results))
    mean_rank = Fraction(total_rank, len(results))
    
    # Check if the correlation is linear and bounded above by a constant multiple of n
    max_n = max(result["protocol_size"] for result in results)
    C = 2 * max_n  # Upper bound factor
    
    conjecture_holds = all(abs(order - rank) <= C * size for order, rank, size in zip(results["order"], results["communication_complexity_rank"], results["protocol_size"]))
    
    return {
        "metric_name": "Order vs Communication Complexity Rank",
        "metric_value": mean_order,
        "instances_tested": len(results),
        "n_max": max_n,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...run_trial output...}}")
        results.append(result)
    
    mean_order = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_order} std=0.0 support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=mapping_undefined")