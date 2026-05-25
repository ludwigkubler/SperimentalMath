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
    
    def generate_read_twice_bp(n):
        if n == 1:
            return [0]
        else:
            bp = []
            for _ in range(n-1):
                bp.append(random.choice([0, 1]))
            bp.append(0)
            return bp
    
    def noncrossing_partition(bp):
        n = len(bp)
        partition = [[i] for i in range(n)]
        for i in range(n-1):
            if bp[i] == 1:
                for j in range(i+1, n):
                    if bp[j] == 0:
                        partition.append(partition.pop(j) + partition.pop(j-1))
                        break
        return partition
    
    def rank_of_partition(partition):
        n = len(partition)
        matrix = [[0]*n for _ in range(n)]
        for i, block in enumerate(partition):
            for j in block:
                for k in block:
                    if j < k:
                        matrix[i][j] += 1
                        matrix[i][k] -= 1
        for i in range(n):
            for j in range(i+1, n):
                matrix[j][i] = -matrix[i][j]
        return gaussian_elimination(matrix)
    
    def gaussian_elimination(A):
        n = len(A)
        rank = 0
        for i in range(n):
            if A[i][i] == 0:
                j = i + 1
                while j < n and A[j][i] == 0:
                    j += 1
                if j == n:
                    continue
                A[i], A[j] = A[j], A[i]
            for j in range(i+1, n):
                factor = -A[j][i] / A[i][i]
                for k in range(n):
                    A[j][k] += factor * A[i][k]
            rank += 1
        return rank
    
    def log_size(bp):
        return math.log(len(bp))
    
    results = []
    n_values = [5, 10, 15, 20, 30, 40]
    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            bp = generate_read_twice_bp(n)
            partition = noncrossing_partition(bp)
            rank = rank_of_partition(partition)
            results.append((n, rank))
    
    if len(results) < 180:
        return {
            "metric_name": "rank/log_size_ratio",
            "metric_value": None,
            "instances_tested": len(results),
            "conjecture_holds": False,
            "counterexample": "not_enough_data"
        }
    
    ratios = [rank / log_size(bp) for n, rank in results]
    mean_ratio = sum(ratios) / len(ratios)
    std_dev = math.sqrt(sum((x - mean_ratio)**2 for x in ratios) / len(ratios))
    
    return {
        "metric_name": "rank/log_size_ratio",
        "metric_value": mean_ratio,
        "instances_tested": len(results),
        "conjecture_holds": all(x <= 1 for x in ratios),
        "counterexample": "" if all(x <= 1 for x in ratios) else f"mean_ratio={mean_ratio}, std_dev={std_dev}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_ratio = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_ratio)**2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_dev} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mean_ratio={results[first_failing]['metric_value']}, std_dev={std_dev}\" first_failing_seed={seeds[first_failing]}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")