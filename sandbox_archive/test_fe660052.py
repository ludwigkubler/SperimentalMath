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
        for i in range(m):
            max_row = i + max(range(i, m), key=lambda r: abs(A[r][i]))
            A[i], A[max_row] = A[max_row], A[i]
            pivot = A[i][i]
            if pivot == 0:
                continue
            for j in range(n):
                A[i][j] /= pivot
            for k in range(m):
                if k != i and A[k][i] != 0:
                    factor = A[k][i]
                    for j in range(n):
                        A[k][j] -= factor * A[i][j]
        return A

    def rank(A):
        m, n = len(A), len(A[0])
        rref = gaussian_elimination([row[:] for row in A])
        rank = 0
        for i in range(m):
            if any(rref[i][j] != 0 for j in range(n)):
                rank += 1
        return rank

    def sipser_function(n):
        # Placeholder for Sipser function generation
        # This is a dummy implementation and should be replaced with actual Sipser functions
        return [random.randint(0, 1) for _ in range(2**n)]

    def tropicalized_k_group(f):
        # Placeholder for tropicalized K-group computation
        # This is a dummy implementation and should be replaced with actual computation
        return [[random.random() for _ in range(len(f))] for _ in range(len(f))]

    n_values = [5, 10, 15, 20, 30, 40]
    results = []

    for n in n_values:
        f = sipser_function(n)
        k_group = tropicalized_k_group(f)
        rank_value = rank(k_group)
        results.append((n, rank_value))

    mean_rank = sum(rank_value for _, rank_value in results) / len(results)
    std_dev = math.sqrt(sum((rank_value - mean_rank) ** 2 for _, rank_value in results) / len(results))
    conjecture_holds = all(math.log2(n) <= rank_value <= math.log(n, 10) for n, rank_value in results)

    return {
        "metric_name": "minimal_rank",
        "metric_value": mean_rank,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"n={n}, rank={rank_value}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)

    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_dev = math.sqrt(sum((result["metric_value"] - mean_metric_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_dev} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=mapping_undefined")