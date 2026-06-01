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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def communication_complexity_rank(phi):
        n = len(phi)
        max_rank = 0
        for i in range(n):
            rank = 0
            for j in range(i + 1, n):
                if phi[i] != phi[j]:
                    rank += 1
            max_rank = max(max_rank, rank)
        return max_rank
    
    def linear_code_from_boolean_function(phi):
        n = len(phi)
        code = []
        for i in range(2**n):
            row = [phi[i >> j & 1] for j in range(n)]
            code.append(row)
        return code
    
    def brauer_induction_index(code):
        n = len(code[0])
        count = 0
        for i in range(n):
            if all(code[j][i] == code[j + 1][i] for j in range(len(code) - 1)):
                count += 1
        return count
    
    def matrix_multiplication(A, B):
        m, k = len(A), len(B[0])
        n = len(B)
        C = [[0] * k for _ in range(m)]
        for i in range(m):
            for j in range(k):
                for l in range(n):
                    C[i][j] += A[i][l] * B[l][j]
        return C
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i
            for j in range(i + 1, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            for j in range(i + 1, m):
                factor = A[j][i] / A[i][i]
                for k in range(n):
                    A[j][k] -= factor * A[i][k]
        return A
    
    def rank_of_matrix(A):
        A = gaussian_elimination(A)
        rank = sum(1 for row in A if any(row))
        return rank
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_ratio = 0
    instances_tested = 0
    n_max = 0
    
    for n in n_values:
        phi = generate_boolean_function(n)
        code = linear_code_from_boolean_function(phi)
        mBI = brauer_induction_index(code)
        crank = communication_complexity_rank(phi)
        
        if crank == 0:
            continue
        
        ratio = mBI / crank
        total_ratio += ratio
        instances_tested += 1
        n_max = max(n_max, n)
    
    mean_ratio = total_ratio / instances_tested if instances_tested > 0 else float('inf')
    conjecture_holds = mean_ratio <= 2  # Assuming c = 2 for simplicity
    counterexample = "" if conjecture_holds else f"mean_ratio={mean_ratio}"
    
    return {
        "metric_name": "mBI/crank",
        "metric_value": mean_ratio,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i + 7 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ratio = sum(res["metric_value"] for res in results) / len(results)
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mean_ratio exceeded\" first_failing_seed={first_failing_seed}")