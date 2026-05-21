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
        n = len(A)
        for i in range(n):
            max_row = i
            for j in range(i+1, n):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            factor = Fraction(A[i][i])
            for j in range(i, n + 1):
                A[i][j] /= factor
            for k in range(n):
                if k != i:
                    factor = Fraction(A[k][i])
                    for j in range(i, n + 1):
                        A[k][j] -= factor * A[i][j]
        return A

    def matrix_multiply(A, B):
        m, p = len(A), len(B[0])
        n = len(B)
        C = [[Fraction(0) for _ in range(p)] for _ in range(m)]
        for i in range(m):
            for j in range(p):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def free_probability_tensor_entanglement(P, Q):
        n = len(P)
        max_val = 0
        for i in range(n):
            for j in range(i+1, n):
                T_i = P[i]
                T_j = Q[j]
                entanglement = abs(matrix_multiply(T_i, T_j)[i][j])
                if entanglement > max_val:
                    max_val = entanglement
        return max_val

    def generate_bp(n):
        P = [[Fraction(0) for _ in range(n)] for _ in range(n)]
        for i in range(n):
            P[i][i] = Fraction(1)
        for i in range(n-1):
            for j in range(i+1, n):
                P[i][j] = Fraction(random.randint(1, 10), random.randint(1, 10))
                P[j][i] = P[i][j]
        return P

    def generate_ip2(n):
        Q = [[Fraction(0) for _ in range(n)] for _ in range(n)]
        for i in range(n):
            Q[i][i] = Fraction(1)
        for i in range(n-1):
            for j in range(i+1, n):
                Q[i][j] = Fraction(random.randint(1, 10), random.randint(1, 10))
                Q[j][i] = Q[i][j]
        return Q

    def check_bp(P):
        entanglement = free_probability_tensor_entanglement(P, P)
        return entanglement <= math.log(len(P))

    def check_ip2(Q):
        entanglement = free_probability_tensor_entanglement(Q, Q)
        return entanglement >= len(Q)

    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        P = generate_bp(n)
        Q = generate_ip2(n)
        
        bp_result = check_bp(P)
        ip2_result = check_ip2(Q)
        
        results.append({
            "n": n,
            "bp_entanglement": free_probability_tensor_entanglement(P, P),
            "ip2_entanglement": free_probability_tensor_entanglement(Q, Q),
            "bp_valid": bp_result,
            "ip2_valid": ip2_result
        })

    metric_value_bp = sum(result["bp_entanglement"] for result in results) / len(results)
    metric_value_ip2 = sum(result["ip2_entanglement"] for result in results) / len(results)
    
    conjecture_holds = all(result["bp_valid"] and result["ip2_valid"] for result in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Free Probability Tensor Entanglement",
        "metric_value_bp": metric_value_bp,
        "metric_value_ip2": metric_value_ip2,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)

    mean_bp = sum(result["metric_value_bp"] for result in results) / len(results)
    mean_ip2 = sum(result["metric_value_ip2"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean_bp={mean_bp} std_bp=0 support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unsupported")