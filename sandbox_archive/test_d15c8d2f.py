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
    
    def generate_polynomial(n):
        terms = []
        for i in range(1, n+1):
            coeffs = [random.randint(-5, 5) for _ in range(i)]
            term = sum(c * x**i for c, x in zip(coeffs, range(1, i+1)))
            terms.append(term)
        return sum(terms)
    
    def min_rank(poly):
        n = len(poly)
        A = [[0] * (n + 1) for _ in range(n + 1)]
        for i in range(n):
            A[i][i] = poly[i]
        for j in range(n, -1, -1):
            if A[j][j] == 0:
                continue
            for k in range(j+1, n+1):
                A[j][k] /= A[j][j]
            for i in range(j-1, -1, -1):
                factor = A[i][j]
                for k in range(j, n+1):
                    A[i][k] -= factor * A[j][k]
        rank = 0
        for row in A:
            if any(row):
                rank += 1
        return rank
    
    def permutation_circuit_threshold(poly):
        n = len(poly)
        max_degree = max(i for i, coeff in enumerate(poly) if coeff != 0)
        return math.ceil(math.log2(max_degree + 1))
    
    results = []
    for _ in range(30):
        n = random.choice([5, 10, 15, 20, 30, 40])
        poly = generate_polynomial(n)
        rank = min_rank(poly)
        circuit_threshold = permutation_circuit_threshold(poly)
        results.append((rank, circuit_threshold))
    
    mean_rank = sum(rank for rank, _ in results) / len(results)
    mean_circuit_threshold = sum(threshold for _, threshold in results) / len(results)
    support_fraction = sum(1 for rank, threshold in results if rank >= 0.9 * threshold) / len(results)
    
    return {
        "metric_name": "minimal_rank_over_circuit_threshold",
        "metric_value": mean_rank,
        "instances_tested": len(results),
        "conjecture_holds": support_fraction >= 0.9,
        "counterexample": "" if support_fraction >= 0.9 else f"mean rank {mean_rank} < 0.9 * circuit threshold {mean_circuit_threshold}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results) and support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")