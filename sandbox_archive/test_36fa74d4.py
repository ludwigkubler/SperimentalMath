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
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i
            for j in range(i+1, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            factor = Fraction(-A[i][i], A[i][i])
            for j in range(n):
                A[i][j] *= factor
            for j in range(m):
                if i != j:
                    factor = Fraction(A[j][i], A[i][i])
                    for k in range(n):
                        A[j][k] += factor * A[i][k]
        return A
    
    def matrix_multiplication(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[Fraction(0) for _ in range(p)] for _ in range(m)]
        for i in range(m):
            for j in range(n):
                for k in range(p):
                    C[i][k] += A[i][j] * B[j][k]
        return C
    
    def rank(A):
        A = gaussian_elimination(A)
        r = 0
        for row in A:
            if any(row):
                r += 1
        return r
    
    def generate_disjointness_instance(n):
        x = [random.randint(0, 1) for _ in range(n)]
        y = [random.randint(0, 1) for _ in range(n)]
        return x, y
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        total_rank = 0
        for _ in range(5):  # Each n tested 5 times
            x, y = generate_disjointness_instance(n)
            A = [[x[i] + y[j] for j in range(n)] for i in range(n)]
            total_rank += rank(A)
        
        avg_rank = Fraction(total_rank) / 5
        results.append({"n": n, "avg_rank": avg_rank})
    
    metric_value = sum(result["avg_rank"] * result["n"]**2 for result in results) / sum(result["n"]**2 for result in results)
    instances_tested = len(results)
    
    conjecture_holds = all(result["avg_rank"] >= 10 * result["n"]**2 for result in results)
    counterexample = "" if conjecture_holds else f"Failed for n={results[0]['n']}, avg_rank={results[0]['avg_rank']} < 10*{results[0]['n']}^2"
    
    return {
        "metric_name": "Minimal Rank of Tropicalized Configuration Space",
        "metric_value": float(metric_value),
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
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
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Failed for n={results[0]['n']}, avg_rank={results[0]['avg_rank']} < 10*{results[0]['n']}^2\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")