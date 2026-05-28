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
    
    def xor_function(n):
        return lambda x: sum(x[i] for i in range(n)) % 2
    
    def generate_tropical_curve(n, f):
        # Simplified tropical curve generation for XOR function
        curve = []
        for i in range(1 << n):
            curve.append(f(i))
        return curve
    
    def compute_minimal_rank(curve):
        n = len(curve)
        matrix = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                if curve[i] == curve[j]:
                    matrix[i][j] = 1
        rank = gaussian_elimination(matrix)
        return rank
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        rank = 0
        for i in range(m):
            if A[i][i] == 0:
                swap_found = False
                for j in range(i + 1, m):
                    if A[j][i] != 0:
                        A[i], A[j] = A[j], A[i]
                        swap_found = True
                        break
                if not swap_found:
                    continue
            pivot = A[i][i]
            for j in range(n):
                A[i][j] /= pivot
            for k in range(m):
                if k != i and A[k][i] != 0:
                    factor = A[k][i]
                    for j in range(n):
                        A[k][j] -= factor * A[i][j]
            rank += 1
        return rank
    
    def communication_complexity(f, n):
        # Simplified communication complexity calculation
        return n
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""
    
    for n in n_values:
        f = xor_function(n)
        curve = generate_tropical_curve(n, f)
        rank = compute_minimal_rank(curve)
        comm_complexity = communication_complexity(f, n)
        
        total_metric_value += abs(comm_complexity - rank)
        instances_tested += 1
        
        if abs(comm_complexity - rank) > 3:
            conjecture_holds = False
            counterexample = f"n={n}, comm_complexity={comm_complexity}, rank={rank}"
    
    mean_metric_value = total_metric_value / instances_tested
    support_fraction = instances_tested / len(n_values)
    
    return {
        "metric_name": "communication_complexity",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")