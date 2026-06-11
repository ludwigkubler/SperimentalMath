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
            max_row = i + max(range(i, m), key=lambda r: abs(A[r][i]))
            A[i], A[max_row] = A[max_row], A[i]
            for j in range(n):
                if j != i:
                    factor = Fraction(A[j][i], A[i][i])
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        return A

    def matrix_multiply(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[Fraction(0) for _ in range(p)] for _ in range(m)]
        for i in range(m):
            for j in range(n):
                for k in range(p):
                    C[i][k] += A[i][j] * B[j][k]
        return C

    def determinant(A):
        m, n = len(A), len(A[0])
        if m != n:
            raise ValueError("Matrix must be square")
        if n == 1:
            return A[0][0]
        det = Fraction(0)
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for row in A[1:]]
            det += (-1)**j * A[0][j] * determinant(submatrix)
        return det

    def local_induction_dimension(C):
        # Simplified version of LID calculation
        n = len(C)
        A = [[Fraction(0) for _ in range(n)] for _ in range(n)]
        for i in range(n):
            for j in range(n):
                if C[i][j] == 1:
                    A[i][j] = Fraction(1, 2)
        return determinant(gaussian_elimination(A))

    def communication_complexity_rank(C):
        # Simplified version of rank calculation
        n = len(C)
        A = [[Fraction(0) for _ in range(n)] for _ in range(n)]
        for i in range(n):
            for j in range(n):
                if C[i][j] == 1:
                    A[i][j] = Fraction(1, 2)
        return len([row for row in gaussian_elimination(A) if any(row)])

    def variance(lst):
        mean = sum(lst) / len(lst)
        return sum((x - mean) ** 2 for x in lst) / len(lst)

    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        for _ in range(5):
            C = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
            lid = local_induction_dimension(C)
            rank = communication_complexity_rank(C)
            variance_rank = variance(rank)
            results.append((n, lid, variance_rank))
    
    mtr_values = [lid for _, lid, _ in results]
    variance_rank_values = [variance_rank for _, _, variance_rank in results]
    
    correlation_coefficient = sum((mtr - mean_mtr) * (variance_rank - mean_variance_rank) for mtr, variance_rank in zip(mtr_values, variance_rank_values)) / len(results)
    mean_mtr = sum(mtr_values) / len(mtr_values)
    median_mtr = sorted(mtr_values)[len(mtr_values) // 2]
    
    conjecture_holds = correlation_coefficient >= 0.8 and abs(mean_mtr - median_mtr) <= 3
    counterexample = "" if conjecture_holds else "correlation_coefficient=<{}> mean_mtr=<{}> median_mtr=<{}>".format(correlation_coefficient, mean_mtr, median_mtr)
    
    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print("TRIAL: {}".format(result))
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print("RESULT: SUPPORTED mean={} std={} support_fraction={}".format(mean_metric_value, std_metric_value, support_fraction))
    elif support_fraction >= 0.8:
        print("RESULT: SUPPORTED mean={} std={} support_fraction={}".format(mean_metric_value, std_metric_value, support_fraction))
    else:
        for r in results:
            if not r["conjecture_holds"]:
                counterexample = r["counterexample"]
                first_failing_seed = seed
                break
        
        print("RESULT: FALSIFIED counterexample=\"{}\" first_failing_seed={}".format(counterexample, first_failing_seed))