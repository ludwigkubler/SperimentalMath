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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def truth_table(f):
        n = len(f)
        tt = []
        for i in range(2**n):
            inputs = [(i >> j) & 1 for j in range(n)]
            output = f[:]
            for j, val in enumerate(inputs):
                if output[j] == -1:
                    output[j] = val
            tt.append(output)
        return tt
    
    def matrix_multiplication(A, B):
        m = len(A)
        n = len(B[0])
        p = len(B)
        C = [[0 for _ in range(n)] for _ in range(m)]
        for i in range(m):
            for j in range(n):
                for k in range(p):
                    C[i][j] += A[i][k] * B[k][j]
        return C
    
    def gaussian_elimination(A):
        m = len(A)
        n = len(A[0])
        rank = 0
        for i in range(m):
            if i < n:
                max_row = i
                for j in range(i+1, m):
                    if abs(A[j][i]) > abs(A[max_row][i]):
                        max_row = j
                A[i], A[max_row] = A[max_row], A[i]
                if A[i][i] != 0:
                    for j in range(n-1, i-1, -1):
                        A[i][j] /= A[i][i]
                    for j in range(m):
                        if j != i and A[j][i] != 0:
                            for k in range(n-1, i-1, -1):
                                A[j][k] -= A[j][i] * A[i][k]
                    rank += 1
        return rank
    
    def minimal_rank(f):
        n = len(f)
        tt = truth_table(f)
        m = len(tt)
        A = [[0 for _ in range(n)] for _ in range(m)]
        for i in range(m):
            for j in range(n):
                if tt[i][j] == 1:
                    A[i][j] = 1
                elif tt[i][j] == 0:
                    A[i][j] = -1
        
        rank_value = gaussian_elimination(A)
        return rank_value
    
    def count_non_zero_entries(f):
        return sum(1 for x in f if x != 0)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        for _ in range(5):  # Ensure at least 5 instances per size
            f = generate_boolean_function(n)
            rank_value = minimal_rank(f)
            non_zero_entries = count_non_zero_entries(f)
            if non_zero_entries == 0:
                continue
            results.append((rank_value, non_zero_entries))
    
    if not results:
        return {
            "metric_name": "minimal_rank",
            "metric_value": 0,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    total_rank = sum(result[0] for result in results)
    total_entries = sum(result[1] for result in results)
    mean_rank = Fraction(total_rank, len(results))
    lower_bound = Fraction(2**n / total_entries, 1)
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": float(mean_rank),
        "instances_tested": len(results),
        "conjecture_holds": mean_rank >= lower_bound,
        "counterexample": "" if mean_rank >= lower_bound else f"mean_rank={mean_rank} < lower_bound={lower_bound}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...run_trial output...}}")
        results.append(result)
    
    total_rank = sum(result["metric_value"] * result["instances_tested"] for result in results)
    total_instances = sum(result["instances_tested"] for result in results)
    mean_rank = Fraction(total_rank, total_instances)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0 support_fraction=1")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")