# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
from fractions import Fraction
import math
import itertools

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_disjointness_function(n):
        return lambda x, y: sum(xi != yi for xi, yi in zip(x, y))
    
    def noncrossing_partition_matrix(f, n):
        A = [[f(i, j) for j in range(n)] for i in range(n)]
        rank = 0
        for k in range(1, n + 1):
            for partition in itertools.combinations(range(n), k):
                B = [A[i][j] for i in partition for j in partition]
                if is_independent(B):
                    rank += 1
        return rank
    
    def is_independent(matrix):
        m = len(matrix)
        n = len(matrix[0])
        A = matrix + [[0] * n for _ in range(m)]
        for i in range(m):
            pivot = next((j for j in range(n) if A[i][j]), None)
            if pivot is None:
                return False
            for j in range(i, m):
                A[j][pivot] /= A[i][pivot]
            for j in range(m):
                if j != i and any(A[j][k] != 0 for k in range(n)):
                    for k in range(n):
                        A[j][k] -= A[i][k] * A[j][pivot]
        return True
    
    def communication_complexity(f, n):
        # Example protocol: O(n) bits
        return n
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        f = generate_disjointness_function(n)
        rank = noncrossing_partition_matrix(f, n)
        comm_complexity = communication_complexity(f, n)
        results.append((rank, comm_complexity))
    
    if len(results) < 30:
        return {
            "metric_name": "Spearman rank correlation",
            "metric_value": None,
            "instances_tested": len(results),
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    ranks = [r for r, _ in results]
    comm_complexities = [c for _, c in results]
    
    def spearman_rank_correlation(ranks, comm_complexities):
        n = len(ranks)
        rank_ranks = {x: i + 1 for i, x in enumerate(sorted(set(ranks)))}
        rank_comm_complexities = {x: i + 1 for i, x in enumerate(sorted(set(comm_complexities)))}
        sum_diff_squares = sum((rank_ranks[r] - rank_comm_complexities[c]) ** 2 for r, c in zip(ranks, comm_complexities))
        return 1 - (6 * sum_diff_squares) / (n * (n**2 - 1))
    
    correlation = spearman_rank_correlation(ranks, comm_complexities)
    mean_metric_value = correlation
    support_fraction = len([r for r in ranks if r >= 0.8]) / len(ranks)
    
    return {
        "metric_name": "Spearman rank correlation",
        "metric_value": correlation,
        "instances_tested": len(results),
        "conjecture_holds": support_fraction >= 0.8 and mean_metric_value <= 3,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i + 7 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    all_metric_values = [r["metric_value"] for r in results if r["metric_value"] is not None]
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all_metric_values and support_fraction >= 0.8:
        mean_metric_value = sum(all_metric_values) / len(all_metric_values)
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=NA support_fraction={support_fraction}")
    else:
        first_failing_seed = next((i for i, r in enumerate(results) if not r["conjecture_holds"]), None)
        counterexample = "insufficient_support" if not all_metric_values else ""
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")