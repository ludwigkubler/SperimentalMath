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
    
    def generate_boolean_matrix(n):
        return [[random.choice([-1, 0, 1]) for _ in range(n)] for _ in range(n)]
    
    def matrix_multiplication(A, B):
        n = len(A)
        C = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C
    
    def gaussian_elimination(A, b):
        n = len(A)
        Augmented = [A[i] + [b[i]] for i in range(n)]
        for i in range(n):
            max_row = max(range(i, n), key=lambda x: abs(Augmented[x][i]))
            Augmented[i], Augmented[max_row] = Augmented[max_row], Augmented[i]
            for j in range(i + 1, n):
                factor = Augmented[j][i] / Augmented[i][i]
                for k in range(n + 1):
                    Augmented[j][k] -= factor * Augmented[i][k]
        x = [0] * n
        for i in range(n - 1, -1, -1):
            x[i] = (Augmented[i][-1] - sum(Augmented[i][j] * x[j] for j in range(i + 1, n))) / Augmented[i][i]
        return x
    
    def communication_complexity(M):
        n = len(M)
        count = 0
        for i in range(n):
            for j in range(n):
                if M[i][j] != 0:
                    count += 1
        return count * math.log2(count) if count > 0 else 0
    
    def minimal_rank(M):
        n = len(M)
        A = [row[:] for row in M]
        b = [sum(row[i] for row in A) for i in range(n)]
        x = gaussian_elimination(A, b)
        rank = sum(1 for val in x if abs(val) > 1e-9)
        return rank
    
    def quadratic_form(M):
        n = len(M)
        Q = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                Q[i][j] = sum(M[k][i] * M[k][j] for k in range(n))
        return Q
    
    def spearman_rank_correlation(ranks1, ranks2):
        n = len(ranks1)
        if n != len(ranks2):
            raise ValueError("Ranks lists must have the same length")
        
        sorted_ranks1 = sorted(range(n), key=lambda i: ranks1[i])
        sorted_ranks2 = sorted(range(n), key=lambda i: ranks2[i])
        
        rho_numerator = sum((sorted_ranks1[i] - sorted_ranks2[i]) ** 2 for i in range(n))
        rho_denominator = n * (n**2 - 1)
        return 1 - 6 * rho_numerator / rho_denominator
    
    def compute_metric(M):
        Q = quadratic_form(M)
        rank_Q = minimal_rank(Q)
        CC_M = communication_complexity(M)
        
        if CC_M == 0:
            return None
        
        ratios = [rank_Q / (CC_M ** c) for c in range(1, 4)]
        return sum(ratios) / len(ratios)
    
    n = random.randint(5, 40)
    M = generate_boolean_matrix(n)
    metric_value = compute_metric(M)
    
    if metric_value is None:
        return {
            "metric_name": "Spearman's rank correlation",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "communication_complexity_zero"
        }
    
    instances_tested = 1
    conjecture_holds = all(metric_value > 0.5 for _ in range(3))
    counterexample = "" if conjecture_holds else "not_enough_evidence"
    
    return {
        "metric_name": "Spearman's rank correlation",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if not results:
        print("RESULT: INCONCLUSIVE no_data")
        sys.exit(0)
    
    mean_metric = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.9:
        print(f"RESULT: SUPPORTED mean={mean_metric} std=NA support_fraction={support_fraction}")
    elif any(result["counterexample"] == "communication_complexity_zero" for result in results):
        print("RESULT: INCONCLUSIVE communication_complexity_zero")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"not_enough_evidence\" first_failing_seed={first_failing_seed}")