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
    
    def generate_channel(n):
        X = [random.randint(0, n-1) for _ in range(n)]
        Y = [random.randint(0, n-1) for _ in range(n)]
        P = [[random.random() for _ in range(n)] for _ in range(n)]
        for row in P:
            total = sum(row)
            if total == 0:
                continue
            for i in range(n):
                row[i] /= total
        return X, Y, P
    
    def free_probability_distribution(P):
        n = len(P)
        I = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
        A = [P[i][j] * (I[j][k] - P[k][j]) for i in range(n) for j in range(n) for k in range(n)]
        rank = gaussian_elimination(A)
        return rank
    
    def gaussian_elimination(matrix):
        n = len(matrix)
        for i in range(n):
            max_row = max(range(i, n), key=lambda r: abs(matrix[r][i]))
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            if matrix[i][i] == 0:
                continue
            for j in range(i + 1, n):
                factor = matrix[j][i] / matrix[i][i]
                for k in range(n):
                    matrix[j][k] -= factor * matrix[i][k]
        rank = sum(1 for row in matrix if any(row))
        return rank
    
    def calculate_rank(X, Y, P):
        n = len(P)
        rho_C = free_probability_distribution(P)
        return rho_C
    
    n_values = [5, 10, 15, 20, 30, 40]
    ranks = []
    
    for n in n_values:
        channel = generate_channel(n)
        rank = calculate_rank(*channel)
        ranks.append(rank)
    
    mean_rank = sum(ranks) / len(ranks)
    conjecture_holds = all(rank <= math.log(n) for n, rank in zip(n_values, ranks))
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "mean_rank",
        "metric_value": mean_rank,
        "instances_tested": len(ranks),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else list(range(2, 30)) + [random.randint(100, 999) for _ in range(27)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")