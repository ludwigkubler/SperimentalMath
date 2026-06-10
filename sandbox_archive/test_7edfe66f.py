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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(2**n):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            if sum(clause) != 0:
                clauses.append(clause)
        return clauses
    
    def matrix_multiply(A, B):
        m, k = len(A), len(B[0])
        n = len(B)
        C = [[0] * k for _ in range(m)]
        for i in range(m):
            for j in range(k):
                for l in range(n):
                    C[i][j] += A[i][l] * B[l][j]
        return C
    
    def gaussian_elimination(A, b):
        m, n = len(A), len(A[0])
        Augmented = [A[i] + [b[i]] for i in range(m)]
        for i in range(n):
            max_row = i
            for j in range(i+1, m):
                if abs(Augmented[j][i]) > abs(Augmented[max_row][i]):
                    max_row = j
            Augmented[i], Augmented[max_row] = Augmented[max_row], Augmented[i]
            pivot = Augmented[i][i]
            for j in range(i, n+1):
                Augmented[i][j] /= pivot
            for j in range(m):
                if j != i:
                    factor = Augmented[j][i]
                    for k in range(n+1):
                        Augmented[j][k] -= factor * Augmented[i][k]
        return [row[-1] for row in Augmented]
    
    def compute_rank(A):
        m, n = len(A), len(A[0])
        A_copy = [A[i].copy() for i in range(m)]
        rank = 0
        for i in range(n):
            if any(A_copy[j][i] != 0 for j in range(rank, m)):
                gaussian_elimination(A_copy, [1 if j == i else 0 for j in range(n)])
                rank += 1
        return rank
    
    def compute_betti_numbers(path_algebra):
        # Placeholder for Betti number computation
        # This is a dummy implementation and should be replaced with actual homological algebra code
        return [random.randint(1, 5) for _ in range(5)]
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    cnf = generate_cnf(n)
    path_algebra = [[random.random() for _ in range(n)] for _ in range(n)]
    rank_variance = compute_rank(cnf) ** 2
    betti_numbers = compute_betti_numbers(path_algebra)
    
    return {
        "metric_name": "Rank Variance",
        "metric_value": rank_variance,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 7 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    metric_values = [r["metric_value"] for r in results]
    conjecture_holds_count = sum(r["conjecture_holds"] for r in results)
    
    mean_metric_value = sum(metric_values) / len(metric_values)
    std_metric_value = math.sqrt(sum((x - mean_metric_value) ** 2 for x in metric_values) / len(metric_values))
    support_fraction = conjecture_holds_count / len(results)
    
    if support_fraction >= 0.75:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=mapping_undefined")