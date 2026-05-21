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
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            # Find the pivot row
            max_row = i
            for j in range(i+1, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            
            # Eliminate below the pivot
            for j in range(i+1, m):
                factor = A[j][i] / A[i][i]
                for k in range(n):
                    A[j][k] -= factor * A[i][k]
        
        # Back substitution
        x = [0] * n
        for i in range(m-1, -1, -1):
            x[i] = A[i][-1]
            for j in range(i+1, n):
                x[i] -= A[i][j] * x[j]
            x[i] /= A[i][i]
        
        return x
    
    def matrix_multiply(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[0] * p for _ in range(m)]
        for i in range(m):
            for j in range(p):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C
    
    def construct_quaternion_algebra(P):
        n = len(P)
        Q = [[0] * (2*n) for _ in range(2*n)]
        
        # Construct the quaternion algebra
        for i in range(n):
            for j in range(n):
                if P[i][j]:
                    Q[2*i][2*j] = 1
                    Q[2*i+1][2*j+1] = 1
        
        return Q
    
    def minimal_representation_rank(Q):
        m, n = len(Q), len(Q[0])
        A = [[Q[i][j] for j in range(n)] + [0] * (n - i) for i in range(m)]
        rank = gaussian_elimination(A)
        return sum(1 for x in rank if abs(x) > 1e-9)
    
    def read_twice_branching_program_size(P):
        return len(P) ** 2
    
    n_max = 40
    total_metric_value = 0
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""
    
    for n in range(5, n_max + 1, 5):
        for _ in range(6):  # Sample 6 instances per size
            P = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
            Q = construct_quaternion_algebra(P)
            r_Q = minimal_representation_rank(Q)
            S_P = read_twice_branching_program_size(P)
            
            if r_Q > S_P ** 2:
                conjecture_holds = False
                counterexample = f"r(Q)={r_Q} > S(P)^2={S_P**2}"
                break
            
            total_metric_value += r_Q / (n * n)
            instances_tested += 1
    
    return {
        "metric_name": "Minimal Representation Rank",
        "metric_value": total_metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")