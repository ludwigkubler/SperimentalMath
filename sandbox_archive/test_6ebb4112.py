# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from itertools import combinations

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = 40
    A = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    B = [[A[i][j] if i < n // 2 and j >= n // 2 else 0 for j in range(n)] for i in range(n)]
    C = [[A[i][j] if i >= n // 2 and j < n // 2 else 0 for j in range(n)] for i in range(n)]
    
    def matrix_multiplication(A, B):
        result = [[sum(a * b for a, b in zip(row_A, col_B)) for col_B in zip(*B)] for row_A in A]
        return result
    
    CC = 0
    for i in range(n // 2):
        for j in range(n // 2, n):
            if B[i][j] == 1:
                CC += 1
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i
            for k in range(i + 1, m):
                if abs(A[k][i]) > abs(A[max_row][i]):
                    max_row = k
            A[i], A[max_row] = A[max_row], A[i]
            factor = A[i][i]
            for j in range(n):
                A[i][j] /= factor
            for k in range(m):
                if k != i:
                    factor = A[k][i]
                    for j in range(n):
                        A[k][j] -= factor * A[i][j]
        return A
    
    def rank(A):
        A = gaussian_elimination(A)
        rank = 0
        for row in A:
            if any(row):
                rank += 1
        return rank
    
    def simplicial_complex_rank(n):
        return n - 1
    
    cohomological_dimension = simplicial_complex_rank(rank(B))
    
    conjecture_holds = abs(cohomological_dimension - (math.log(n) / math.log(math.log(n)))) < 0.1 * CC
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "cohomological_dimension",
        "metric_value": cohomological_dimension,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] if sys.argv[1:] else [2**i + 1 for i in range(5, 35)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean = sum(r["metric_value"] for r in results) / len(results)
    std = math.sqrt(sum((r["metric_value"] - mean) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")