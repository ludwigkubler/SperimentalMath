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
    
    def generate_random_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def communication_complexity_rank_variance(f, n):
        if len(f) != 2**n:
            raise ValueError("Function length must be 2^n")
        
        matrix = [[f[i * (2**(n-1)) + j] for i in range(2**(n-1))] for j in range(2**(n-1))]
        rank = gaussian_elimination(matrix)
        return rank
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        lead = 0
        for r in range(m):
            if lead >= n:
                return 0
            i = r
            while A[i][lead] == 0:
                i += 1
                if i == m:
                    i = r
                    lead += 1
                    if n == lead:
                        return 0
            A[r], A[i] = A[i], A[r]
            for i in range(m):
                if i != r:
                    factor = Fraction(A[i][lead], A[r][lead])
                    for j in range(n):
                        A[i][j] -= factor * A[r][j]
            lead += 1
        return sum(1 for row in A if any(row))

    def entropic_quasi_group_order(f, n):
        # Placeholder function to compute the order of an entropic quasi-group
        # This is a dummy implementation and should be replaced with actual logic
        return random.randint(1, 3)  # Return a random value between 1 and 3

    n = random.choice([5, 10, 15, 20, 30, 40])
    f = generate_random_boolean_function(n)
    
    try:
        rc_f = communication_complexity_rank_variance(f, n)
        order_eq_f = entropic_quasi_group_order(f, n)
        correlation_coefficient = (order_eq_f - rc_f) / max(order_eq_f, rc_f)
        
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": correlation_coefficient,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": abs(correlation_coefficient) >= 0.8 and order_eq_f <= 3 * rc_f,
            "counterexample": "" if conjecture_holds else f"order={order_eq_f}, rc={rc_f}"
        }
    except Exception as e:
        return {
            "metric_name": "error",
            "metric_value": float('nan'),
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": str(e)
        }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_value = sum(result["metric_value"] for result in results) / len(results)
        std_value = math.sqrt(sum((result["metric_value"] - mean_value)**2 for result in results) / len(results))
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        counterexample = next(result["counterexample"] for result in results if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")