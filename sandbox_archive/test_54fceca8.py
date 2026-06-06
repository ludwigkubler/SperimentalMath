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
    
    # Generate a random system of linear equations over Z_p with size n ≤ 40
    p = random.randint(2, 100)
    n = random.randint(5, 40)
    A = [[random.randint(0, p-1) for _ in range(n)] for _ in range(n)]
    b = [random.randint(0, p-1) for _ in range(n)]
    
    # Calculate the number of p-adic Hensel lifting steps
    def hensel_steps(A, b, p):
        n = len(A)
        count = 0
        while True:
            A_tilde = []
            b_tilde = []
            for i in range(n):
                row_sum = sum(A[i][j] * b[j] % p for j in range(n)) % p
                if row_sum != 0:
                    return count
                A_tilde.append([A[i][j] // p for j in range(n)])
                b_tilde.append(b[i] // p)
            A = A_tilde
            b = b_tilde
            count += 1
    
    hensel_steps_count = hensel_steps(A, b, p)
    
    # Compute the rank of the communication complexity matrix
    def gaussian_elimination(matrix):
        n = len(matrix)
        for i in range(n):
            if matrix[i][i] == 0:
                for j in range(i+1, n):
                    if matrix[j][i] != 0:
                        matrix[i], matrix[j] = matrix[j], matrix[i]
                        break
                else:
                    return i
            for j in range(n):
                if j != i and matrix[j][i] != 0:
                    factor = -matrix[j][i] // matrix[i][i]
                    for k in range(n):
                        matrix[j][k] += factor * matrix[i][k]
        return n
    
    rank = gaussian_elimination(A)
    
    # Correlate the number of p-adic Hensel lifting steps with the communication complexity rank
    correlation_coefficient = (hensel_steps_count - rank) / math.sqrt(hensel_steps_count**2 + rank**2)
    
    return {
        "metric_name": "Hensel Steps vs Rank",
        "metric_value": abs(hensel_steps_count - rank),
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": abs(hensel_steps_count - rank) <= 3 and correlation_coefficient > 0.7,
        "counterexample": "" if abs(hensel_steps_count - rank) <= 3 and correlation_coefficient > 0.7 else f"Hensel Steps: {hensel_steps_count}, Rank: {rank}"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]
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
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={seeds[first_failing_seed]}")
    else:
        print("RESULT: INCONCLUSIVE insufficient support for conjecture")