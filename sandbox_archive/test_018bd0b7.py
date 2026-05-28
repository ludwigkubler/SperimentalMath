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

def generate_random_matrix(N):
    return [[random.choice([-1, 1]) for _ in range(N)] for _ in range(N)]

def matrix_rank(M):
    N = len(M)
    A = [row[:] for row in M]
    rank = 0
    for i in range(N):
        if all(A[j][i] == 0 for j in range(rank, N)):
            continue
        rank += 1
        pivot_row = rank - 1
        for j in range(i + 1, N):
            if A[j][i] != 0:
                factor = Fraction(A[j][i], A[pivot_row][i])
                for k in range(N):
                    A[j][k] -= factor * A[pivot_row][k]
    return rank

def communication_complexity(M):
    N = len(M)
    count = 0
    for i in range(N):
        for j in range(i + 1, N):
            if M[i][j] != M[j][i]:
                count += 1
    return count

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):  # Ensure at least 30 instances per seed
            M = generate_random_matrix(n)
            rank_Q = matrix_rank(M)
            CC = communication_complexity(M)
            results.append((n, rank_Q, CC))
    if not results:
        return {
            "metric_name": "communication_complexity",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "No instances generated"
        }
    
    metric_values = [CC * math.log2(n * rank_Q) for n, rank_Q, CC in results]
    mean_metric_value = sum(metric_values) / len(metric_values)
    std_metric_value = (sum((x - mean_metric_value) ** 2 for x in metric_values) / len(metric_values)) ** 0.5
    
    conjecture_holds = any(CC >= 1 * math.log2(n * rank_Q) for n, rank_Q, CC in results if rank_Q < math.log2(n) / 4)
    
    return {
        "metric_name": "communication_complexity",
        "metric_value": mean_metric_value,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else "CC < C * log2(N * rank_Q) for some N and M with rank_Q < log2(N)/4"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **trial_result}}")
        results.append(trial_result)
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_metric_value = (sum((r["metric_value"] - mean_metric_value) ** 2 for r in results if r["metric_value"] is not None) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] and r["counterexample"] != "" for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"] and r["counterexample"] != "")
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")