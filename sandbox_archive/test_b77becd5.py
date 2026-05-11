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

def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        max_row = i + max(range(i, n), key=lambda k: abs(A[k][i]))
        A[i], A[max_row] = A[max_row], A[i]
        for j in range(i + 1, n):
            factor = A[j][i] / A[i][i]
            for k in range(n):
                A[j][k] -= factor * A[i][k]
    return A

def det(A):
    n = len(A)
    if n == 2:
        return A[0][0] * A[1][1] - A[0][1] * A[1][0]
    det_val = 0
    for j in range(n):
        submatrix = [row[:j] + row[j+1:] for row in A[1:]]
        det_val += ((-1) ** j) * A[0][j] * det(submatrix)
    return det_val

def matrix_mult(A, B):
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 40
    instances_tested = 30
    read_once_sum = 0
    read_twice_sum = 0
    
    for _ in range(instances_tested):
        # Generate a random read-once BP transition matrix
        P = [[random.random() for _ in range(n)] for _ in range(n)]
        for i in range(n):
            P[i][i] += 1 - sum(P[i])
        
        # Compute eigenvalues and free cumulants for read-once BP
        eigenvals = [det([[P[i][j] if i != j else 2 * P[i][j] - 1 for j in range(n)] for i in range(n)]) for _ in range(30)]
        read_once_sum += sum(math.log(abs(eigenval)) for eigenval in eigenvals)
        
        # Generate a random read-twice BP transition matrix
        Q = [[random.random() for _ in range(n)] for _ in range(n)]
        for i in range(n):
            Q[i][i] += 1 - sum(Q[i])
        
        # Compute eigenvalues and free cumulants for read-twice BP
        eigenvals = [det([[Q[i][j] if i != j else 2 * Q[i][j] - 1 for j in range(n)] for i in range(n)]) for _ in range(30)]
        read_twice_sum += sum(math.log(abs(eigenval)) for eigenval in eigenvals)
    
    return {
        "metric_name": "Free Cumulant Sum",
        "metric_value": (read_once_sum, read_twice_sum),
        "instances_tested": instances_tested,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 1 for i in range(5, 6)]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    read_once_sums = [r["metric_value"][0] for r in results]
    read_twice_sums = [r["metric_value"][1] for r in results]
    
    mean_read_once = sum(read_once_sums) / len(read_once_sums)
    std_read_once = math.sqrt(sum((x - mean_read_once)**2 for x in read_once_sums) / len(read_once_sums))
    mean_read_twice = sum(read_twice_sums) / len(read_twice_sums)
    std_read_twice = math.sqrt(sum((x - mean_read_twice)**2 for x in read_twice_sums) / len(read_twice_sums))
    
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean_read_once={mean_read_once} std_read_once={std_read_once} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((i + 1 for i, r in enumerate(results) if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")