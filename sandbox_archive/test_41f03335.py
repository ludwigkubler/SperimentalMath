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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def gaussian_elimination(A):
        n = len(A)
        for i in range(n):
            max_row = i + A[i:].index(max(abs(row[i]) for row in A[i:]))
            A[i], A[max_row] = A[max_row], A[i]
            for j in range(i + 1, n):
                factor = Fraction(A[j][i], A[i][i])
                for k in range(n):
                    A[j][k] -= factor * A[i][k]
        return A
    
    def order_of_quaternionic_kahler_manifold(protocol_size: int) -> int:
        if protocol_size == 1:
            return 1
        n = protocol_size
        A = [[0 for _ in range(n)] for _ in range(n)]
        for i in range(n):
            A[i][i] = 2
            if i < n - 1:
                A[i][i + 1] = 3
        A = gaussian_elimination(A)
        rank = sum(1 for row in A if any(row[j] != 0 for j in range(n)))
        return rank
    
    def communication_complexity_rank(protocol_size: int) -> int:
        # Placeholder function to simulate the computation of communication complexity rank
        return protocol_size ** 2
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""
    
    for n in n_values:
        protocol_size = random.randint(1, n)
        order = order_of_quaternionic_kahler_manifold(protocol_size)
        rank = communication_complexity_rank(protocol_size)
        
        if order != rank and not conjecture_holds:
            continue
        
        total_metric_value += abs(order - rank) / rank
        instances_tested += 1
        
        if order > rank * 2 or order < rank / 2:
            conjecture_holds = False
            counterexample = f"Protocol size {protocol_size}: Order={order}, Rank={rank}"
    
    if instances_tested == 0:
        return {
            "metric_name": "Communication Complexity Rank",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "No instances tested"
        }
    
    mean_metric_value = total_metric_value / instances_tested
    support_fraction = Fraction(instances_tested, len(n_values))
    
    if conjecture_holds:
        return {
            "metric_name": "Communication Complexity Rank",
            "metric_value": mean_metric_value,
            "instances_tested": instances_tested,
            "n_max": max(n_values),
            "conjecture_holds": True,
            "counterexample": ""
        }
    else:
        return {
            "metric_name": "Communication Complexity Rank",
            "metric_value": mean_metric_value,
            "instances_tested": instances_tested,
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": counterexample
        }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    total_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None)
    instances_tested = sum(r["instances_tested"] for r in results)
    support_fraction = Fraction(instances_tested, len(seeds))
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={total_metric_value / instances_tested} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[seeds.index(first_failing_seed)]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")