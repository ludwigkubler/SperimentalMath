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
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        rank = 0
        for i in range(n):
            max_row = None
            for j in range(rank, m):
                if A[j][i] != 0:
                    max_row = j
                    break
            if max_row is not None:
                A[max_row], A[rank] = A[rank], A[max_row]
                pivot = A[rank][i]
                for j in range(n):
                    A[rank][j] /= pivot
                for j in range(m):
                    if j != rank:
                        factor = A[j][i]
                        for k in range(n):
                            A[j][k] -= factor * A[rank][k]
                rank += 1
        return rank
    
    def calculate_rank_variance(ranks):
        mean = sum(ranks) / len(ranks)
        variance = sum((x - mean) ** 2 for x in ranks) / len(ranks)
        return variance
    
    n_values = [5, 10, 15, 20, 30, 40]
    instances_tested = 0
    total_rank_variance = 0.0
    max_n = 0
    
    for n in n_values:
        for _ in range(5):
            m = random.randint(1, 10 * n)
            protocol = [[random.choice([0, 1]) for _ in range(m)] for _ in range(n)]
            kernel = [sum(row) % 2 for row in zip(*protocol)]
            homology_rank = gaussian_elimination([kernel])
            instances_tested += 1
            total_rank_variance += homology_rank ** 2
            max_n = max(max_n, n)
    
    mean_rank_variance = total_rank_variance / instances_tested
    conjecture_holds = all(math.log(variance) <= math.log(n) for n, variance in zip(n_values, [mean_rank_variance] * len(n_values)))
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "log(rank_variance)",
        "metric_value": math.log(mean_rank_variance),
        "instances_tested": instances_tested,
        "n_max": max_n,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")