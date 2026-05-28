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
    n = 20  # Fixed size for simplicity, can be adjusted if needed
    instances_tested = 30
    
    def construct_sheaf(f):
        sheaf = []
        for i in range(n):
            row = [f[j] if j & (1 << i) else 0 for j in range(2**n)]
            sheaf.append(row)
        return sheaf
    
    def compute_minimal_rank(sheaf):
        m, n = len(sheaf), len(sheaf[0])
        A = [[Fraction(sheaf[i][j]) for j in range(n)] for i in range(m)]
        
        def gaussian_elimination(A):
            rows, cols = len(A), len(A[0])
            rank = 0
            for col in range(cols):
                pivot_row = -1
                for row in range(rank, rows):
                    if A[row][col] != 0:
                        pivot_row = row
                        break
                if pivot_row == -1:
                    continue
                A[pivot_row], A[rank] = A[rank], A[pivot_row]
                rank += 1
                for row in range(rank, rows):
                    factor = A[row][col] / A[pivot_row][col]
                    for j in range(col, cols):
                        A[row][j] -= factor * A[pivot_row][j]
            return rank
        
        return gaussian_elimination(A)
    
    def generate_random_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    total_rank = 0
    counterexample = ""
    conjecture_holds = True
    
    for _ in range(instances_tested):
        f = generate_random_boolean_function(n)
        sheaf = construct_sheaf(f)
        rank = compute_minimal_rank(sheaf)
        
        if rank < math.log2(2**n) or rank > 2 * math.log2(2**n):
            conjecture_holds = False
            counterexample = f"Function with n={n} and rank {rank}"
            break
        
        total_rank += rank
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": total_rank / instances_tested,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_rank = sum(result["metric_value"] for result in results) / len(results)
    std_rank = math.sqrt(sum((result["metric_value"] - mean_rank)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_support")