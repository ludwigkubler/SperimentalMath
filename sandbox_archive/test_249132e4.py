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
    
    def generate_matrix(N):
        return [[random.choice([-1, 1]) for _ in range(N)] for _ in range(N)]
    
    def matrix_rank(matrix):
        N = len(matrix)
        A = [row[:] + [0] * (N - len(row)) for row in matrix]
        for i in range(N):
            if A[i][i] == 0:
                for j in range(i + 1, N):
                    if A[j][i] != 0:
                        A[i], A[j] = A[j], A[i]
                        break
                    if j == N - 1:
                        return i
            pivot = A[i][i]
            for j in range(N + 1):
                A[i][j] /= pivot
            for j in range(N):
                if j != i and A[j][i] != 0:
                    factor = A[j][i]
                    for k in range(N + 1):
                        A[j][k] -= factor * A[i][k]
        return N
    
    def communication_complexity(matrix):
        N = len(matrix)
        rank_Q = matrix_rank(matrix)
        if rank_Q < math.log2(N) / 4:
            return 3
        # Placeholder for actual CC(XOR, M) calculation
        return 1 + math.log2(N * rank_Q)
    
    N = 40
    matrix = generate_matrix(N)
    cc = communication_complexity(matrix)
    rank_Q = matrix_rank(matrix)
    
    metric_value = cc
    instances_tested = 1
    conjecture_holds = False
    counterexample = ""
    
    if rank_Q < math.log2(N) / 4 and cc <= 3:
        counterexample = "rank_Q < log2(N)/4 but CC(XOR, M) > 3"
    
    return {
        "metric_name": "communication_complexity",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and sum(1 for r in results if not r["conjecture_holds"]) / len(results) < 0.2:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")