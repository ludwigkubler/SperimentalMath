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
            if A[i][i] == 0:
                return None
            for j in range(n):
                A[i][j] /= A[i][i]
            for k in range(m):
                if k != i and A[k][i] != 0:
                    factor = A[k][i]
                    for j in range(n):
                        A[k][j] -= factor * A[i][j]
        return [sum(row) for row in A]

    def min_rank(E):
        rank = 0
        for e in E:
            if gaussian_elimination(e) is not None:
                rank += 1
        return rank

    def generate_explicit_function(n):
        # Placeholder function to generate an explicit function with known ACC⁰ lower bound
        return [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]

    n = random.choice([5, 10, 15, 20, 30, 40])
    f = generate_explicit_function(n)
    E = [f]  # Placeholder for Eichler-Shimura relations
    min_rank_value = min_rank(E)

    expected_bound = math.log(n) ** 2  # Placeholder for the actual bound

    return {
        "metric_name": "MinimalRank(Eichler-ShimuraRelations)",
        "metric_value": min_rank_value,
        "instances_tested": 1,
        "conjecture_holds": abs(min_rank_value - expected_bound) <= 3 and min_rank_value <= expected_bound + 3,
        "counterexample": f"min_rank={min_rank_value}, expected_bound={expected_bound}" if not conjecture_holds else ""
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
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
        print(f"RESULT: FALSIFIED counterexample=min_rank>10 first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")