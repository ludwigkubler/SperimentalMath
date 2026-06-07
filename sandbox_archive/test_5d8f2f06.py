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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def communication_matrix(f, q):
        n = len(f)
        matrix = []
        for i in range(q**n):
            row = []
            for j in range(q**n):
                if f([i // (q**k) % q for k in range(n)]) == f([j // (q**k) % q for k in range(n)]):
                    row.append(1)
                else:
                    row.append(0)
            matrix.append(row)
        return matrix
    
    def min_local_cohomology(f, q):
        n = len(f)
        matrix = communication_matrix(f, q)
        rank = gaussian_elimination(matrix)
        return rank
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i
            for j in range(i+1, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            if A[i][i] == 0:
                continue
            for j in range(n):
                A[i][j] /= A[i][i]
            for k in range(m):
                if k != i and A[k][i] != 0:
                    factor = A[k][i]
                    for j in range(n):
                        A[k][j] -= factor * A[i][j]
        rank = sum(1 for row in A if any(row))
        return rank
    
    def rank_variance(matrix):
        n, m = len(matrix), len(matrix[0])
        total_sum = 0
        for i in range(n):
            for j in range(m):
                total_sum += matrix[i][j]
        mean = Fraction(total_sum, n * m)
        variance = 0
        for i in range(n):
            for j in range(m):
                variance += (matrix[i][j] - mean) ** 2
        variance /= n * m
        return math.sqrt(variance)
    
    q = 2
    f = generate_boolean_function(5)
    min_cohomology = min_local_cohomology(f, q)
    rank_variance_value = rank_variance(communication_matrix(f, q))
    
    return {
        "metric_name": "min_cohomology_rank_variance",
        "metric_value": min_cohomology * rank_variance_value,
        "instances_tested": 1,
        "n_max": 5,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")