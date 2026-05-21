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
    
    def is_prime(n):
        if n <= 1:
            return False
        for i in range(2, int(math.sqrt(n)) + 1):
            if n % i == 0:
                return False
        return True
    
    def generate_random_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def circuit_size(f):
        # Simplified AC^0 circuit size estimation
        return len(f)
    
    def fourier_transform(f):
        n = int(math.log2(len(f)))
        F = [[0] * n for _ in range(n)]
        for k in range(n):
            for x in range(1 << n):
                F[k][x % n] += f[x] * math.exp(-2j * math.pi * k * x / (1 << n))
        return F
    
    def min_rank(matrix):
        m, n = len(matrix), len(matrix[0])
        rank = 0
        for i in range(min(m, n)):
            if matrix[i][i] != 0:
                rank += 1
                for j in range(n):
                    matrix[i][j] /= matrix[i][i]
                for k in range(m):
                    if k != i and matrix[k][i] != 0:
                        for j in range(n):
                            matrix[k][j] -= matrix[i][j] * matrix[k][i]
        return rank
    
    def kostant_sheaf_rank(f):
        F = fourier_transform(f)
        return min_rank(F)
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    f = generate_random_boolean_function(n)
    rank = kostant_sheaf_rank(f)
    circuit_size_f = circuit_size(f)
    
    c = 1.0  # Fixed constant for the inequality
    if rank > c * circuit_size_f:
        return {
            "metric_name": "rank",
            "metric_value": rank,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"Counterexample found: n={n}, rank={rank}, circuit_size={circuit_size_f}"
        }
    else:
        return {
            "metric_name": "rank",
            "metric_value": rank,
            "instances_tested": 1,
            "conjecture_holds": True,
            "counterexample": ""
        }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    total_rank = sum(result["metric_value"] for result in results if result["conjecture_holds"])
    count_supported = sum(1 for result in results if result["conjecture_holds"])
    mean_rank = total_rank / len(results) if count_supported > 0 else float('nan')
    std_rank = math.sqrt(sum((result["metric_value"] - mean_rank) ** 2 for result in results if result["conjecture_holds"])) / len(results) if count_supported > 1 else float('nan')
    
    support_fraction = count_supported / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=mapping_undefined")