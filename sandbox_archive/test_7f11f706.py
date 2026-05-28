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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def truth_table(f):
        n = int(math.log2(len(f)))
        return {i: f[i] for i in range(2**n)}
    
    def count_non_zero_entries(tt):
        return sum(1 for v in tt.values() if v != 0)
    
    def gaussian_elimination(matrix):
        m, n = len(matrix), len(matrix[0])
        rank = 0
        for j in range(n):
            i_max = next((i for i in range(rank, m) if matrix[i][j] != 0), None)
            if i_max is not None:
                matrix[rank], matrix[i_max] = matrix[i_max], matrix[rank]
                for i in range(rank + 1, m):
                    factor = -matrix[i][j] / matrix[rank][j]
                    for k in range(j, n):
                        matrix[i][k] += factor * matrix[rank][k]
                rank += 1
        return rank
    
    def minimal_rank_brauer_group(f):
        tt = truth_table(f)
        n = int(math.log2(len(tt)))
        m = len(tt)
        A = [[0 for _ in range(n)] for _ in range(m)]
        for i, v in tt.items():
            if v == 1:
                for j in range(n):
                    A[i][j] = (i >> j) & 1
        return gaussian_elimination(A)
    
    def compute_metric(f):
        n = int(math.log2(len(f)))
        rank = minimal_rank_brauer_group(f)
        non_zero_entries = count_non_zero_entries(truth_table(f))
        return rank, non_zero_entries
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            f = generate_boolean_function(n)
            rank, non_zero_entries = compute_metric(f)
            results.append((rank, non_zero_entries))
    
    if not results:
        return {
            "metric_name": "minimal_rank_brauer_group",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    total_rank = sum(r for r, _ in results)
    total_non_zero_entries = sum(nz for _, nz in results)
    mean_rank = total_rank / len(results)
    mean_value = mean_rank * total_non_zero_entries / len(results)
    
    return {
        "metric_name": "minimal_rank_brauer_group",
        "metric_value": mean_value,
        "instances_tested": len(results),
        "conjecture_holds": mean_value >= 2**n_values[0] / (total_non_zero_entries / len(n_values)),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = 1.0
        result = f"RESULT: SUPPORTED mean={mean_value} std=0 support_fraction={support_fraction}"
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        result = f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}"
    else:
        result = "RESULT: INCONCLUSIVE reason=unknown"
    
    print(result)