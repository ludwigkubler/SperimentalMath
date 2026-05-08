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

def generate_branching_program(n, read_twice=False):
    if read_twice:
        # Generate a read-twice branching program for IP_2
        bp = [[random.choice([0, 1]) for _ in range(2)] for _ in range(n)]
        return bp
    else:
        # Generate a read-once branching program for IP_2
        bp = [[random.choice([0, 1]) for _ in range(1)] for _ in range(n)]
        return bp

def adjacency_matrix(bp):
    n = len(bp)
    A = [[0] * n for _ in range(n)]
    for i in range(n):
        if bp[i][0] == 1:
            A[0][i] = 1
        if len(bp[i]) > 1 and bp[i][1] == 1:
            A[i + 1][i] = 1
    return A

def determinant(A):
    n = len(A)
    if n == 1:
        return A[0][0]
    det = 0
    for j in range(n):
        submatrix = [row[:j] + row[j+1:] for row in A[1:]]
        det += (-1) ** j * A[0][j] * determinant(submatrix)
    return det

def r_transform(A):
    n = len(A)
    R = [[0] * (n + 1) for _ in range(n + 1)]
    R[0][0] = 1
    for k in range(1, n + 1):
        R[k][0] = determinant(A ** k)
        for j in range(1, k + 1):
            R[j][k] = R[j-1][k-1] - R[j][k-1]
    return R

def free_cumulant(R):
    n = len(R) - 1
    kappa_4 = (R[2][3] * R[1][2] - R[2][2] * R[1][3]) / (R[0][2] * R[1][1] - R[0][1] * R[1][2])
    return kappa_4

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    for n in range(5, 41):
        for _ in range(3):  # Ensure at least 30 instances per seed
            if n == 5 and len(results) >= 27:
                break
            bp_type = 'read_twice' if random.choice([True, False]) else 'read_once'
            bp = generate_branching_program(n, read_twice=(bp_type == 'read_twice'))
            A = adjacency_matrix(bp)
            kappa_4 = free_cumulant(r_transform(A))
            results.append(kappa_4)
    
    mean_kappa_4 = sum(results) / len(results)
    std_kappa_4 = math.sqrt(sum((x - mean_kappa_4) ** 2 for x in results) / len(results))
    support_fraction = sum(1 for kappa in results if (kappa >= n / 10 if bp_type == 'read_twice' else kappa <= math.log(n) + 1)) / len(results)
    
    conjecture_holds = support_fraction >= 0.8
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "free_cumulant_kappa_4",
        "metric_value": mean_kappa_4,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i - 1 for i in range(5, 31)]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **{result}**}}")
        results.append(result["metric_value"])
    
    mean_kappa_4 = sum(results) / len(results)
    std_kappa_4 = math.sqrt(sum((x - mean_kappa_4) ** 2 for x in results) / len(results))
    support_fraction = sum(1 for kappa in results if kappa >= n / 10) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_kappa_4} std={std_kappa_4} support_fraction={support_fraction}")
    else:
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed=1")