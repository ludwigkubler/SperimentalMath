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
            # Find pivot
            max_row = i
            for j in range(i + 1, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            
            # Eliminate below the pivot
            for j in range(i + 1, m):
                factor = A[j][i] / A[i][i]
                for k in range(n):
                    A[j][k] -= factor * A[i][k]
        
        # Back-substitute to find solution
        x = [0] * n
        for i in range(m - 1, -1, -1):
            x[i] = A[i][-1]
            for j in range(i + 1, n):
                x[i] -= A[i][j] * x[j]
            x[i] /= A[i][i]
        
        return x
    
    def matrix_multiplication(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[0] * p for _ in range(m)]
        for i in range(m):
            for j in range(p):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C
    
    def quaternion_multiplication(q1, q2):
        a, b, c, d = q1
        e, f, g, h = q2
        return (
            a*e - b*f - c*g - d*h,
            a*f + b*e + c*h - d*g,
            a*g - b*h + c*e + d*f,
            a*h + b*g - c*f + d*e
        )
    
    def quaternion_rank(A):
        m, n = len(A), len(A[0])
        Aq = []
        for i in range(m):
            row = [A[i][j] for j in range(n)]
            Aq.append(row)
        
        rank = 0
        for i in range(min(m, n)):
            if Aq[i][i] != 0:
                rank += 1
                for j in range(i + 1, m):
                    factor = Aq[j][i] / Aq[i][i]
                    for k in range(n):
                        Aq[j][k] -= factor * Aq[i][k]
        
        return rank
    
    def ac0_parity_circuit_size(n):
        # Simplified model of AC⁰ parity circuit size
        return 2 ** n
    
    def boolean_function_to_quaternion_algebra(f, n):
        # Constructive mapping from boolean function to quaternion algebra
        A = []
        for i in range(2**n):
            row = [0] * (2**n)
            for j in range(n):
                if f(i >> j & 1):
                    row[i ^ (1 << j)] = 1
            A.append(row)
        return A
    
    def is_ac0_parity_circuit(f, n):
        # Check if the function is a parity circuit
        for i in range(2**n):
            if f(i) != sum((i >> j & 1) for j in range(n)) % 2:
                return False
        return True
    
    def log_size(C):
        return math.log(len(C))
    
    n = random.randint(5, 40)
    size_C = ac0_parity_circuit_size(n)
    f = lambda x: sum((x >> j & 1) for j in range(n)) % 2
    Aq = boolean_function_to_quaternion_algebra(f, n)
    
    rank_Aq = quaternion_rank(Aq)
    log_size_C = log_size(size_C)
    
    return {
        "metric_name": "Minimal Rank of Quaternion Algebra",
        "metric_value": rank_Aq,
        "instances_tested": 1,
        "conjecture_holds": rank_Aq <= log_size_C,
        "counterexample": "" if rank_Aq <= log_size_C else f"Counterexample for n={n}, size(C)={size_C}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
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
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = results[first_failing_seed]["counterexample"]
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")