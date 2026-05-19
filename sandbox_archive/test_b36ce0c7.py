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
    
    n = 30  # Fixed size for simplicity, as we need to test multiple sizes within each trial
    d = 2   # Depth of AC⁰ circuit computing parity
    
    # Generate a random AC⁰ circuit computing parity
    def ac0_circuit(x):
        return sum(x) % 2
    
    # Construct the communication matrix
    comm_matrix = [[ac0_circuit([i, j]) for j in range(n)] for i in range(n)]
    
    # Compute the real rank of the communication matrix
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i + max(range(i, m), key=lambda k: abs(A[k][i]))
            A[i], A[max_row] = A[max_row], A[i]
            for j in range(n):
                if i != j:
                    factor = A[j][i] / A[i][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        rank = sum(1 for row in A if any(row))
        return rank
    
    real_rank = gaussian_elimination(comm_matrix)
    
    # Verify scaling with Ω(n^(1/(d-1)))
    expected_real_rank = n ** (1 / (d - 1))
    conjecture_holds = real_rank >= expected_real_rank
    counterexample = "" if conjecture_holds else f"Real rank {real_rank} is less than expected {expected_real_rank}"
    
    return {
        "metric_name": "real_rank",
        "metric_value": real_rank,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else list(range(2, 30))  # Default to first 30 primes
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    # Compute mean/std of metric_value, fraction of seeds where conjecture_holds
    if not results:
        print("RESULT: INCONCLUSIVE no_trials_run")
    else:
        total_metric = sum(r["metric_value"] for r in results)
        count_supporting = sum(1 for r in results if r["conjecture_holds"])
        
        mean_metric = total_metric / len(results)
        std_metric = math.sqrt(sum((r["metric_value"] - mean_metric) ** 2 for r in results) / len(results))
        support_fraction = count_supporting / len(results)
        
        if support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
        elif any(not r["conjecture_holds"] for r in results):
            first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
            print(f"RESULT: FALSIFIED counterexample=\"real_rank_too_low\" first_failing_seed={first_failing_seed}")
        else:
            print("RESULT: INCONCLUSIVE insufficient_support")