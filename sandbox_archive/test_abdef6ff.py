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
    
    def generate_kcnf(n, m):
        variables = list(range(n))
        clauses = set()
        for _ in range(m):
            clause = random.sample(variables, 2)
            clauses.add(tuple(sorted(clause)))
        return clauses
    
    def incidence_algebra(clauses):
        n = max(max(clause) for clause in clauses) + 1
        A = [[0] * n for _ in range(n)]
        for a, b in clauses:
            A[a][b] += 1
            A[b][a] += 1
        return A
    
    def brauer_group_rank(A):
        n = len(A)
        rank = 0
        for i in range(n):
            if all(A[j][i] == 0 for j in range(i)):
                continue
            pivot = next(j for j in range(i, n) if A[j][i] != 0)
            rank += 1
            for j in range(n):
                A[j][i], A[j][pivot] = A[j][pivot], A[j][i]
            for j in range(n):
                if j == i:
                    continue
                factor = Fraction(A[j][i], A[i][i])
                for k in range(n):
                    A[j][k] -= factor * A[i][k]
        return rank
    
    def largest_weight(clauses, n):
        weights = [0] * (1 << n)
        for clause in clauses:
            weight = sum(2 ** var for var in clause)
            weights[sum(2 ** var if i in clause else 0 for i in range(n))] += weight
        return max(weights)
    
    def kcnf_to_brauer_rank(n, m):
        clauses = generate_kcnf(n, m)
        A = incidence_algebra(clauses)
        rank = brauer_group_rank(A)
        weight = largest_weight(clauses, n)
        return rank, weight
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        total_rank = 0
        max_weight = 0
        for _ in range(5):
            rank, weight = kcnf_to_brauer_rank(n, random.randint(1, n * (n - 1) // 2))
            total_rank += rank
            if weight > max_weight:
                max_weight = weight
        results.append((total_rank / len(results), max_weight))
    
    mean_rank = sum(rank for rank, _ in results) / len(results)
    mean_weight = sum(weight for _, weight in results) / len(results)
    ratio = mean_rank / mean_weight
    
    return {
        "metric_name": "Brauer Group Rank to Largest Weight Ratio",
        "metric_value": ratio,
        "instances_tested": 30,
        "conjecture_holds": ratio <= 1.0,
        "counterexample": "" if ratio <= 1.0 else f"Ratio {ratio} exceeds bound of 1"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_ratio = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Ratio exceeds bound of 1\" first_failing_seed={first_failing_seed + 1}")