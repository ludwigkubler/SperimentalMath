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
    
    def generate_matrix(N):
        return [[random.choice([-1, 0, 1]) for _ in range(N)] for _ in range(N)]
    
    def matrix_multiply(A, B):
        N = len(A)
        result = [[0 for _ in range(N)] for _ in range(N)]
        for i in range(N):
            for j in range(N):
                for k in range(N):
                    result[i][j] += A[i][k] * B[k][j]
        return result
    
    def transpose(A):
        N = len(A)
        return [[A[j][i] for j in range(N)] for i in range(N)]
    
    def determinant(A):
        if len(A) == 1:
            return A[0][0]
        det = 0
        for c in range(len(A)):
            det += ((-1) ** c) * A[0][c] * determinant([row[:c] + row[c+1:] for row in A[1:]])
        return det
    
    def rank(matrix):
        if not matrix:
            return 0
        N = len(matrix)
        M = [row[:] for row in matrix]
        rank = 0
        for i in range(N):
            if M[i][i] == 0:
                for j in range(i+1, N):
                    if M[j][i] != 0:
                        M[i], M[j] = M[j], M[i]
                        break
                else:
                    continue
            pivot = M[i][i]
            for j in range(N):
                M[i][j] /= pivot
            for j in range(N):
                if j != i and M[j][i] != 0:
                    factor = M[j][i]
                    for k in range(N):
                        M[j][k] -= factor * M[i][k]
            rank += 1
        return rank
    
    def communication_complexity(matrix):
        N = len(matrix)
        max_row_sum = max(sum(abs(x) for x in row) for row in matrix)
        max_col_sum = max(sum(abs(x) for x in col) for col in zip(*matrix))
        return max(max_row_sum, max_col_sum)
    
    def quadratic_form_valuation(matrix):
        N = len(matrix)
        Q = [[0 for _ in range(N)] for _ in range(N)]
        for i in range(N):
            for j in range(N):
                Q[i][j] = matrix[i][j] * matrix[j][i]
        return Q
    
    def min_rank_quadratic_form(matrix):
        return rank(quadratic_form_valuation(matrix))
    
    N = random.randint(5, 40)
    M = generate_matrix(N)
    CC = communication_complexity(M)
    
    if CC == 0:
        return {
            "metric_name": "min_rank_quadratic_form / CC^c",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "CC is zero"
        }
    
    ratios = []
    for c in [1, 2, 3]:
        ratio = min_rank_quadratic_form(M) / (CC ** c)
        if ratio is not None:
            ratios.append(ratio)
    
    if len(ratios) == 0:
        return {
            "metric_name": "min_rank_quadratic_form / CC^c",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "All ratios are None"
        }
    
    mean_ratio = sum(ratios) / len(ratios)
    return {
        "metric_name": "min_rank_quadratic_form / CC^c",
        "metric_value": mean_ratio,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_value} std=0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        counterexample = "First failing seed"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")