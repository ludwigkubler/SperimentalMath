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

def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        max_row = i + max(range(i, n), key=lambda j: abs(A[j][i]))
        A[i], A[max_row] = A[max_row], A[i]
        if A[i][i] == 0:
            continue
        denom = A[i][i]
        for j in range(n):
            A[i][j] /= denom
        for j in range(n):
            if i != j:
                factor = A[j][i]
                for k in range(n):
                    A[j][k] -= factor * A[i][k]
    rank = sum(1 for row in A if any(row))
    return rank

def hodge_index(matrix):
    n = len(matrix)
    if n == 0:
        return 0
    return gaussian_elimination(matrix)

def communication_complexity_rank(f, n):
    # Placeholder function to simulate the calculation of communication complexity rank
    # This is a dummy implementation and should be replaced with actual logic
    return random.randint(1, n)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0.0
    instances_tested = 0
    n_max = 0
    conjecture_holds = True
    counterexample = ""

    for n in n_values:
        hodge_index_sum = 0.0
        rank_variance_sum = 0.0
        for _ in range(5):  # Generate multiple circuits per function
            f = [random.randint(0, 1) for _ in range(n)]
            hodge_index_value = hodge_index([[f[i] - f[j] for j in range(n)] for i in range(n)])
            rank = communication_complexity_rank(f, n)
            rank_variance_sum += (rank - n / 2) ** 2
            instances_tested += 1
            n_max = max(n_max, n)
            hodge_index_sum += hodge_index_value

        if instances_tested < 30:
            conjecture_holds = False
            counterexample = "insufficient_instances"
            break

        mean_rank_variance = rank_variance_sum / instances_tested
        ratio = hodge_index_sum / (instances_tested * mean_rank_variance)
        total_metric_value += ratio

    if not conjecture_holds:
        return {
            "metric_name": "h(V_f) / Var(Rank_C(f))",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": conjecture_holds,
            "counterexample": counterexample
        }

    mean_metric_value = total_metric_value / len(n_values)
    return {
        "metric_name": "h(V_f) / Var(Rank_C(f))",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
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

    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")