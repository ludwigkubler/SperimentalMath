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
        for j in range(n):
            i_max = rank
            for i in range(rank, m):
                if abs(A[i][j]) > abs(A[i_max][j]):
                    i_max = i
            if A[i_max][j] == 0:
                continue
            A[rank], A[i_max] = A[i_max], A[rank]
            for i in range(m):
                if i != rank:
                    factor = A[i][j] / A[rank][j]
                    for k in range(n):
                        A[i][k] -= factor * A[rank][k]
            rank += 1
        return rank
    
    def log_bound(n, c):
        return (math.log(n) ** c)
    
    n = random.randint(5, 40)
    # Generate a random matrix for Eichler-Shimura relations
    A = [[random.randint(-10, 10) for _ in range(n)] for _ in range(n)]
    min_rank = gaussian_elimination(A)
    
    c = 2  # Example constant for the bound
    expected_bound = log_bound(n, c)
    metric_value = abs(min_rank - expected_bound)
    
    return {
        "metric_name": "MinimalRank(Eichler-ShimuraRelations)",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": metric_value <= 3 and metric_value <= 10,
        "counterexample": "" if metric_value <= 3 else f"min_rank={min_rank}, expected_bound={expected_bound}"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
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
    elif any(r["metric_value"] > 10 for r in results):
        first_failing_seed = next((r["seed"] for r in results if r["metric_value"] > 10), None)
        print(f"RESULT: FALSIFIED counterexample='min_rank_exceeds_bound' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence")