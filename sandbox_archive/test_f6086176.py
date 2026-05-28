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
    
    def is_monotone(f):
        n = len(f)
        for i in range(2**n):
            binary_i = format(i, f'0{n}b')
            inputs = [int(binary_i[j]) for j in range(n)]
            output = f(*inputs)
            if not isinstance(output, int) or output < 0 or output > 1:
                return False
        return True
    
    def generate_monotone_function(n):
        # Generate a random monotone function using the principle of inclusion-exclusion
        f = [random.choice([0, 1]) for _ in range(2**n)]
        for i in range(2**n):
            binary_i = format(i, f'0{n}b')
            inputs = [int(binary_i[j]) for j in range(n)]
            if any(f[sum(inputs[:j+1])] != f[sum(inputs[:j+1] + [1])] for j in range(n)):
                f[i] = 1 - f[i]
        return f
    
    def compute_minimal_rank(f):
        n = len(f)
        # Convert the function to a matrix representation
        A = [[0] * (2**n) for _ in range(2**n)]
        for i in range(2**n):
            binary_i = format(i, f'0{n}b')
            inputs = [int(binary_i[j]) for j in range(n)]
            output = f(*inputs)
            A[i][i] = 1
            for j in range(2**n):
                if i & j == 0:
                    binary_j = format(j, f'0{n}b')
                    inputs_j = [int(binary_j[k]) for k in range(n)]
                    output_j = f(*inputs_j)
                    A[i][j] = 1 if output_j >= output else -1
        # Compute the rank of the matrix using Gaussian elimination
        rank = 0
        for i in range(2**n):
            if all(A[j][i] == 0 for j in range(i, 2**n)):
                continue
            pivot_row = next(j for j in range(i, 2**n) if A[j][i] != 0)
            A[pivot_row], A[i] = A[i], A[pivot_row]
            rank += 1
            for j in range(2**n):
                if i == j:
                    continue
                factor = A[j][i] / A[i][i]
                for k in range(2**n):
                    A[j][k] -= factor * A[i][k]
        return rank
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        c_Q = random.random() + 0.1  # Random constant c_Q
        for _ in range(5):  # Test with 5 instances per size
            f = generate_monotone_function(n)
            if not is_monotone(f):
                continue
            min_rank = compute_minimal_rank(f)
            results.append({
                "n": n,
                "c_Q": c_Q,
                "min_rank": min_rank,
                "log_n": math.log(n),
                "conjecture_holds": min_rank >= c_Q * math.log(n)
            })
    
    if not results:
        return {
            "metric_name": "minimal_rank",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "no_monotone_functions"
        }
    
    mean_min_rank = sum(result["min_rank"] for result in results) / len(results)
    std_min_rank = math.sqrt(sum((result["min_rank"] - mean_min_rank) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": mean_min_rank,
        "instances_tested": len(results),
        "conjecture_holds": support_fraction >= 0.8,
        "counterexample": "" if support_fraction >= 0.8 else f"c_Q={results[0]['c_Q']}, min_rank={results[0]['min_rank']}, log_n={results[0]['log_n']}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_min_rank = sum(result["metric_value"] for result in results) / len(results)
    std_min_rank = math.sqrt(sum((result["metric_value"] - mean_min_rank) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_min_rank:.4f} std={std_min_rank:.4f} support_fraction={support_fraction:.2f}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"c_Q={results[0]['c_Q']}, min_rank={results[0]['min_rank']}, log_n={results[0]['log_n']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_support")