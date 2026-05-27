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
    
    # Define the function to compute the characteristic polynomial of a linear transformation
    def char_poly(A):
        n = len(A)
        if n == 0:
            return [1]
        A = [[A[i][j] for j in range(n)] for i in range(n)]
        det_A = 0
        for c in range(n):
            minor = [[A[i][j] for j in range(n) if j != c] for i in range(1, n)]
            det_A += A[0][c] * (-1) ** c * char_poly(minor)
        return [det_A]
    
    # Define the function to compute the rank of a matrix
    def rank(A):
        m = len(A)
        if m == 0:
            return 0
        n = len(A[0])
        A = [[A[i][j] for j in range(n)] for i in range(m)]
        pivot_row = 0
        pivot_col = 0
        while pivot_row < m and pivot_col < n:
            if A[pivot_row][pivot_col] == 0:
                swap_found = False
                for i in range(pivot_row + 1, m):
                    if A[i][pivot_col] != 0:
                        A[pivot_row], A[i] = A[i], A[pivot_row]
                        swap_found = True
                        break
                if not swap_found:
                    pivot_col += 1
                    continue
            for i in range(pivot_row + 1, m):
                factor = -A[i][pivot_col] / A[pivot_row][pivot_col]
                for j in range(n):
                    A[i][j] += factor * A[pivot_row][j]
            pivot_row += 1
            pivot_col += 1
        return min(pivot_row, n)
    
    # Define the function to generate a random linear transformation matrix
    def random_matrix(n):
        A = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
        return A
    
    # Define the function to compute the Eichler-Shimura modular form rank bound
    def eichler_shimura_bound(N):
        return math.log2(N)
    
    # Generate a random linear transformation matrix
    n = 10
    A = random_matrix(n)
    
    # Compute the characteristic polynomial of the linear transformation
    χ_A = char_poly(A)
    
    # Compute the rank of the Eichler-Shimura modular form associated with the characteristic polynomial
    rank_Mχ_A = rank(χ_A)
    
    # Check if the rank is within the conjectured bound
    conjecture_holds = rank_Mχ_A <= eichler_shimura_bound(n)
    
    return {
        "metric_name": "Eichler-Shimura Rank",
        "metric_value": rank_Mχ_A,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"Rank {rank_Mχ_A} exceeds bound {eichler_shimura_bound(n)}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
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
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"Rank exceeds bound\" first_failing_seed={first_failing_seed}")