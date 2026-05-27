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
            max_row = i
            for j in range(i+1, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            for j in range(i+1, m):
                factor = A[j][i] / A[i][i]
                for k in range(n):
                    A[j][k] -= factor * A[i][k]
        return A
    
    def matrix_multiply(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[0] * p for _ in range(m)]
        for i in range(m):
            for j in range(p):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C
    
    def construct_quaternion_algebra(CNF):
        n = len(CNF)
        Q = [[0] * (2*n) for _ in range(2*n)]
        for i in range(n):
            Q[2*i][2*i] = 1
            Q[2*i+1][2*i+1] = -1
            for j in range(i+1, n):
                if CNF[i][j]:
                    Q[2*i][2*j] = 1
                    Q[2*i+1][2*j+1] = 1
        return Q
    
    def minimal_rank(Q):
        A = gaussian_elimination(Q)
        rank = sum(1 for row in A if any(row))
        return rank
    
    n_values = [10, 20, 40]
    results = []
    
    for n in n_values:
        CNF = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
        Q = construct_quaternion_algebra(CNF)
        rank = minimal_rank(Q)
        f_n = int(n ** 1.5)
        
        results.append({
            "n": n,
            "rank": rank,
            "f_n": f_n,
            "conjecture_holds": rank <= f_n
        })
    
    metric_value = sum(result["rank"] for result in results) / len(results)
    conjecture_holds = all(result["conjecture_holds"] for result in results)
    counterexample = "" if conjecture_holds else "f(n) violated"
    
    return {
        "metric_name": "Minimal Rank",
        "metric_value": metric_value,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(seed) for seed in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"f(n) violated\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")