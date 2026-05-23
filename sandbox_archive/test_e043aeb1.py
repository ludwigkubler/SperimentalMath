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
    
    def generate_polynomial(n):
        coefficients = [random.randint(0, 1) for _ in range(n)]
        return coefficients
    
    def matrix_multiply(A, B):
        m, k = len(A), len(B[0])
        n = len(B)
        result = [[0] * k for _ in range(m)]
        for i in range(m):
            for j in range(k):
                for l in range(n):
                    result[i][j] += A[i][l] * B[l][j]
        return result
    
    def gaussian_elimination(A, b):
        n = len(b)
        augmented_matrix = [A[i] + [b[i]] for i in range(n)]
        for i in range(n):
            max_row = i
            for j in range(i+1, n):
                if abs(augmented_matrix[j][i]) > abs(augmented_matrix[max_row][i]):
                    max_row = j
            augmented_matrix[i], augmented_matrix[max_row] = augmented_matrix[max_row], augmented_matrix[i]
            pivot = augmented_matrix[i][i]
            for j in range(i, n+1):
                augmented_matrix[i][j] /= pivot
            for j in range(n):
                if j != i:
                    factor = augmented_matrix[j][i]
                    for k in range(i, n+1):
                        augmented_matrix[j][k] -= factor * augmented_matrix[i][k]
        return [row[-1] for row in augmented_matrix]
    
    def rank(matrix):
        m, n = len(matrix), len(matrix[0])
        A = [[matrix[i][j] for j in range(n)] for i in range(m)]
        gaussian_elimination(A, [0]*n)
        rank = 0
        for row in A:
            if any(row):
                rank += 1
        return rank
    
    def compute_representation_size(f):
        n = len(f)
        # Simplified representation size calculation based on polynomial degree
        return int(math.log2(n))
    
    results = []
    for _ in range(30):
        n = random.randint(5, 40)
        f = generate_polynomial(n)
        rep_size = compute_representation_size(f)
        min_rank = rank([[random.random() for _ in range(rep_size)] for _ in range(rep_size)])
        results.append(min_rank)
    
    mean_rank = sum(results) / len(results)
    std_rank = math.sqrt(sum((x - mean_rank) ** 2 for x in results) / len(results))
    support_fraction = sum(1 for r in results if abs(r - math.log2(n)) <= 3) / len(results)
    
    conjecture_holds = support_fraction >= 0.8
    counterexample = "" if conjecture_holds else f"mean_rank={mean_rank}, std_rank={std_rank}"
    
    return {
        "metric_name": "Minimal Rank",
        "metric_value": mean_rank,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    std_rank = math.sqrt(sum((r["metric_value"] - mean_rank) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mean_rank={mean_rank}, std_rank={std_rank}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_support")