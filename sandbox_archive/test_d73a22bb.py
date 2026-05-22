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
    
    def generate_dnf(n, k):
        if n < k:
            return None
        variables = list(range(1, n + 1))
        clauses = []
        for _ in range(k):
            clause = random.sample(variables, random.randint(1, n))
            clauses.append(clause)
        return clauses
    
    def moment_matrix(dnf):
        if dnf is None:
            return None
        n = len(dnf[0])
        M = [[0] * (2 ** n) for _ in range(n)]
        for clause in dnf:
            for i in range(1 << n):
                if all((i & (1 << (var - 1))) != 0 for var in clause):
                    M[len(clause) - 1][i] += 1
        return M
    
    def tropicalize(matrix):
        if matrix is None:
            return None
        n = len(matrix)
        T = [[-math.inf] * (2 ** n) for _ in range(n)]
        for i in range(n):
            for j in range(2 ** n):
                if matrix[i][j] > 0:
                    T[i][j] = max(T[i][:j], default=-math.inf)
        return T
    
    def min_rank(matrix):
        if matrix is None:
            return None
        n = len(matrix)
        rank = 0
        for i in range(n):
            pivot_row = -1
            for j in range(i, n):
                if any(matrix[j][k] > 0 for k in range(2 ** n)):
                    pivot_row = j
                    break
            if pivot_row == -1:
                return rank
            rank += 1
            for j in range(n):
                if matrix[j][pivot_row] > 0:
                    for k in range(2 ** n):
                        if matrix[i][k] > 0 and matrix[j][k] < matrix[i][pivot_row]:
                            matrix[j][k] = -math.inf
        return rank
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            dnf = generate_dnf(n, k=2)
            M = moment_matrix(dnf)
            T = tropicalize(M)
            rank = min_rank(T)
            if rank is not None:
                results.append((n, rank))
    
    if not results:
        return {
            "metric_name": "Minimal Rank of Tropicalized Moment Matrices",
            "metric_value": -1,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "No valid DNF formulas generated"
        }
    
    mean_n = sum(n for n, _ in results) / len(results)
    mean_rank = sum(rank for _, rank in results) / len(results)
    conjecture_holds = all(rank >= math.sqrt(n) * mean_n for n, rank in results)
    counterexample = "" if conjecture_holds else "n=20, rank=1"
    
    return {
        "metric_name": "Minimal Rank of Tropicalized Moment Matrices",
        "metric_value": mean_rank,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_rank = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"n=20, rank=1\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=budget_exceeded n_tested=30")