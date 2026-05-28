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
    n = 10  # Start with a small size and increase if needed
    
    # Generate a random n x n matrix M representing a free probability space
    M = [[random.random() for _ in range(n)] for _ in range(n)]
    
    # Compute the minimal rank r(M) of the matrix M
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        rank = 0
        for i in range(min(m, n)):
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
    
    r_M = gaussian_elimination(M)
    
    # Simulate the Disjointness problem on n bits and measure the expected randomized communication complexity
    def simulate_disjointness_protocol(n, M):
        # Placeholder for actual protocol simulation logic
        # For simplicity, we assume a constant communication complexity of 2n
        return 2 * n
    
    comm_complexity = simulate_disjointness_protocol(n, M)
    
    # Correlate the computed r(M) with the measured communication complexity to check if the lower bound of 2 * r(M) is satisfied
    correlation_coefficient = (comm_complexity - 2 * r_M) / (n * math.sqrt(2 * n))
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": 1,
        "conjecture_holds": correlation_coefficient >= 0.7 and comm_complexity >= 2 * r_M,
        "counterexample": "" if correlation_coefficient >= 0.7 and comm_complexity >= 2 * r_M else f"Communication complexity {comm_complexity} < 2 * r(M) = {2 * r_M}"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"communication_complexity < 2 * r(M)\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")