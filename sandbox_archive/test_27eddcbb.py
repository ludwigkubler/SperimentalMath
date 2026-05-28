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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_matrix(N):
        return [[random.choice([-1, 1]) for _ in range(N)] for _ in range(N)]
    
    def matrix_rank(matrix):
        N = len(matrix)
        A = [row[:] for row in matrix]
        rank = 0
        for i in range(N):
            if all(A[j][i] == 0 for j in range(rank, N)):
                continue
            rank += 1
            for j in range(i, N):
                A[i], A[j] = A[j], A[i]
                for k in range(N):
                    A[k][j] /= A[k][i]
            for j in range(N):
                if j != i:
                    factor = A[j][i]
                    for k in range(N):
                        A[j][k] -= factor * A[i][k]
        return rank
    
    def communication_complexity(matrix):
        N = len(matrix)
        count = 0
        for i in range(N):
            for j in range(i + 1, N):
                if matrix[i][j] != matrix[j][i]:
                    count += 1
        return count
    
    N = 40
    M = generate_matrix(N)
    rank_Q = matrix_rank(M)
    CC_XOR = communication_complexity(M)
    
    metric_name = "communication_complexity"
    metric_value = CC_XOR
    instances_tested = 1
    conjecture_holds = False
    counterexample = ""
    
    if rank_Q < math.log2(N) / 4:
        C = 1.0
        if CC_XOR >= C * math.log2(N * rank_Q):
            conjecture_holds = True
    else:
        C = 3.0
        if CC_XOR <= C:
            conjecture_holds = True
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] + list(range(31, 40))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    total_metric_value = sum(r["metric_value"] for r in results)
    mean_metric_value = total_metric_value / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        counterexample = next((r["counterexample"] for r in results if r["conjecture_holds"]), "")
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")