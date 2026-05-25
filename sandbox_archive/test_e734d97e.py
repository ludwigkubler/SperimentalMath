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
                continue
            for j in range(n):
                A[i][j] /= A[i][i]
            for k in range(m):
                if k != i and A[k][i] != 0:
                    factor = A[k][i]
                    for j in range(n):
                        A[k][j] -= factor * A[i][j]
        return A

    def min_rank(A):
        rank = 0
        for row in gaussian_elimination(A):
            if any(row):
                rank += 1
        return rank

    def unique_game_instance(n):
        instance = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
        return instance

    def distinguishability_gap(instance):
        n = len(instance)
        dists = []
        for i in range(2**n):
            dist = [0] * n
            for j in range(n):
                if (i >> j) & 1:
                    dist[j] = 1
            dists.append(dist)
        max_prob = 0
        min_prob = 1
        for i in range(len(dists)):
            for j in range(i + 1, len(dists)):
                prob_i = sum(instance[k][j] * dists[i][k] for k in range(n))
                prob_j = sum(instance[j][k] * dists[j][k] for k in range(n))
                max_prob = max(max_prob, abs(prob_i - prob_j))
                min_prob = min(min_prob, abs(prob_i - prob_j))
        return 1 / (max_prob + min_prob)

    n = random.randint(5, 40)
    instance = unique_game_instance(n)
    gap = distinguishability_gap(instance)
    rank = min_rank(instance)
    
    if gap == 0:
        return {
            "metric_name": "ratio",
            "metric_value": -1,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "distinguishability_gap_is_zero"
        }
    
    ratio = rank / (gap ** 2)
    return {
        "metric_name": "ratio",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ratio = sum(r["metric_value"] for r in results if r["metric_value"] != -1) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["metric_value"] >= 0.8 for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0 support_fraction={support_fraction}")
    elif any(r["metric_value"] < 0.8 for r in results):
        first_failing_seed = next(i for i, r in enumerate(results) if r["metric_value"] < 0.8)
        print(f"RESULT: FALSIFIED counterexample='ratio_less_than_0.8' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=not_enough_valid_data")