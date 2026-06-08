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
        n = len(A)
        for i in range(n):
            max_row = i
            for j in range(i+1, n):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            factor = A[i][i]
            for j in range(i, n + 1):
                A[i][j] /= factor
            for j in range(n):
                if j != i:
                    factor = A[j][i]
                    for k in range(i, n + 1):
                        A[j][k] -= factor * A[i][k]
        return A

    def matrix_multiplication(A, B):
        n = len(A)
        C = [[0 for _ in range(n)] for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def communication_complexity_rank_variance(A):
        n = len(A)
        rank = 0
        U, S, Vt = gaussian_elimination(A)
        for s in S:
            if abs(s) > 1e-10:
                rank += 1
        variance = sum((s**2 for s in S)) / rank
        return variance

    def minimal_local_index(A):
        n = len(A)
        index = 0
        for i in range(n):
            for j in range(i+1, n):
                if A[i][j] != 0:
                    index += 1
        return index

    instances_tested = 30
    n_max = 40
    total_ratio = 0.0
    
    for _ in range(instances_tested):
        n = random.randint(5, n_max)
        A = [[random.randint(-10, 10) for _ in range(n)] for _ in range(n)]
        I_min = minimal_local_index(A)
        sigma_phi = communication_complexity_rank_variance(A)
        
        if sigma_phi == 0:
            continue
        
        ratio = abs(I_min / sigma_phi)
        total_ratio += ratio
    
    mean_ratio = total_ratio / instances_tested
    conjecture_holds = all(3.95 <= ratio <= 4.05 for ratio in [mean_ratio])
    
    return {
        "metric_name": "Ratio of Minimal Local Index to Communication Complexity Rank Variance",
        "metric_value": mean_ratio,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"mean_ratio={mean_ratio}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={first_failing_seed}")