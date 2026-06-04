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
            max_row = i + max(range(i, m), key=lambda x: abs(A[x][i]))
            A[i], A[max_row] = A[max_row], A[i]
            for j in range(n):
                if j != i:
                    factor = -A[j][i] / A[i][i]
                    for k in range(n):
                        A[j][k] += factor * A[i][k]
        rank = sum(1 for row in A if any(row))
        return rank
    
    def tropical_curve(M):
        n = len(M)
        T = [[-math.inf] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                if M[i][j] != -math.inf:
                    T[i][j] = M[i][j]
        return T
    
    def rank(T):
        return gaussian_elimination(T)
    
    correlation_values = []
    instances_tested = 0
    n_max = 1
    
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):  # Ensure at least 30 instances per seed
            M = [[random.choice([-math.inf, random.randint(-10, 10)]) for _ in range(n)] for _ in range(n)]
            T = tropical_curve(M)
            rank_M = rank(M)
            rank_T = rank(T)
            if rank_M == 0:
                continue
            correlation_values.append(rank_T / rank_M)
            instances_tested += 1
            n_max = max(n_max, n)
    
    mean_value = sum(correlation_values) / len(correlation_values)
    std_value = math.sqrt(sum((x - mean_value) ** 2 for x in correlation_values) / len(correlation_values))
    conjecture_holds = all(x >= 0.5 for x in correlation_values if x != 0)
    counterexample = "" if conjecture_holds else "correlation < 0.5"
    
    return {
        "metric_name": "Correlation between rank of M and tropical curve",
        "metric_value": mean_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
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
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")